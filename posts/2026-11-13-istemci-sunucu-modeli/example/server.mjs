import { createServer } from "node:http";
import { pathToFileURL } from "node:url";

const prices = { "clay-planet": 120, "star-sticker": 15 }; // the server owns the truth

export const server = createServer(async (req, res) => {
  if (req.method === "POST" && req.url === "/api/orders") {
    let body = "";
    for await (const chunk of req) body += chunk;
    const order = JSON.parse(body || "{}");

    // Never trust the client: validate and recalculate on the server.
    if (!(order.item in prices)) return send(res, 400, { error: "Unknown item" });
    if (!Number.isInteger(order.quantity) || order.quantity < 1) return send(res, 400, { error: "Quantity must be a positive integer" });

    const total = prices[order.item] * order.quantity; // ignore any "total" the client sent
    return send(res, 201, { item: order.item, quantity: order.quantity, total });
  }
  send(res, 404, { error: "Not found" });
});

function send(res, status, data) {
  res.writeHead(status, { "Content-Type": "application/json" });
  res.end(JSON.stringify(data));
}

if (import.meta.url === pathToFileURL(process.argv[1]).href) {
  server.listen(3000, () => console.log("Server listening on http://localhost:3000"));
}
