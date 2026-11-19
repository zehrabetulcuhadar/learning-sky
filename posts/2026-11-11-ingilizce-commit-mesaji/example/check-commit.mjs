#!/usr/bin/env node
// Checks a commit message against common English commit conventions.
import { existsSync, readFileSync } from "node:fs";

const arg = process.argv[2] ?? "";
const message = existsSync(arg) ? readFileSync(arg, "utf8") : arg;
const lines = message.split("\n").filter((l) => !l.startsWith("#"));
const subject = (lines[0] ?? "").trim();
// Allow an optional Conventional Commits prefix like "feat:" or "fix(ui):"
const text = subject.replace(/^[a-z]+(\([^)]*\))?!?:\s*/, "");
const firstWord = text.split(/\s+/)[0] ?? "";
const problems = [];

if (!subject) problems.push("The subject is empty.");
if (subject.length > 72) problems.push(`Subject is ${subject.length} chars, keep it near 50 (hard limit 72).`);
else if (subject.length > 50) problems.push(`Subject is ${subject.length} chars, try to stay near 50.`);
if (text === subject && /^[a-z]/.test(subject)) problems.push("Start the subject with a capital letter.");
if (/\.$/.test(subject)) problems.push("Do not end the subject with a period.");
if (/ed$/i.test(firstWord) && !/^(need|embed|feed|seed|speed|shred)$/i.test(firstWord))
  problems.push(`"${firstWord}" looks like past tense. Use the imperative ("Add", not "Added"): "If applied, this commit will ..."`);
if (/ing$/i.test(firstWord) && !/^(bring|string)$/i.test(firstWord)) problems.push(`"${firstWord}" ends in -ing. Use the imperative.`);
if (/^(update|fix|changes?|wip|stuff|misc)$/i.test(text)) problems.push("Too vague. Say what changed and where.");
if (lines.length > 1 && lines[1].trim() !== "") problems.push("Leave a blank line between the subject and the body.");

if (problems.length) {
  console.log(`✗ "${subject}"`);
  for (const p of problems) console.log("  - " + p);
  process.exit(1);
}
console.log(`✓ "${subject}" reads well: "If applied, this commit will ${text[0].toLowerCase() + text.slice(1)}"`);
