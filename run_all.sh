#!/bin/bash

# run_all.sh: Generate efficient frontiers for all files and modes
# This script runs all combinations:
# - 5 data files (port1.txt to port5.txt)
# - 2 modes (minimize_risk, maximize_return)
# Total: 10 frontier curves

echo "Starting efficient frontier generation for all files and modes..."
echo "==========================================================="

MODES=("minimize_risk")
FILES=("data/port1.txt")
 # MODES=("minimize_risk" "maximize_return")
# FILES=("data/port1.txt" "data/port2.txt" "data/port3.txt" "data/port4.txt" "data/port5.txt")

START_TIME=$(date +%s)

for FILE in "${FILES[@]}"; do
    for MODE in "${MODES[@]}"; do
        echo ""
        echo "Processing: $MODE with $FILE"
        echo "-------------------------------------------"
        ./gen_frontier.sh "$MODE" "$FILE"
    done
done

END_TIME=$(date +%s)
ELAPSED=$((END_TIME - START_TIME))

echo ""
echo "==========================================================="
echo "All frontiers generated successfully!"
echo "Time elapsed: ${ELAPSED}s"
echo "Results available in results/ directory:"
ls -lh results/
