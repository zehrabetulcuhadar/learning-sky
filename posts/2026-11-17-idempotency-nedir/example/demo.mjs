import { createServer } from "node:http";
import { randomUUID } from "node:crypto";

let charged = 0;                 // total money taken from the customer
const keys = new Map();          // idempotency key -> { body, response }  (a DB table with a UNIQUE key in real life)

const server = createServer(async (req, res) => {
  let raw = "";
  for await (const c of req) raw += c;
  const body = JSON.parse(raw || "{}");

  if (req.url === "/payments-unsafe") {
    charged += body.amount;
    return send(res, 201, { ok: true, charged });
  }

  if (req.url === "/payments") {
    const key = req.headers["idempotency-key"];
    if (!key) return send(res, 400, { error: "Idempotency-Key header is required" });
    const seen = keys.get(key);
    if (seen) {
      if (seen.body !== raw) return send(res, 422, { error: "Key reused with a different request" });
      return send(res, seen.response.status, { ...seen.response.data, replayed: true });
    }
    charged += body.amount;
    const response = { status: 201, data: { ok: true, charged } };
    keys.set(key, { body: raw, response });
    return send(res, response.status, response.data);
  }
  send(res, 404, {});
});

function send(res, status, data) {
  res.writeHead(status, { "Content-Type": "application/json" });
  res.end(JSON.stringify(data));
}

server.listen(0, async () => {
  const base = `http://localhost:${server.address().port}`;
  const post = (path, body, headers = {}) =>
    fetch(base + path, { method: "POST", headers: { "Content-Type": "application/json", ...headers }, body: JSON.stringify(body) })
      .then(async (r) => ({ status: r.status, ...(await r.json()) }));

  console.log("Without idempotency:");
  await post("/payments-unsafe", { amount: 100 }); // response "lost" on the network
  console.log("  retry ->", await post("/payments-unsafe", { amount: 100 }));
  console.log(`  customer was charged ${charged} TL for one purchase ✗\n`);

  charged = 0;
  console.log("With an Idempotency-Key:");
  const key = randomUUID(); // generated ONCE when the user clicks "Pay", reused on every retry
  await post("/payments", { amount: 100 }, { "Idempotency-Key": key }); // response "lost"
  console.log("  retry ->", await post("/payments", { amount: 100 }, { "Idempotency-Key": key }));
  console.log(`  customer was charged ${charged} TL ✓`);
  console.log("  same key, different amount ->", await post("/payments", { amount: 999 }, { "Idempotency-Key": key }));
  server.close();
});
