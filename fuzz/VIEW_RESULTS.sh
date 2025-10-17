#!/bin/bash
# Quick script to view all results

echo "======================================"
echo "FUZZ TESTING PIPELINE RESULTS"
echo "======================================"
echo ""

echo "Step 1: Grammar Evaluation"
echo "---"
if [ -f fuzz/experiments/step1_results/summary.json ]; then
    python3 -c "
import json
with open('fuzz/experiments/step1_results/summary.json') as f:
    data = json.load(f)
for g in data['grammars']:
    print(f\"  {g['display_name']:30s}: {g['compiled_count']:2d}/{g['generated_count']:2d} ({g['success_rate']:.1f}%)\")
"
else
    echo "  Not yet run"
fi
echo ""

echo "Step 2: Complex Code Generation"
echo "---"
if [ -f fuzz/experiments/step2_results/results.json ]; then
    python3 -c "
import json
with open('fuzz/experiments/step2_results/results.json') as f:
    data = json.load(f)
print(f\"  Generated: {data['generated']}  Compiled: {data['compiled']}  Success: {data['success_rate']:.1f}%\")
"
else
    echo "  Not yet run"
fi
echo ""

echo "Step 3: Maximum Complexity"
echo "---"
if [ -f fuzz/experiments/step3_results/results.json ]; then
    python3 -c "
import json
with open('fuzz/experiments/step3_results/results.json') as f:
    data = json.load(f)
print(f\"  Generated: {data['generated']}  Compiled: {data['compiled']}  Success: {data['success_rate']:.1f}%\")
"
else
    echo "  Not yet run"
fi
echo ""

echo "Step 4: Differential Fuzzing (2.2.20 vs 2.0.0)"
echo "---"
if [ -f fuzz/experiments/step4_results/summary.json ]; then
    python3 -c "
import json
with open('fuzz/experiments/step4_results/summary.json') as f:
    data = json.load(f)
s = data['statistics']
print(f\"  Tests Generated: {s['generated']}\")
print(f\"  Both Compiled:   {s['both_compiled']}\")
print(f\"  Outputs Match:   {s['output_match']}\")
print(f\"  Outputs Differ:  {s['output_differ']}\")
print(f\"  Failures Saved:  {s['failures_saved']}\")
"
else
    echo "  Not yet run"
fi
echo ""

echo "======================================"
echo "Example files available in: fuzz/examples/"
echo "Full results in: fuzz/experiments/"
echo "======================================"
