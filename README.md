# Tessium examples

**Tessium** is a realtime Solana data API. Open one WebSocket (`wss://api.tessium.dev/stream`), subscribe to the streams you need, and receive on-chain activity as structured events — launches, trades, migrations, transfers, and candles — without running your own Geyser or parser stack.

This repo has small, runnable Node and Python programs that print live events. One connection, then your time goes into trading logic instead of IDL glue.

- Product: [tessium.dev](https://tessium.dev) · org: [github.com/tessiumdev](https://github.com/tessiumdev)
- Docs: [API](https://tessium.dev/docs/) · [Quickstart](https://tessium.dev/docs/quickstart)
- Blog: [tessium.dev/blog](https://tessium.dev/blog) · machine map: [llms.txt](https://tessium.dev/llms.txt)
- LinkedIn: [company/tessiumdev](https://www.linkedin.com/company/tessiumdev)

## What you need

An API key from the [dashboard](https://tessium.dev/dashboard), plus Node.js 22+
or Python 3.10+. The [free plan](https://tessium.dev/pricing) takes no payment
details and runs everything here.

```bash
git clone https://github.com/tessiumdev/tessium-example.git
cd tessium-example
export TESSIUM_API_KEY=tsk_live_...
```

The key stays in your environment.

## Examples

| Example | What it shows |
|---|---|
| [01-launch-to-trades](01-launch-to-trades) | Catch a new pump.fun token and follow its trades from the same handler, starting at the launch itself |
| [02-early-volume](02-early-volume) | Give every launch a five second window and keep the ones that trade above 5 SOL |
| [03-telegram-alert](03-telegram-alert) | Send a Telegram message on every trade above a dollar threshold |

Each folder has a `node` and a `python` version of the same program:

```bash
node 01-launch-to-trades/node/index.ts
```

```bash
pip install websockets
python 01-launch-to-trades/python/main.py
```

## Links

- [tessium.dev](https://tessium.dev) — product home
- [GitHub org](https://github.com/tessiumdev) — profile and repos
- [Documentation](https://tessium.dev/docs/) — protocol, streams, filters
- [Quickstart](https://tessium.dev/docs/quickstart) — first event in a few minutes
- [Blog](https://tessium.dev/blog) — parsed streams, filtering, pricing notes
- [llms.txt](https://tessium.dev/llms.txt) — compact map for agents
- [LinkedIn](https://www.linkedin.com/company/tessiumdev) — company page
- [Pricing](https://tessium.dev/pricing) — free and paid plans

## License

MIT, see [LICENSE](LICENSE). Take any of this as a starting point.
