🇬🇧 **English** | [🇹🇷 Türkçe](README.tr.md)

# What is an exception? How should errors be handled?

> *Researched and written by Zehra. Drafted with AI assistance and reviewed by me.*

**Short answer:** An exception is a mechanism for a function to report that it **cannot do the job it promised to do**. When an exception is thrown (`throw`), normal flow stops and the call stack unwinds back to the first block that catches it (`catch`). If nothing catches it, the program crashes. Good error handling comes down to three rules: **catch only where you can do something about it**, **never swallow errors**, and **use normal control flow, not exceptions, for expected situations.**

## 1. What I researched and why

I write `try/catch` every day, but often by reflex: something might fail here, wrap it, log in the `catch`, carry on. In this second extra post on the basics planet I wanted to question whether that reflex is right. Wide `try/catch` blocks wrapping everything are also one of the patterns I see most often in AI-generated code.

## 2. Three key takeaways

1. **An exception is a message a return value cannot carry.** In old C code, errors were reported through return values (`-1` means error). The problem: the caller can forget to check, and the error flows on silently. An exception cannot be ignored; either someone catches it or the program stops. When one is thrown:
   - The function stops at that point; the remaining lines do not run.
   - The call stack unwinds: a `catch` is searched for at each level.
   - On the way, `finally` blocks run (and in C#, `Dispose` for resources opened with `using`); files and connections get closed.
   - If a matching `catch` is found, execution continues there. If not, the app crashes ("unhandled exception" in .NET, a red error in the browser console).

   Besides the message, the exception object carries a **stack trace**: which file, which line and which chain of calls produced the error. That is the most valuable information when debugging.

2. **Where to catch: where you can do something with the error.** Not every function has to catch its own exceptions; in fact it should not. If a function cannot do anything meaningful with an error, it should let it go up. Meaningful things are:
   - **Recover:** try another way (a fallback source, a default value, a retry).
   - **Add meaning:** wrap a low-level error in a more meaningful one and rethrow. In C#, `throw new OrderException("Could not save the order", ex);` keeps the original as `InnerException`.
   - **Handle at the boundary:** at the outermost layer of the app (a global exception handler and `ProblemDetails` in ASP.NET Core, an `ErrorHandler` and an HTTP interceptor in Angular), show the user a clear message and log the error.

   Things to avoid:
   - **Swallowing errors:** `catch { }` or `catch (Exception) { return null; }`. The error disappears, the program continues with wrong data, and the real problem shows up much later, far away. This is the most dangerous pattern.
   - **Erasing the stack trace:** in C#, `catch (Exception ex) { throw ex; }` restarts the stack trace at that line and the real origin is lost. The right form is just `throw;`.
   - **Catching everything as `Exception`:** it also catches and hides programming errors like `NullReferenceException`. Catch the most specific type you can (`HttpRequestException`, `DbUpdateException`).

3. **An expected situation is not an exception.** "User not found", "form invalid", "out of stock" are part of the program's normal flow. Handling them with exceptions is slow (throwing collects a stack trace, so it is far more expensive than a normal `return`) and hard to read. .NET's own design guidelines say the same: use patterns like `TryParse` for situations that happen often.
   - `int.Parse("abc")` throws; `int.TryParse("abc", out var n)` returns `false`. For user input the second is right.
   - In an API, return `null` / `NotFound()` for a missing record instead of throwing and catching.
   - Some teams use the **Result pattern** for this: a function returns either a success value or an error object, and the caller must handle both.

   A rough split: **exceptions for the truly exceptional** (database unreachable, disk full, a programming bug); **return values for expected outcomes** (not found, invalid).

## 3. What I got wrong or still find unclear

- I thought adding `try/catch` made code "safer". Often the opposite: a `catch` that swallows the error is worse than a crash, because it hides the problem.
- Error flow is different in asynchronous code: in C#, an exception thrown in an `async void` method cannot be caught and can crash the app. In JavaScript, the error of a Promise that is never `await`ed disappears as an "unhandled rejection". I will dig into this in the async/await posts.
- The community seems split on when to choose the Result pattern vs exceptions. Languages like Go and Rust use error values instead of exceptions. I do not have enough experience yet to pick a side.

## 4. Example

[`example/`](example/) has a small Node.js example (with the C# equivalents in comments). It does the same "read settings from a file" job three ways:
1. The **swallowing** version: silently returns `null`, and the program blows up much later in an unrelated place.
2. The **add meaning and rethrow** version: keeps the original error as `cause`.
3. The **return value for the expected case** version: if the file is missing it continues with default settings, but if the file is corrupt it lets the error go up.

**AI note:** One of the things I check most in AI-written code is the `catch` blocks. Common mistakes: wrapping every method in `try/catch (Exception)`, doing only `Console.WriteLine` in the `catch` and carrying on, writing `throw ex;`. I tell it explicitly: "Do not swallow errors; catch only where you can recover and leave the rest to the global handler." I also ask of the code it produces: "what happens if this line throws?" If the answer is "the user sees wrong data and nobody notices", there is a problem.

## 5. References

_Sources I used for this post. Links last accessed on 18 November 2026._

- Microsoft Learn, "Best practices for exceptions" (.NET). https://learn.microsoft.com/dotnet/standard/exceptions/best-practices-for-exceptions
- Microsoft Learn, "Handle errors in ASP.NET Core" (global exception handler, ProblemDetails). https://learn.microsoft.com/aspnet/core/fundamentals/error-handling
- MDN Web Docs, "try...catch" and "Error: cause". https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Error/cause
- Angular Docs, "ErrorHandler". https://angular.dev/api/core/ErrorHandler
- Krzysztof Cwalina, Brad Abrams. *Framework Design Guidelines*, Addison-Wesley (chapter on exceptions).

---

© 2026 Zehra Betül Çuhadar. The text and figures of this post are licensed under [CC BY-NC-ND 4.0](https://creativecommons.org/licenses/by-nc-nd/4.0/): you may share them with credit and a link, for non-commercial purposes and without changes. The code examples are all rights reserved, see [LICENSE-CODE](../../LICENSE-CODE).
