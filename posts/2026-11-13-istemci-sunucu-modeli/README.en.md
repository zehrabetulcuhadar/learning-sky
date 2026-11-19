🇬🇧 **English** | [🇹🇷 Türkçe](README.tr.md)

# What is the client-server model? How are frontend and backend split?

> *Researched and written by Zehra. Drafted with AI assistance and reviewed by me.*

**Short answer:** The client-server model has two roles: the **client** asks for something and the **server** processes the request and answers. The client always starts the conversation. On the web, the client is usually the **frontend** code running in the browser (Angular in my job) and the server is the **backend** code that owns the data and business rules (a .NET API) plus the database behind it. The most important consequence of this line: **the client is in the user's hands, so it cannot be trusted.** Validation, authorization and business rules must live on the server.

## 1. What I researched and why

Every day I work on both the Angular and the .NET side, so I write code on both sides of this line. But I often answer "should this rule go in the frontend or the backend?" out of habit. In the first extra post on the backend planet I wanted to properly write down why this split exists and what it decides.

## 2. Three key takeaways

1. **The role comes from the position in the conversation, not the machine.** A "server" does not mean a big computer; it means a program that listens for requests and answers them. The same machine can be a server in one conversation and a client in another: my .NET API is a server to the browser, but a client when it calls the database or a payment service. Running `ng serve` on my laptop also starts a server (a development server).

   When a web page opens, roughly this happens:
   1. The browser (client) asks the server for the HTML, CSS and JavaScript files.
   2. The Angular app starts running in the browser.
   3. When it needs data, Angular sends an HTTP request to the .NET API with `HttpClient`: `GET /api/posts`.
   4. The API validates the request, reads the data from the database and returns JSON.
   5. Angular renders that JSON on screen.

   This is a **request-response** cycle. The server cannot send anything to the client on its own; that needs extra mechanisms such as WebSockets or Server-Sent Events (which SignalR uses).

2. **Do not trust the client, because the client is in the user's hands.** This is the most important rule I learned. Everything that runs in the browser runs on the user's computer: they can open DevTools and change the JavaScript, remove the `*ngIf` hiding a button, or send any request they like directly to the API with Postman. So:
   - **Frontend validation is for user experience** (an instant "invalid email" hint).
   - **Backend validation is for security and data integrity.** The same rule is always repeated on the backend.
   - "The admin button is only visible to admins" is not a security measure. `[Authorize(Roles = "Admin")]` on the API is.
   - Secrets (API keys, connection strings) never go into frontend code. Angular's `environment.ts` becomes a JavaScript file anyone can read after the build.
   - Prices, discounts and stock are calculated on the server. A "total: 10 TL" coming from the client is not trusted.

3. **The split also shapes scaling and team structure.** Separating frontend and backend (SPA + API) gains a lot: the two sides deploy independently, the same API can serve the web, a mobile app and other services, and the server side can be scaled out horizontally. It has costs too: two projects, managing the API contract, CORS settings, network latency, and the question "what do we show until the data arrives?" (loading states).

   A good server is usually designed to be **stateless**: each request carries everything needed to process it (a token, for example), and the server does not remember anything user-specific between requests. That makes it possible to run ten copies of the same API behind a load balancer; it does not matter which copy answers. State lives in the database, a cache or the client.

   It is not the only model either. With **server-side rendering** (SSR) the page HTML is produced on the server; **static sites** like my Learning Sky site are produced once at build time and served as files, with no backend code at runtime at all. Which one to pick is, again, an architecture decision.

## 3. What I got wrong or still find unclear

- I thought "backend = server, frontend = browser" was a fixed pairing. With SSR part of the Angular code can run on the server too (Angular SSR), and with Node.js you can write a JavaScript backend. The split is not about the language, it is about where the code runs and who is trusted.
- In the peer-to-peer model, for example torrents or WebRTC video calls, everyone is both client and server. For now I only know it by name.
- "Thin client" vs "thick client": how much business logic lives on the client. Angular apps keep getting thicker; I will revisit where that line should be in my architecture posts.

## 4. Example

[`example/`](example/) has a dependency-free, single-file Node.js example: a tiny HTTP server (`server.mjs`) and a client that calls it (`client.mjs`). The client sends three requests: a valid one, a cheating one that claims the total is "1" (the server ignores it and calculates the price itself), and one with a negative quantity that the server rejects. The point is this sentence: whatever the client sends, the server has the final word.

**AI note:** When I have AI write a form feature, it sometimes puts validation only on the Angular side, or does authorization only by hiding a button. In the code it produces I always ask: "Could someone bypass this rule by calling the API directly from Postman?" If yes, the check must go on the server too. I also tell it explicitly: "Write validation on both the frontend and the backend; the backend one is mandatory."

## 5. References

_Sources I used for this post. Links last accessed on 18 November 2026._

- MDN Web Docs, "Client-Server overview". https://developer.mozilla.org/en-US/docs/Learn_web_development/Extensions/Server-side/First_steps/Client-Server_overview
- MDN Web Docs, "An overview of HTTP". https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Overview
- Roy T. Fielding. *Architectural Styles and the Design of Network-based Software Architectures* (2000), Chapter 5: the client-server and stateless constraints.
- OWASP, "Input Validation Cheat Sheet" (on why client-side validation is not security). https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html

---

© 2026 Zehra Betül Çuhadar. The text and figures of this post are licensed under [CC BY-NC-ND 4.0](https://creativecommons.org/licenses/by-nc-nd/4.0/): you may share them with credit and a link, for non-commercial purposes and without changes. The code examples are all rights reserved, see [LICENSE-CODE](../../LICENSE-CODE).
