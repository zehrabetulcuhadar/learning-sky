const base = process.env.API ?? "http://localhost:3000";

async function order(label, body) {
  const res = await fetch(`${base}/api/orders`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  console.log(`${label}: ${res.status}`, await res.json());
}

await order("Valid order          ", { item: "clay-planet", quantity: 2 });
await order("Client says total = 1", { item: "clay-planet", quantity: 2, total: 1 });
await order("Negative quantity    ", { item: "star-sticker", quantity: -5 });
