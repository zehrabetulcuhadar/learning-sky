# Example: watch CORS happen

Needs Node.js 18+ (no packages).

```bash
node cors-demo.mjs                 # CORS off
CORS=on node cors-demo.mjs         # CORS on (PowerShell: $env:CORS="on"; node cors-demo.mjs)
```

Then open http://localhost:4200, press the buttons, and watch:
- the browser console and the Network tab (look for the `OPTIONS` preflight),
- the terminal, which logs every request the API receives.

From another terminal, `curl -X POST http://localhost:5000/api/posts -H "Content-Type: application/json" -d "{}"` works whether CORS is on or off: CORS is enforced by browsers only.
