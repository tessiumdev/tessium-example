import asyncio, json, os, websockets

ENDPOINT = f"wss://api.tessium.dev/stream?key={os.environ['TESSIUM_API_KEY']}"
MIN_USD = 10


async def main():
    async with websockets.connect(ENDPOINT) as ws:
        mint = None

        async def watch_trades(cursor=None):
            frame = {
                "op": "subscribe",
                "stream": "token_trades",
                "sub": "trades",
                "params": {"mint": mint, "minUsdAmount": MIN_USD},
                "id": 2 if cursor else 3,
            }
            if cursor:
                frame["cursor"] = cursor
            await ws.send(json.dumps(frame))

        await ws.send(json.dumps({
            "op": "subscribe",
            "stream": "launches",
            "sub": "launches",
            "params": {"platforms": ["pumpfun"]},
            "id": 1,
        }))

        async for message in ws:
            frame = json.loads(message)

            if frame["op"] == "error":
                # Replay is a paid capability. Without it the live feed is all
                # there is, so ask for that rather than stopping — and say so,
                # because the trades that made the launch worth watching happened
                # before this subscription opened.
                if frame.get("feature") == "cursor":
                    print("  replay is not on this plan; following from here, not from the launch")
                    await watch_trades()
                else:
                    print(f"{frame['code']}: {frame['message']}")
                continue
            if frame["op"] != "event":
                continue

            if frame["stream"] == "launches" and mint is None:
                mint = frame["data"]["mint"]

                # Snipers buy inside the transaction that creates the token, so a
                # subscription that starts "now" opens after the busiest part is
                # over. Every frame carries its own position in the chain, and
                # passing the launch position to the trades subscription tells the
                # server where to resume. That is what keeps the switch lossless.
                await watch_trades(frame["cursor"])
                await ws.send(json.dumps({"op": "unsubscribe", "sub": "launches", "id": 4}))

                print(f"launch {frame['data'].get('symbol', '?')} {mint}")
                continue

            if frame["stream"] == "token_trades":
                t = frame["data"]
                print(f"  {t['tradeType']:<4} ${t['valueUsd'] or '?'} {t['user']}")


try:
    asyncio.run(main())
except websockets.ConnectionClosed as exc:
    print(f"closed ({exc.code})")
