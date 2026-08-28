# Early volume filter

Most new tokens never trade. This example watches every launch, gives each one a
five second window, adds up the SOL that moved through it, and prints whether it
cleared 5 SOL.

## Run it

```bash
export TESSIUM_API_KEY=tsk_live_...
node node/index.ts
```

```bash
pip install websockets
python python/main.py
```

## What you see

```
skip    0.00 SOL  astro      GrNhsv9p6zfmXNYKnjjbGLt9VjmZMMdZymaBkm4pump
skip    2.85 SOL  Harambe    5qhMxM5BddXrRcv2DnreGzrxwaLdnmjY6eyo872upump
PASS   18.42 SOL  astro      AnYhUVLuw4w5fYGsZ7AWVohykvs7vNM6qV21xgVYpump
skip    0.51 SOL  Colercuck  Gu79skViEZe1jNRYjUCis3E1TyEmzZ77rodSdhP6pump
PASS   19.64 SOL  Solman     8H7Yff7cDfhWKuMbTW3DAZfw4V5fuuUU14hnTJ6Tpump
```

One line per closed window. Zeros are the normal case.

## How it works

**Watch every launch.** Empty `params` means no platform filter. The free plan
sells pump.fun launches, so that is what arrives there; paid plans widen the
same subscription to the other launchpads.

**Give each mint a window.** A new launch opens a `token_trades` subscription
named after the window, and a timer closes it five seconds later. Trades are
matched back to their window by the subscription name in the frame.

**Count the SOL side.** Each trade has two legs; the one in SOL goes into the
total. Trades routed through another token have no SOL leg and stay out of it.

The total adds up `amountRaw`, the integer the chain stores, and compares it
against the threshold scaled by `decimals` from the same trade. Adding the
decimal strings instead would put every trade through floating point, and the
scale is not assumed anywhere: it arrives with the data.

**Hold four windows at a time.** Launches arriving while all four are busy are
skipped, and a slot opens as soon as a window closes.

## Worth knowing

On the free plan an account opens about ten new subscriptions per minute, and
pump.fun alone launches several times that. Refused windows release their slot
and the next launch takes it, so the output shows a sample of the flow rather
than all of it. Paid plans raise both that rate and the four windows this
example holds at once; the [pricing page](https://tessium.dev/pricing) has the
full table.

Five seconds is short on purpose: it keeps slots turning over. Widen the window
and each token gets a longer look, at the cost of measuring fewer of them.

## Reference

- [launches](https://tessium.dev/docs/streams/launches): platforms and payload
- [token_trades](https://tessium.dev/docs/streams/token-trades): filters and
  fields
- [Limits and plans](https://tessium.dev/docs/limits): subscriptions and rates
  per plan
