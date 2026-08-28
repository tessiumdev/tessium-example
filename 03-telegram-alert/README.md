# Telegram alert on large trades

Sends a Telegram message for every trade above a dollar threshold. The whole
thing is a subscription, a string template and one HTTP call.

## Set it up

Create a bot with [@BotFather](https://t.me/BotFather) and get its token. To
find your chat id, message your bot once and open
`https://api.telegram.org/bot<TOKEN>/getUpdates`.

```bash
export TESSIUM_API_KEY=tsk_live_...
export TELEGRAM_BOT_TOKEN=123456:AA...
export TELEGRAM_CHAT_ID=12345678
```

## Run it

```bash
node node/index.ts
```

```bash
pip install websockets
python python/main.py
```

## What arrives

```
sell $565.804245960055 of So11...1112
by 9Yp217bd5nHpW4iyifS2cdKEpTZRnafKQQ4dPEussxY3
https://solscan.io/tx/33cUEYW5PveMmZHhE3eLumK3ifVgY54zJdtc44Z2PwqRi7hDWueZ...
```

## What to change

The five constants at the top of the file are the whole configuration:

| Constant | Meaning |
|---|---|
| `MINT` | the token to watch, wrapped SOL by default |
| `MIN_USD` | the dollar threshold below which nothing is sent |
| `TEMPLATE` | the message, with `{side}`, `{usd}`, `{mint}`, `{user}` and `{signature}` filled in per trade |

Two more come from the environment: the bot token and the chat id.

A threshold can be a number or a string. Quantities in events are always
strings, because a JSON number is a float64 and drops digits on large or
fractional values; passing the threshold the same way keeps it exact.

## Worth knowing

The threshold is applied by the server, so trades below it never arrive and cost
you nothing. Raise it before pointing this at a busy token: at `$100` on wrapped
SOL the bot will hit Telegram's rate limits within seconds.

Trades whose dollar value cannot be worked out still pass the threshold and show
up with `?` in place of the amount.

How many subscriptions and connections you get depends on the plan; the
[pricing page](https://tessium.dev/pricing) lists them.

## Reference

- [token_trades](https://tessium.dev/docs/streams/token-trades): filters and
  fields
- [Limits and plans](https://tessium.dev/docs/limits): what each plan allows
