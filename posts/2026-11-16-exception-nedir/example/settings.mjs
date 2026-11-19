import { mkdtempSync, readFileSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";

const dir = mkdtempSync(join(tmpdir(), "settings-"));
const missing = join(dir, "missing.json");
const corrupt = join(dir, "corrupt.json");
writeFileSync(corrupt, "{ theme: dark ");   // not valid JSON

// 1. Swallowing: C# `catch (Exception) { return null; }`
function loadSettingsSwallow(path) {
  try {
    return JSON.parse(readFileSync(path, "utf8"));
  } catch {
    return null; // the error is gone, nobody knows why
  }
}

// 2. Add meaning and rethrow: C# `throw new SettingsException("...", ex);` (never `throw ex;`)
function loadSettingsRethrow(path) {
  try {
    return JSON.parse(readFileSync(path, "utf8"));
  } catch (err) {
    throw new Error(`Could not load settings from ${path}`, { cause: err });
  }
}

// 3. Expected case as a return value, unexpected case as an exception
//    C#: if (!File.Exists(path)) return Defaults;  then let JsonException bubble up
const DEFAULTS = { theme: "light", lang: "tr" };
function loadSettingsOrDefault(path) {
  let text;
  try {
    text = readFileSync(path, "utf8");
  } catch (err) {
    if (err.code === "ENOENT") return DEFAULTS; // missing file is expected on first run
    throw err;                                  // permission denied etc.: not ours to hide
  }
  return JSON.parse(text);                      // corrupt file is a real problem: let it go up
}

console.log("1. swallow:");
const s = loadSettingsSwallow(corrupt);
try {
  console.log("   theme is", s.theme); // crashes HERE, far from the real cause
} catch (e) {
  console.log("   crashed later with:", e.message);
}

console.log("2. rethrow with cause:");
try {
  loadSettingsRethrow(corrupt);
} catch (e) {
  console.log("   ", e.message);
  console.log("    caused by:", e.cause.message);
}

console.log("3. default for the expected case:");
console.log("    missing file ->", loadSettingsOrDefault(missing));
try {
  loadSettingsOrDefault(corrupt);
} catch (e) {
  console.log("    corrupt file -> error goes up:", e.constructor.name);
}
