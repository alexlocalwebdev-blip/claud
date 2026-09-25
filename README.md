# claud

## Cloud Nine Vapes

A static landing page for a vape shop, in `site/`:

- 21+ age gate (remembered in `localStorage`)
- Nicotine warning banner
- Product catalog with category filters (devices, pods, e-liquids)
- "Why us" and contact sections

No build step. Open `site/index.html` in a browser, or serve it:

```sh
python3 -m http.server -d site 8000
```

Products are defined in the `products` array in `site/script.js`.

## Paper Trader

A browser-based trading simulator, in `trading/`:

- Five fictional symbols with randomly generated prices that update every second
- Live price chart for the selected symbol
- Market buy/sell orders against $10,000 of fake cash (no short selling)
- Positions with average cost and unrealized P&L, plus trade history
- Account saved in `localStorage`; "Reset account" starts over

Open `trading/index.html`, or `python3 -m http.server -d trading 8001`.
