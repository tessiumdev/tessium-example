import asyncio, json, os, re, urllib.request, websockets

BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]
MINT = "So11111111111111111111111111111111111111112"
MIN_USD = 5000
TEMPLATE = "{side} ${usd} of {mint}\nby {user}\nhttps://solscan.io/tx/{signature}"

ENDPOINT = f"wss://api.tessium.dev/stream?key={os.environ['TESSIUM_API_KEY']}"


def fill(trade):
    return re.sub(r"{(\w+)}", lambda m: str(trade.get(m.group(1), "")), TEMPLATE)


def send(text):
    body = json.dumps({"chat_id": CHAT_ID, "text": text,
                       "disable_web_page_preview": True}).encode()
    request = urllib.request.Request(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        data=body, headers={"Content-Type": "application/json"})
    try:
        urllib.request.urlopen(request, timeout=10)
    except Exception as exc:
        print(f"telegram: {exc}")


async def main():
    async with websockets.connect(ENDPOINT) as ws:
        await ws.send(json.dumps({
            "op": "subscribe",
            "stream": "token_trades",
            "params": {"mint": MINT, "minUsdAmount": MIN_USD},
            "id": 1,
        }))

        async for message in ws:
            frame = json.loads(message)

            if frame["op"] == "error":
                print(f"{frame['code']}: {frame['message']}")
                continue
            if frame["op"] != "event":
                continue

            t = frame["data"]
            send(fill({
                "side": t["tradeType"],
                "usd": t["valueUsd"] or "?",
                "mint": MINT[:4] + "..." + MINT[-4:],
                "user": t["user"],
                "signature": t["signature"],
            }))


try:
    asyncio.run(main())
except websockets.ConnectionClosed as exc:
    print(f"closed ({exc.code})")
