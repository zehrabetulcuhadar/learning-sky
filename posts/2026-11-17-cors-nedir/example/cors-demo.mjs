import { createServer } from "node:http";

const CORS_ON = process.env.CORS === "on";
const FRONTEND = "http://localhost:4200";

// "API" on port 5000
createServer((req, res) => {
  console.log(`[api] ${req.method} ${req.url}  Origin: ${req.headers.origin ?? "-"}`);
  if (CORS_ON && req.headers.origin === FRONTEND) {   // allow list, not "*" and not reflecting any origin
    res.setHeader("Access-Control-Allow-Origin", FRONTEND);
    res.setHeader("Vary", "Origin");
  }
  if (req.method === "OPTIONS") {                       // preflight
    if (CORS_ON) {
      res.setHeader("Access-Control-Allow-Methods", "GET, POST");
      res.setHeader("Access-Control-Allow-Headers", "Content-Type");
      res.setHeader("Access-Control-Max-Age", "600");
    }
    res.writeHead(204).end();
    return;
  }
  res.writeHead(200, { "Content-Type": "application/json" });
  res.end(JSON.stringify({ posts: ["What is CORS?"], method: req.method }));
}).listen(5000, () => console.log(`API on http://localhost:5000 (CORS ${CORS_ON ? "on" : "off"})`));

// "Frontend" on port 4200: a different origin because the port differs
const page = `<!doctype html><meta charset="utf-8"><title>CORS demo</title>
<body style="font-family:system-ui;padding:24px">
<h1>CORS demo</h1>
<button id="get">Simple GET</button> <button id="post">POST with JSON (preflight)</button>
<pre id="out"></pre>
<script>
const out = document.getElementById("out");
const show = (t) => (out.textContent += t + "\\n");
async function call(opts) {
  try {
    const r = await fetch("http://localhost:5000/api/posts", opts);
    show("OK: " + JSON.stringify(await r.json()));
  } catch (e) {
    show("Blocked: " + e.message + " (see the console; the API terminal still logged the request)");
  }
}
document.getElementById("get").onclick = () => call();
document.getElementById("post").onclick = () =>
  call({ method: "POST", headers: { "Content-Type": "application/json" }, body: "{}" });
</script>`;
createServer((req, res) => res.writeHead(200, { "Content-Type": "text/html" }).end(page))
  .listen(4200, () => console.log(`Frontend on ${FRONTEND}`));
