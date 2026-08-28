const BOT_TOKEN = process.env.TELEGRAM_BOT_TOKEN
const CHAT_ID = process.env.TELEGRAM_CHAT_ID
const MINT = 'So11111111111111111111111111111111111111112'
const MIN_USD = 5000
const TEMPLATE = '{side} ${usd} of {mint}\nby {user}\nhttps://solscan.io/tx/{signature}'

const ENDPOINT = `wss://api.tessium.dev/stream?key=${process.env.TESSIUM_API_KEY}`
const ws = new WebSocket(ENDPOINT)

function fill(trade: Record<string, string>) {
    return TEMPLATE.replace(/{(\w+)}/g, (_, field) => trade[field] ?? '')
}

async function send(text: string) {
    const res = await fetch(`https://api.telegram.org/bot${BOT_TOKEN}/sendMessage`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({chat_id: CHAT_ID, text, disable_web_page_preview: true}),
    })
    if (!res.ok) console.error(`telegram ${res.status}: ${await res.text()}`)
}

ws.onopen = () =>
    ws.send(
        JSON.stringify({
            op: 'subscribe',
            stream: 'token_trades',
            params: {mint: MINT, minUsdAmount: MIN_USD},
            id: 1,
        }),
    )

ws.onmessage = (e: MessageEvent) => {
    const frame = JSON.parse(e.data as string)

    if (frame.op === 'error') return console.error(`${frame.code}: ${frame.message}`)
    if (frame.op !== 'event') return

    const t = frame.data
    void send(
        fill({
            side: t.tradeType,
            usd: t.valueUsd ?? '?',
            mint: MINT.slice(0, 4) + '...' + MINT.slice(-4),
            user: t.user,
            signature: t.signature,
        }),
    )
}

ws.onclose = (e: CloseEvent) => console.log(`closed (${e.code})`)
