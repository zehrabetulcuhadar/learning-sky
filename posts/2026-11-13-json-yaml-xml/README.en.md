🇬🇧 **English** | [🇹🇷 Türkçe](README.tr.md)

# What are JSON, YAML and XML? When to use which?

> *Researched and written by Zehra. Drafted with AI assistance and reviewed by me.*

**Short answer:** JSON, YAML and XML are three ways to write structured data (objects, lists, numbers, strings) as **plain text**, so a program can save data to a file or send it to another program over the network; this is called **serialization**. Roughly: **JSON** leads in APIs and data exchange between programs, **YAML** in configuration files written by hand (GitHub Actions, Docker Compose, Kubernetes), and **XML** where schema validation, namespaces and document structure matter (older enterprise services, SOAP, Office files, `.csproj`).

## 1. What I researched and why

I use all three formats every day in Learning Sky and had never stopped to think about it: every post has a `meta.json`, the GitHub Action lives in `sky.yml`, and my .NET projects' `.csproj` files are XML. At work there are Angular's `angular.json` and .NET's `appsettings.json`. On the basics planet this is the next step after "how does a computer store data": in memory data is objects, on disk or on the wire it is text. A format sits in between.

## 2. Three key takeaways

1. **Same data, three spellings.** A post's info looks like this in the three formats:

   ```json
   { "title": "What is a database?", "topic": "data", "tags": ["sql", "basics"], "draft": true }
   ```

   ```yaml
   title: What is a database?
   topic: data
   tags: [sql, basics]
   draft: true
   ```

   ```xml
   <post draft="true">
     <title>What is a database?</title>
     <topic>data</topic>
     <tags><tag>sql</tag><tag>basics</tag></tags>
   </post>
   ```

   - **JSON** (JavaScript Object Notation): six types: object, array, string, number, `true/false`, `null`. No comments, no trailing commas, keys in double quotes. Because it is small and strict, every language parses it quickly and identically. It is the common language of REST APIs today.
   - **YAML** ("YAML Ain't Markup Language"): structure through indentation, comments (`#`), quotes usually optional. Designed for humans to read and write. YAML 1.2 is actually a superset of JSON: every valid JSON is valid YAML.
   - **XML** (eXtensible Markup Language): tags and attributes. Longer, but a **schema** (XSD) can formally define and validate the structure, and namespaces let different vocabularies mix. It can also carry mixed content (tags inside text, like HTML).

2. **Each format has its own traps.**
   - **YAML's magic is sometimes a nasty surprise.** Under YAML 1.1 rules, words like `no`, `yes`, `on`, `off` became booleans. The famous "Norway problem": writing `NO` in a list of country codes turned Norway into `false`. `version: 1.10` can become the number `1.1`, and values like `22:22` can turn into base-60 numbers in some parsers. And indentation: one shifted space changes the whole structure. Rule: quote any text you are not sure about (`version: "1.10"`).
   - **JSON's limits:** no comments (which is why files like `tsconfig.json` actually use "JSONC", which allows them), no date type (dates travel as strings, usually ISO 8601: `"2026-12-12"`), and careful with big numbers: JavaScript stores every number as a `double`, so integers above 2^53 (some IDs, for example) lose precision. That is why some APIs send large IDs as strings.
   - **XML's security side:** if an XML parser allows loading external entities, an **XXE** attack becomes possible; an attacker can make the server read a local file. Modern .NET defaults are safe, but older code needs care.

3. **The choice depends on who reads and writes the file.** A trade-off again:

   | | JSON | YAML | XML |
   |---|---|---|---|
   | Who writes it? | Mostly programs | Mostly humans | Both |
   | Comments | No | Yes | Yes |
   | Readability | Good | Very good | Fair (verbose) |
   | Parsing reliability | Very high, strict | Surprising, loose | High, validated by schema |
   | Typical place | APIs, `package.json`, `appsettings.json` | CI/CD, Docker Compose, Kubernetes | SOAP, `.csproj`, SVG, RSS, Office |

   This logic appeared naturally in my own project: `meta.json` is written by me and read by a program, so strictness is good. Only I write `sky.yml`, and I want comments in it. `sky.json` is fully generated and read by the site. And my SVG planets are XML too.

## 3. What I got wrong or still find unclear

- I thought XML was "old and dead". It is not: `.csproj`, SVG, RSS, `.docx` (a zip full of XML files) are everywhere. It just gave way to JSON in new APIs.
- I thought JSON was specific to JavaScript; it is a language-independent standard (RFC 8259). C#'s `System.Text.Json` and Python's `json` module read the same format.
- There are binary formats too, like Protobuf and MessagePack, which gRPC uses. Humans cannot read them but they are much smaller and faster. I will open that up in later API posts.

## 4. Example

In [`example/`](example/) the same post info sits in all three formats, and a small Python script reads the JSON and the XML with the standard library and turns both into the same object. The script also shows JavaScript's big-number problem and, in a note, why the word `NO` is dangerous in YAML 1.1.

**AI note:** When I have AI write a GitHub Actions or Docker Compose YAML, I always check the indentation and the key names: it can invent keys from old versions or options that do not exist. Running the YAML through a validator (`actionlint`, schema support in the editor) catches these at once. When I want it to produce JSON, I have to say "valid JSON only, no explanation"; otherwise it may add text like "Here is your JSON:" and break parsing.

## 5. References

_Sources I used for this post. Links last accessed on 18 November 2026._

- RFC 8259, The JavaScript Object Notation (JSON) Data Interchange Format. https://www.rfc-editor.org/rfc/rfc8259
- YAML 1.2.2 Specification. https://yaml.org/spec/1.2.2/
- W3C, Extensible Markup Language (XML) 1.0. https://www.w3.org/TR/xml/
- "The Norway Problem" (common write-ups on the YAML 1.1 boolean issue), e.g. https://hitchdev.com/strictyaml/why/implicit-typing-removed/
- OWASP, "XML External Entity Prevention Cheat Sheet". https://cheatsheetseries.owasp.org/cheatsheets/XML_External_Entity_Prevention_Cheat_Sheet.html
