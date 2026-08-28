import asyncio, json, os, websockets

ENDPOINT = f"wss://api.tessium.dev/stream?key={os.environ['TESSIUM_API_KEY']}"
WSOL = "So11111111111111111111111111111111111111112"
WINDOW_SECONDS = 5
MIN_SOL = 5
SLOTS = 4


async def main():
    async with websockets.connect(ENDPOINT) as ws:
        windows = {}
        next_id = 1

        async def close_window(window_id):
            await asyncio.sleep(WINDOW_SECONDS)
            w = windows.pop(window_id, None)
            if w is None:
                return
            await ws.send(json.dumps({"op": "unsubscribe", "sub": f"w{window_id}",
                                      "id": 1000 + window_id}))
            # The scale comes with the trades themselves, so nothing here assumes
            # what SOL looks like. A window that saw none keeps raw at zero and skips.
            scale = 10 ** w["decimals"]
            verdict = "PASS" if w["raw"] >= MIN_SOL * scale else "skip"
            print(f"{verdict}  {w['raw'] / scale:>6.2f} SOL  {w['symbol'] or '?'}  {w['mint']}")

        await ws.send(json.dumps({"op": "subscribe", "stream": "launches",
                                  "sub": "launches", "params": {}, "id": 0}))

        async for message in ws:
            frame = json.loads(message)

            if frame["op"] == "error":
                # The id echoes the command that failed, so a refused window frees
                # its slot instead of holding one for a subscription that was
                # never created.
                if windows.pop(frame.get("id"), None) is None:
                    print(f"{frame['code']}: {frame['message']}")
                continue
            if frame["op"] != "event":
                continue

            if frame["stream"] == "launches":
                if len(windows) < SLOTS:
                    window_id, next_id = next_id, next_id + 1
                    windows[window_id] = {"mint": frame["data"]["mint"],
                                          "symbol": frame["data"].get("symbol"),
                                          "raw": 0, "decimals": 0}
                    await ws.send(json.dumps({
                        "op": "subscribe",
                        "stream": "token_trades",
                        "sub": f"w{window_id}",
                        "params": {"mint": frame["data"]["mint"]},
                        "id": window_id,
                    }))
                    asyncio.create_task(close_window(window_id))
                continue

            w = windows.get(int(frame["sub"][1:]))
            if w is None:
                continue

            # The total is SOL volume, so each trade contributes its SOL leg. A
            # swap routed through another token adds nothing to this window.
            t = frame["data"]
            leg = t["input"] if t["input"]["mint"] == WSOL else (
                t["output"] if t["output"]["mint"] == WSOL else None)
            # Summing amountRaw keeps the total exact: it is an integer, and adding
            # the decimal strings would go through floating point on every trade.
            if leg:
                w["raw"] += int(leg["amountRaw"])
                w["decimals"] = leg["decimals"]


try:
    asyncio.run(main())
except websockets.ConnectionClosed as exc:
    print(f"closed ({exc.code})")
