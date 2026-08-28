# From a launch to its trades

The launch event carries the mint address, and that is all a `token_trades`
subscription needs. This example takes the first mint that arrives and opens its
trades from the same handler

## Run it

```bash
export TESSIUM_API_KEY=tsk_live_...
node node/index.ts
```

```bash
pip install websockets
python python/main.py
```

Both print the same output

## What you see

```
launch Doll 8iEzwfMgqvkAAVypCjptyozmMK4uD6GAqz4NatCNpGzT
  sell $18.021156390895 HLA488zjtzbnHJBYFjkUpMN26qMPEosMAs6s5wUtYHkL
  sell $10.640443666685 AqUNoT2WY9MGzFshrfswFYbeozodMjjQ7denU5sdu4bg
```

One line for the launch, one per trade above the threshold. Tokens often go
quiet after the first seconds: restart to catch the next one, or drop
`minUsdAmount` to see every trade

## How it works

**Subscribe to launches.** `platforms: ['pumpfun']` narrows the stream to
pump.fun, which is also what the free plan sells.

**Open the trades from the launch handler.** The subscribe frame is the first
thing that branch does. `minUsdAmount: 10` is applied server side, so smaller
trades never reach your process.

**Start at the launch, not at "now".** Every frame carries a `cursor`, its
position in the chain. Passing the launch cursor to the trades subscription
starts the feed there. Bots buy inside the transaction that creates the token,
so a feed starting at the current moment opens after the first wave has traded.

Replay comes with the Starter plan. On free the server answers `not_on_plan`
with `feature: "cursor"`, and the code asks again without it, which gives the
live feed from that point on. See [pricing](https://tessium.dev/pricing) for the
plans that include it.

**Drop the launches subscription.** `unsubscribe` frees the slot.

## Worth knowing

A USD threshold keeps trades that have no dollar value: token-to-token swaps
cannot always be priced, and they arrive with `valueUsd` unset.

`tradeType` is relative to your mint. Leaving the pool is `sell`, arriving is
`buy`.

On paid plans replays are capped at six per hour per account. Past that, a
`replay_rate_limited` notice arrives instead of the catch-up and the
subscription stays live. Each plan sells a different catch-up window; the
[pricing page](https://tessium.dev/pricing) lists them.

For anything long-running, store each event's `cursor` and
[replay the gap](https://tessium.dev/docs/protocol/cursor) after a disconnect.

## Reference

- [token_trades](https://tessium.dev/docs/streams/token-trades): filters and
  fields
- [launches](https://tessium.dev/docs/streams/launches): what a launch carries
- [Cursor and replay](https://tessium.dev/docs/protocol/cursor): positions and
  catch-up
- [Limits and plans](https://tessium.dev/docs/limits): what each plan allows
