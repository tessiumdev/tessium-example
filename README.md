# Tessium examples

Runnable examples for [Tessium](https://tessium.dev), a realtime Solana data API.
Each one is a single file you start with one command and watch print live
on-chain events.

One WebSocket connection gives you decoded launches, trades, transfers and
candles. Set up the connection once, and the rest of your time goes into the
trading logic.

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

- [tessium.dev](https://tessium.dev): what the service does
- [Documentation](https://tessium.dev/docs): protocol, streams, filters
- [Quickstart](https://tessium.dev/docs/quickstart): first event in a few minutes
- [Pricing](https://tessium.dev/pricing): free and paid plans

## License

MIT, see [LICENSE](LICENSE). Take any of this as a starting point.
