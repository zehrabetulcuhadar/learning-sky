# Example: a retry that charges twice, and one that does not

```bash
node demo.mjs
```

Needs Node.js 18+ (no packages). The server keeps balances in memory. The client "loses" the first response and retries, once against an endpoint without idempotency and once with an `Idempotency-Key`.
