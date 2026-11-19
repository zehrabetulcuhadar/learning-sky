🇬🇧 **English** | [🇹🇷 Türkçe](README.tr.md)

# What did we learn from the big outages? CrowdStrike, AWS and Cloudflare

> *Researched and written by Zehra. Drafted with AI assistance and reviewed by me.*

**Short answer:** Most of the outages that took down large parts of the internet in recent years did not come from an attack but from **a change the company made itself**: a faulty content update (CrowdStrike, July 2024), a race condition in an automated DNS system (AWS, October 2025), a configuration file bigger than expected (Cloudflare, November 2025). Their shared lessons: **roll out changes gradually**, **validate even the data you generate yourself**, **keep the blast radius of a failure small**, and **know your shared dependencies.**

## 1. What I researched and why

In November 2026, Apple services, US air traffic and several big banks went down in a single week; the official explanations had one thing in common: "not an attack, an internal update" (details in my monthly news post). Reading these stories in my morning briefing, I noticed something: big outages are almost routine now, and the most educational sources are the **postmortem** reports companies publish afterwards. For this post I read the official reports of three big incidents from recent years and collected the lessons for my own work (Angular, .NET).

## 2. Three key takeaways

1. **CrowdStrike (19 July 2024): one content update, millions of blue screens.** CrowdStrike's Falcon security software has a driver that runs at kernel level on Windows. To recognize new threats, the company pushed "content" files (Channel File 291) to the driver. According to the report, the new template type defined 21 input fields, but the code feeding this file to the driver supplied only 20 values; accessing the 21st caused an out-of-bounds memory read. Because the code runs in the kernel, this was not an application error but an operating system crash. Microsoft estimated about 8.5 million Windows devices were affected; airlines, hospitals and banks stopped. Since machines crashed while booting, in many places the fix had to be applied by hand, one machine at a time.
   - **Lesson:** "content" and "configuration" are code too, and deserve the same testing rigor. Updates should go to a small group first, not to everyone at once (staged rollout, canary). In its report CrowdStrike committed to staged deployment and extra bounds checks for content updates.

2. **AWS us-east-1 (20 October 2025): a DNS record went empty, half the internet stopped.** According to AWS's report, a rare **race condition** occurred in the system that automatically manages DynamoDB's DNS records: when the timing of two automation components overlapped, the DNS record for `dynamodb.us-east-1.amazonaws.com` was left empty. With DynamoDB unreachable, AWS's own services that depend on it (EC2's systems for launching new instances, network load balancers) were hit in a chain reaction. The impact lasted for hours, and many apps, games and messaging services worldwide were disrupted.
   - **Lesson:** a single region and a single foundational service can quietly become a **single point of failure**. There is no such thing as "the cloud never goes down". I need to know which services my system depends on directly or indirectly, and think about how my app behaves if one is unreachable. And the race condition: the "two jobs running at the same time" problem from my concurrency lessons can stop the world's largest cloud.

3. **Cloudflare (18 November 2025): a file that doubled in size.** According to Cloudflare's report, a database (ClickHouse) permissions change caused the query that builds the bot management system's "feature file" to return duplicate rows. The file grew to about twice its normal size and exceeded the limit (200 features) set by the software that processes traffic. Instead of handling this gracefully, the software failed and stopped (the report points to an `unwrap()` call in Rust code). Because the file was regenerated every few minutes, the system kept recovering and failing again, so at first the team suspected an attack. For a few hours X, ChatGPT and many large sites returned errors.
   - **Lesson:** treat the data your own system generates like external input; the assumption "we produce this file, so it is always right" is dangerous. On unexpected input, continuing with the last known good configuration (fail-safe) is safer than taking down the whole process. And if a configuration spreads worldwide in seconds, so does its mistake.

## 3. What I got wrong or still find unclear

- I thought most big outages were cyberattacks. In almost every report I read, the cause was an internal change: an update, a configuration, a permissions change.
- "Staged rollout" sounds simple, but for a security product there is a dilemma: rolling out protection against a new threat slowly is also a risk. I do not fully understand yet how that balance is struck.
- I only know the internal systems mentioned in the reports (like AWS's DNS automation components) as far as the reports describe them. The reports themselves are the real source for details.

## 4. Example

[`example/`](example/) has a small simulation of the Cloudflare incident (Node.js, no packages). A service reads a configuration file that is refreshed every few seconds. One day the file grows past the limit. The script has two versions:
1. **Fragile:** throws and stops when the limit is exceeded.
2. **Resilient:** validates the new file and, if it is invalid, logs a warning and keeps running with the **last known good configuration**.

This is a pattern I can use in my own code: a setting reloaded with `IOptionsMonitor` in .NET, or a remotely fetched feature flag file in Angular, should not crash the app when it arrives broken.

**AI note:** Postmortem reports are long and technical. Giving an AI the whole report and asking it to "extract the root cause, the timeline and the remediations separately, then write three lessons for a .NET developer" works very well. But I always check the numbers (affected devices, durations) against the report myself; AI can mix up such figures or merge them with another incident.

## 5. References

_Sources I used for this post. Links last accessed on 18 November 2026._

- CrowdStrike. "Channel File 291 Incident: Root Cause Analysis" (August 2024). https://www.crowdstrike.com/
- Microsoft. "Helping our customers through the CrowdStrike outage" (July 2024). https://blogs.microsoft.com/blog/2024/07/20/helping-our-customers-through-the-crowdstrike-outage/
- AWS. "Summary of the Amazon DynamoDB Service Disruption in the Northern Virginia (US-EAST-1) Region" (October 2025). https://aws.amazon.com/message/101925/
- Cloudflare. "Cloudflare outage on November 18, 2025" (November 2025). https://blog.cloudflare.com/18-november-2025-outage/
- Google SRE Book, "Postmortem Culture: Learning from Failure". https://sre.google/sre-book/postmortem-culture/
