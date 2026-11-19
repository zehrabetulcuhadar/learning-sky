🇬🇧 **English** | [🇹🇷 Türkçe](README.tr.md)

# What is CORS? Why did the browser block my request?

> *Researched and written by Zehra. Drafted with AI assistance and reviewed by me.*

**Short answer:** By default, browsers stop a page's JavaScript from reading a response that comes from a server on **another origin** (origin = scheme + host + port, for example `http://localhost:4200`). This is the **same-origin policy**. **CORS** (Cross-Origin Resource Sharing) is the standard that lets a server say "I allow this origin" with headers like `Access-Control-Allow-Origin`. The key point: **the browser enforces CORS, the server configures it.** That is why a CORS error shows up in the frontend but the fix is in the backend; and CORS does not protect the server, it protects the user.

## 1. What I researched and why

Ever since my first day running Angular and .NET on separate ports, I have known a certain red line: *"Access to XMLHttpRequest at 'http://localhost:5000/api/...' from origin 'http://localhost:4200' has been blocked by CORS policy..."* I usually copied a line from Stack Overflow (`AllowAnyOrigin()`) and moved on. It also confused me that the same request worked fine in Postman. In this extra post on the frontend planet I wanted to understand why CORS exists and how to configure it properly.

## 2. Three key takeaways

1. **The same-origin policy protects the user; CORS relaxes it in a controlled way.** The cookies of the bank I am logged into sit in my browser. Without the same-origin policy, any malicious page I open could call `fetch("https://bank.com/my-accounts")` in the background, the browser would attach my cookies, and the page could **read** the response. The same-origin policy prevents that: the request may go out, but JavaScript cannot read a response from another origin.

   An origin has three parts, and **all three must match**:
   - `http://localhost:4200` vs `http://localhost:5000` → different port, **different origin**.
   - `http://site.com` vs `https://site.com` → different scheme, different origin.
   - `https://site.com` vs `https://api.site.com` → different host, different origin.

   CORS is the server deliberately relaxing that rule: "Yes, `http://localhost:4200` may read my responses." It says so with a header on the response:
   ```
   Access-Control-Allow-Origin: http://localhost:4200
   ```

   **Why does it work in Postman?** Because CORS is a browser rule. Postman, `curl` or another server do not enforce it. That shows something important: **CORS is not a firewall.** Protecting my API from unauthorized access takes authentication and authorization, not CORS.

2. **Before some requests the browser asks for permission: the preflight.** "Simple" requests (only `GET`, `HEAD`, or `POST` with certain content types, and no custom headers) are sent directly; the browser checks the header on the response and lets JavaScript read it or not. But a request is not "simple" when it has:
   - methods like `PUT`, `DELETE`, `PATCH`,
   - `Content-Type: application/json` (yes, every Angular `POST`),
   - custom headers like `Authorization`.

   Then, before the real request, the browser sends an **`OPTIONS` request** (the preflight) to ask:
   ```
   OPTIONS /api/posts
   Origin: http://localhost:4200
   Access-Control-Request-Method: POST
   Access-Control-Request-Headers: content-type, authorization
   ```
   If the server allows it, it answers:
   ```
   Access-Control-Allow-Origin: http://localhost:4200
   Access-Control-Allow-Methods: GET, POST, PUT, DELETE
   Access-Control-Allow-Headers: content-type, authorization
   Access-Control-Max-Age: 600
   ```
   Only then does the real request go out. That is why I see two requests in the DevTools Network tab. `Max-Age` tells the browser how long to cache the permission, so it does not ask before every request. A common mistake: the server's authentication middleware rejects the `OPTIONS` request with `401` because it has no token, and the preflight fails. In ASP.NET Core, `UseCors()` must come **before** `UseAuthentication()` and `UseAuthorization()`.

3. **The right setup: an allow list, not a wildcard.** In ASP.NET Core:
   ```csharp
   builder.Services.AddCors(o => o.AddPolicy("Frontend", p => p
       .WithOrigins("http://localhost:4200", "https://app.company.com")
       .WithMethods("GET", "POST", "PUT", "DELETE")
       .WithHeaders("Content-Type", "Authorization")));
   // ...
   app.UseCors("Frontend");
   ```
   Things to watch:
   - **`AllowAnyOrigin()` (`*`) is easy but usually wrong.** It can fit a public API with no authentication (a public data service, say), not much else.
   - For **requests with cookies** (`withCredentials: true`), `*` does not work anyway; the standard requires an explicit origin and `Access-Control-Allow-Credentials: true` for credentialed requests.
   - **Reflecting the incoming `Origin` header back** (telling every request "you are allowed too") is even more dangerous than `*`, because it works with cookies. It is a common finding in security audits.
   - An alternative in development: the Angular CLI **proxy** (`proxy.conf.json`). The browser calls `localhost:4200/api`, and the dev server forwards it to `localhost:5000`. From the browser's point of view it is the same origin, so CORS never kicks in. In production, if the frontend and the API are served under the same domain (behind a reverse proxy), CORS may not be needed at all.

## 3. What I got wrong or still find unclear

- I thought that when CORS fails, the request never reaches the server. For simple requests it **does reach the server and gets processed**; JavaScript just cannot read the response. So CORS alone does not stop a `POST` from having side effects on the server. That also explains why the attack called CSRF needs separate protection (a topic for another post).
- I thought of CORS as "the backend blocking the frontend". It is really the browser protecting the user; the backend only grants permission by saying "this origin is trusted".
- How `SameSite` cookie settings work together with CORS is still a bit confusing to me.

## 4. Example

[`example/`](example/) has a dependency-free Node.js example: a simple "frontend" page on port `4200` and an "API" on port `5000`. The API's CORS can be switched on and off with an environment variable. Opening the page in a browser, DevTools shows:
- With CORS off: the familiar red error in the console, yet the server log shows the request arrived.
- With CORS on: an `OPTIONS` preflight before the `POST`, then the real request.
- That `curl` from the terminal reaches the same API in every case (proof that CORS is not a firewall).

**AI note:** When I paste a CORS error into an AI, the most common answer is `AllowAnyOrigin().AllowAnyHeader().AllowAnyMethod()`. The error goes away, but if this reaches production the API is open to every site. A better question: "My frontend is `https://app.company.com`, my API is `https://api.company.com`, I do not use cookies, I send an `Authorization` header. What is the narrowest CORS policy, and what should the middleware order be?" I also ask it to suggest options that avoid CORS entirely in development, like the Angular proxy.

## 5. References

_Sources I used for this post. Links last accessed on 18 November 2026._

- MDN Web Docs, "Cross-Origin Resource Sharing (CORS)". https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CORS
- MDN Web Docs, "Same-origin policy". https://developer.mozilla.org/en-US/docs/Web/Security/Same-origin_policy
- WHATWG Fetch Standard, "CORS protocol". https://fetch.spec.whatwg.org/#http-cors-protocol
- Microsoft Learn, "Enable Cross-Origin Requests (CORS) in ASP.NET Core". https://learn.microsoft.com/aspnet/core/security/cors
- Angular Docs, "Proxying to a backend server". https://angular.dev/tools/cli/serve#proxying-to-a-backend-server
- PortSwigger Web Security Academy, "CORS" (common misconfigurations). https://portswigger.net/web-security/cors
