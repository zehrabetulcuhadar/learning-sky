🇬🇧 **English** | [🇹🇷 Türkçe](README.tr.md)

# What data should you never share with AI? Privacy, KVKK and company rules

> *Researched and written by Zehra. Drafted with AI assistance and reviewed by me.*

**Short answer:** Everything you paste or upload into an AI tool is data going to another company's servers. So these are **never** shared directly: **secrets** (passwords, API keys, tokens, connection strings, certificates), **personal data** (national ID numbers, phone numbers, emails, addresses, health or financial information tied to a person), **customer and production data**, and the company's **confidential business information** (unreleased product plans, contracts, security vulnerabilities). Three questions before sharing: Has my company approved this tool? How is data stored in this tool, and is it used for training? Can I ask the same question with masked or fake data?

## 1. What I researched and why

This post was near the end of the AI track in my plan, but I think it is something to know from day one. Every day I paste code, error messages and logs into an AI. While debugging I rarely think that a stack trace might contain a connection string or a customer's email. In 2023 there were news reports that employees at a large tech company pasted confidential source code and meeting notes into a chatbot, and the company banned these tools for a while. So this is not a theoretical risk.

## 2. Three key takeaways

1. **What you paste leaves the company, and you do not control where it ends up.** When I send data to a chat tool, depending on the provider and my plan:
   - The conversation is **stored** on the provider's servers for some time (for abuse monitoring and legal obligations).
   - On individual and free plans, depending on settings, data may be **used to train models**. Enterprise plans and API usage are usually not used for training by default, but this varies between providers and over time. I need to check my own tool's current data policy and settings rather than assume.
   - The servers are most likely **abroad**.
   - Shared chat links, plugins and integrations can carry data elsewhere too.

   Practical consequence: the company-approved tool with an enterprise account and the free tool on my personal account are not the same thing. If the company has an AI usage policy, that policy binds me.

2. **Under KVKK, sending personal data to an AI is a "data transfer".** Under Turkey's Personal Data Protection Law No. 6698 (KVKK), personal data is any information about an identified or identifiable natural person. Pasting a few rows of a customer table to "fix this query" means transferring those people's data to a third party, most likely abroad. Transfers abroad fall under Article 9 of the law; the 2024 amendment tied them to specific conditions such as an adequacy decision or appropriate safeguards like standard contracts. As a developer I cannot decide alone whether those conditions are met; that is the job of the company's legal and information security teams. My job is to **not send** when in doubt, and to use fake or masked data instead.

   Rules are even stricter for special categories of personal data (health, religion, biometrics, criminal convictions). In Europe, the GDPR brings similar obligations.

3. **The rule: mask first, ask with fake data, shrink the context.** Most questions can be asked without real data:
   - **Secrets:** should not be in code anyway (user secrets, environment variables, Key Vault). Before pasting, turn values like `Password=...` into `***`.
   - **Personal data:** give the schema and a few fake rows instead of real customer rows. "User A, 00000000000" instead of a real name and ID number.
   - **Logs and stack traces:** they can contain emails, IPs, tokens, request bodies. Read before sending.
   - **Code:** whether company code may be shared depends on the company. Without an approved enterprise tool, reducing the problem to a small, generic example (a minimal reproducible example) is safer and usually gets a better answer.
   - **Screenshots:** easier to forget than text. The customer name, browser tabs and notifications in the image are data too.
   - **If you shared a secret by accident:** deleting the chat is not enough; **rotate** that key or password immediately.

## 3. What I got wrong or still find unclear

- I thought "I deleted the chat, the data is gone". What deletion means on the provider's side (retention periods, backups) depends on the policy. Assuming a secret has leaked and rotating it is safer.
- Whether the code itself is "confidential" varies by company. Some companies open the whole codebase to enterprise AI tools, others ban them entirely. I am not the one setting the rule; I am the one following it.
- Local models (data never leaves the machine) seem to solve part of this problem, but at a cost in quality and hardware. I will open that up in the "running models locally" post.
- This post is not legal advice; for KVKK details the company's legal team and the Personal Data Protection Authority's guides are the real sources.

## 4. Example

[`example/`](example/) contains a small **masking script** (Python, standard library) to run before pasting something into an AI. It takes text and masks: email addresses, valid Turkish ID numbers (checked with the checksum algorithm, not just any 11-digit number), Turkish IBANs, phone numbers, values like `Password=` and `ApiKey`, `Bearer` tokens and AWS-style access keys. It is not perfect (a list of regexes never is), but it automates the habit of "stop and look once before pasting".

**AI note:** Ironically, you have to be careful asking AI about this too: to ask "is there sensitive data in this log?" I would have to paste the log. I check it with my own eyes and the masking script first. Also, AI can embed secrets in code it writes (for example putting a sample connection string with a real password in `appsettings.json`). In the code it produces I check that secrets are read from environment variables or a secret store.

## 5. References

_Sources I used for this post. Links last accessed on 18 November 2026._

- Personal Data Protection Law No. 6698 (KVKK) and its 2024 amendments (Law No. 7499). https://www.mevzuat.gov.tr/
- Personal Data Protection Authority (KVKK), guides and announcements on transfers abroad. https://www.kvkk.gov.tr/
- OWASP, "Top 10 for Large Language Model Applications" (sensitive information disclosure). https://genai.owasp.org/
- OWASP, "Secrets Management Cheat Sheet". https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html
- Microsoft Learn, "Safe storage of app secrets in development in ASP.NET Core". https://learn.microsoft.com/aspnet/core/security/app-secrets
- Your AI provider's current privacy and data usage policy (date note: written in November 2026; policies change).

---

© 2026 Zehra Betül Çuhadar. The text and figures of this post are licensed under [CC BY-NC-ND 4.0](https://creativecommons.org/licenses/by-nc-nd/4.0/): you may share them with credit and a link, for non-commercial purposes and without changes. The code examples are all rights reserved, see [LICENSE-CODE](../../LICENSE-CODE).
