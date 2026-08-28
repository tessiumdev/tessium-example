const ENDPOINT = `wss://api.tessium.dev/stream?key=${process.env.TESSIUM_API_KEY}`
const WSOL = 'So11111111111111111111111111111111111111112'
const WINDOW_MS = 5000
const MIN_SOL = 5n
const SLOTS = 4

const ws = new WebSocket(ENDPOINT)
const windows = new Map<number, { mint: string; symbol: string; raw: bigint; decimals: number }>()
let next = 1

function openWindow(mint: string, symbol: string) {
    const id = next++
    windows.set(id, {mint, symbol, raw: 0n, decimals: 0})
    ws.send(
        JSON.stringify({
            op: 'subscribe',
            stream: 'token_trades',
            sub: `w${id}`,
            params: {mint},
            id,
        }),
    )
    setTimeout(() => closeWindow(id), WINDOW_MS)
}

function closeWindow(id: number) {
    const w = windows.get(id)
    if (!w) return
    windows.delete(id)
    ws.send(JSON.stringify({op: 'unsubscribe', sub: `w${id}`, id: 1000 + id}))
    // The scale comes with the trades themselves, so nothing here assumes what
    // SOL looks like. A window that saw none keeps raw at zero and skips.
    const scale = 10n ** BigInt(w.decimals)
    const verdict = w.raw >= MIN_SOL * scale ? 'PASS' : 'skip'
    const sol = (Number(w.raw) / Number(scale)).toFixed(2)
    console.log(`${verdict}  ${sol.padStart(6)} SOL  ${w.symbol ?? '?'}  ${w.mint}`)
}

ws.onopen = () =>
    ws.send(
        JSON.stringify({op: 'subscribe', stream: 'launches', sub: 'launches', params: {}, id: 0}),
    )

ws.onmessage = (e: MessageEvent) => {
    const frame = JSON.parse(e.data as string)

    if (frame.op === 'error') {
        // The id echoes the command that failed, so a refused window frees its slot
        // instead of holding one for a subscription that was never created.
        if (windows.delete(frame.id)) return
        return console.error(`${frame.code}: ${frame.message}`)
    }
    if (frame.op !== 'event') return

    if (frame.stream === 'launches') {
        if (windows.size < SLOTS) openWindow(frame.data.mint, frame.data.symbol)
        return
    }

    const w = windows.get(Number(frame.sub.slice(1)))
    if (!w) return

    // The total is SOL volume, so each trade contributes its SOL leg. A swap
    // routed through another token adds nothing to this window.
    const t = frame.data
    const leg = t.input.mint === WSOL ? t.input : t.output.mint === WSOL ? t.output : null
    // Summing amountRaw keeps the total exact: it is an integer, and adding the
    // decimal strings would go through floating point on every trade.
    if (leg) {
        w.raw += BigInt(leg.amountRaw)
        w.decimals = leg.decimals
    }
}

ws.onclose = (e: CloseEvent) => console.log(`closed (${e.code})`)
