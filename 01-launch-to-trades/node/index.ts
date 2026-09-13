const ENDPOINT = `wss://api.tessium.dev/stream?key=${process.env.TESSIUM_API_KEY}`
const MIN_USD = 10

const ws = new WebSocket(ENDPOINT)
let mint: string | null = null

function watchTrades(from?: string) {
    ws.send(
        JSON.stringify({
            op: 'subscribe',
            stream: 'token_trades',
            sub: 'trades',
            cursor: from,
            params: {mint, minUsdAmount: MIN_USD},
            id: from ? 2 : 3,
        }),
    )
}

ws.onopen = () =>
    ws.send(
        JSON.stringify({
            op: 'subscribe',
            stream: 'launches',
            sub: 'launches',
            params: {platforms: ['pumpfun']},
            id: 1,
        }),
    )

ws.onmessage = (e: MessageEvent) => {
    const frame = JSON.parse(e.data as string)

    if (frame.op === 'error') {
        // Replay is a paid capability. Without it the live feed is all there is, so
        // ask for that rather than stopping — and say so, because the trades that
        // made the launch worth watching happened before this subscription opened.
        if (frame.feature === 'cursor') {
            console.log('  replay is not on this plan; following from here, not from the launch')
            watchTrades()
        } else console.error(`${frame.code}: ${frame.message}`)
        return
    }
    if (frame.op !== 'event') return

    if (frame.stream === 'launches' && mint === null) {
        mint = frame.data.mint

        // Snipers buy inside the transaction that creates the token, so a
        // subscription that starts "now" opens after the busiest part is over.
        // Every frame carries its own position in the chain, and passing the launch
        // position to the trades subscription tells the server where to resume.
        // That is what keeps the switch lossless.
        watchTrades(frame.cursor)
        ws.send(JSON.stringify({op: 'unsubscribe', sub: 'launches', id: 4}))

        console.log(`launch ${frame.data.symbol ?? '?'} ${mint}`)
        return
    }

    if (frame.stream === 'token_trades') {
        const t = frame.data
        console.log(`  ${t.tradeType.padEnd(4)} $${t.valueUsd ?? '?'} ${t.user}`)
    }
}

ws.onclose = (e: CloseEvent) => console.log(`closed (${e.code})`)
