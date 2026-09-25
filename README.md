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
