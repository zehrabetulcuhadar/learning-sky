// Weighted decision matrix: how should I host my personal site?
// Weights: how much each quality matters to me (sum does not need to be 1).
const weights = { cost: 5, speed: 4, dynamicFeatures: 1, maintenance: 4, learning: 2 };

// Scores: 1 (bad) to 5 (good) for each option.
const options = {
  "Static site on GitHub Pages": { cost: 5, speed: 5, dynamicFeatures: 1, maintenance: 5, learning: 3 },
  "Angular SPA + .NET API on a VPS": { cost: 2, speed: 3, dynamicFeatures: 5, maintenance: 2, learning: 4 },
  "Hosted blog platform": { cost: 4, speed: 4, dynamicFeatures: 3, maintenance: 5, learning: 1 },
};

const results = Object.entries(options)
  .map(([name, scores]) => ({
    name,
    total: Object.entries(weights).reduce((sum, [q, w]) => sum + w * scores[q], 0),
  }))
  .sort((a, b) => b.total - a.total);

for (const r of results) console.log(`${String(r.total).padStart(3)}  ${r.name}`);
console.log("\nThe winner depends on the weights. Change them and run again.");
