// A service reloads a generated "feature file" every tick.
// On tick 4 a bug upstream duplicates every row, so the file doubles in size.
const LIMIT = 200;
const mode = process.argv[2] ?? "resilient";

function generateFeatureFile(tick) {
  const features = Array.from({ length: 120 }, (_, i) => `feature-${i}`);
  return tick >= 4 ? [...features, ...features] : features; // duplicated rows: 240 > LIMIT
}

function validate(features) {
  if (features.length > LIMIT) throw new Error(`feature file has ${features.length} entries, limit is ${LIMIT}`);
  if (new Set(features).size !== features.length) throw new Error("feature file has duplicate entries");
  return features;
}

let active = validate(generateFeatureFile(0));

for (let tick = 1; tick <= 6; tick++) {
  const candidate = generateFeatureFile(tick);
  if (mode === "fragile") {
    active = validate(candidate); // throws on tick 4 and the whole service stops
  } else {
    try {
      active = validate(candidate);
    } catch (e) {
      console.warn(`tick ${tick}: rejected new config (${e.message}), keeping last known good`);
    }
  }
  console.log(`tick ${tick}: serving traffic with ${active.length} features`);
}
console.log("service still running ✓");
