🇬🇧 **English** | [🇹🇷 Türkçe](README.tr.md)

# What is idempotency? What happens if the same request arrives twice?

> *Researched and written by Zehra. Drafted with AI assistance and reviewed by me.*

**Short answer:** An operation is idempotent if **doing it once or many times leaves the system in the same state**. An elevator button is idempotent: pressing it five times does not call the elevator five times. "Withdraw 100 TL from the account" is not: run it twice and 200 TL is gone. This matters because networks are unreliable: when a client gets no response, it cannot know whether the request reached the server, so it retries. In HTTP, `GET`, `PUT` and `DELETE` are idempotent by definition; `POST` is not. The common way to make operations like `POST` safe to retry is an **idempotency key**: the client sends a unique key per operation, and when the server sees the same key again it does not repeat the work but returns the first response.

## 1. What I researched and why

We have all heard of bugs like "the user clicked pay twice and two orders were created". The first reaction is usually to disable the button after the click. But that only solves part of it: even if the user clicks once, the browser, a mobile network, a proxy or our own `retry` logic can repeat the request. In the second extra post on the backend planet I learned that the real fix is on the server side.

## 2. Three key takeaways

1. **The network delivers "at least once", not "exactly once".** When a client sends a request and gets no response, there are three possibilities:
   - The request never reached the server.
   - It arrived and was processed, but the response got lost.
   - It is still being processed, just slowly.

   The client cannot tell these apart. Its only safe option is to retry. But in the second case, retrying means doing the operation **twice**. In distributed systems, "exactly-once" delivery cannot be guaranteed in practice; what you can do is combine "at least once" delivery with **idempotent processing** so the **effect** happens once. This idea is not only about HTTP; it showed up in message queues too (RabbitMQ, Kafka consumers): the same message can arrive twice, and the consumer must be ready for it.

2. **HTTP methods come with a contract.** The HTTP standard (RFC 9110) describes methods with two properties:
   - **Safe:** does not change anything on the server. `GET`, `HEAD`, `OPTIONS`.
   - **Idempotent:** doing it several times has the same effect as doing it once. All safe methods, plus `PUT` and `DELETE`.
   - `POST` and `PATCH` are not idempotent (in general; a specific `PATCH` can be designed to be).

   Examples:
   - `PUT /users/42 { "name": "Zehra" }` → no matter how many times it is sent, user 42's name is "Zehra". Idempotent.
   - `DELETE /posts/7` → deletes the first time; afterwards it is already gone. The status code may change (200, then 404), but the **effect on the system** is the same. Idempotent, because the definition is about the effect, not the response.
   - `POST /orders` → creates a new order every time. Not idempotent.
   - `PATCH /accounts/1 { "balance": "+100" }` → adds 100 every time. Not idempotent. An absolute value like `{ "balance": 500 }` would be.

   This contract matters in practice: browsers, proxies and HTTP libraries may retry idempotent methods on their own. A `GET` endpoint that changes data on the server (say `GET /delete-user?id=5`) breaks the contract and invites surprises.

3. **Making POST safe: the idempotency key.** The approach used by payment APIs like Stripe and being standardized at the IETF:
   1. When the user clicks "Pay", the client generates a unique key once (usually a UUID).
   2. It sends the request with that key: `Idempotency-Key: 8e03978e-40d5-43e8-bc93-6894a57f9324`.
   3. If the server sees the key for the first time, it does the work and **stores the key together with the response**.
   4. If a request with the same key arrives again, it does not repeat the work; it returns the stored response.
   5. If the same key arrives with a different request body, it returns an error (the key was reused by mistake).

   Things to watch: the key must be **the same on every retry** and **different for every new operation** (so it is generated on the client when the operation starts, not per request). If two identical requests arrive at exactly the same time there can be a race; storing the key with a unique constraint in the database solves it. Keys are not kept forever; they expire after a while (for example 24 hours).

   In simpler cases a **natural key** works too: let the client generate the order number and put a unique constraint on it, or use "update if exists, insert if not" (upsert).

## 3. What I got wrong or still find unclear

- I thought idempotent meant "returns the same response every time". It does not: as in the `DELETE` example, the response can change; what matters is the effect on the system. A `GET` can return different data each time (if the data changed) and still be idempotent.
- I thought disabling the button was enough. It is a good UX measure, but not a guarantee on its own; the real safeguard is on the server.
- How to manage the key's state ("processing" or "done") when the server crashes halfway through looks complicated. I will come back to it with transactions and the outbox pattern.

## 4. Example

[`example/`](example/) has a dependency-free Node.js example: a small "payment" server and a client that simulates a network failure: the first response gets "lost" and the client retries.
- On the endpoint **without a key**, the customer is charged twice.
- On the endpoint **with an idempotency key**, the second request gets the same response and the customer is charged once.
- Reusing the same key with a different amount is rejected with `422`.

On the .NET side the same logic can be built with a middleware or an action filter: read the key from the header and store it in a table with a unique constraint.

**AI note:** When I ask AI to "add retries to this endpoint", it may add `Polly` or an RxJS `retry` without asking whether the endpoint is idempotent. That is fine for `GET`, but blindly adding retries to a `POST /payments` means double charges. So I ask first: "What happens if this operation runs twice?" If the answer is "something bad", idempotency comes first, then retries. In the idempotency code it produces I check: does the key stay the same across retries, or is it accidentally regenerated on every request?

## 5. References

_Sources I used for this post. Links last accessed on 18 November 2026._

- RFC 9110, HTTP Semantics, Section 9.2: Common Method Properties (safe and idempotent methods). https://www.rfc-editor.org/rfc/rfc9110#section-9.2
- IETF HTTPAPI, "The Idempotency-Key HTTP Header Field" (draft). https://datatracker.ietf.org/doc/draft-ietf-httpapi-idempotency-key-header/
- Stripe API Reference, "Idempotent requests". https://docs.stripe.com/api/idempotent_requests
- Brandur Leach. "Implementing Stripe-like Idempotency Keys in Postgres". https://brandur.org/idempotency-keys
- Martin Kleppmann. *Designing Data-Intensive Applications*, O'Reilly, Chapter 11 (exactly-once and idempotence).

---

© 2026 Zehra Betül Çuhadar. The text and figures of this post are licensed under [CC BY-NC-ND 4.0](https://creativecommons.org/licenses/by-nc-nd/4.0/): you may share them with credit and a link, for non-commercial purposes and without changes. The code examples are all rights reserved, see [LICENSE-CODE](../../LICENSE-CODE).
