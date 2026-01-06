#!/bin/bash

# gen_frontier.sh: Generate efficient frontier for a specific mode and data file
# Usage: ./gen_frontier.sh <mode> <data_file>
# Example: ./gen_frontier.sh minimize_risk data/port1.txt

MODE=$1
DATA_FILE=$2

if [ -z "$MODE" ] || [ -z "$DATA_FILE" ]; then
    echo "Usage: $0 <mode> <data_file>"
    echo "Example: $0 minimize_risk data/port1.txt"
    exit 1
fi

# Validate mode
if [ "$MODE" != "minimize_risk" ] && [ "$MODE" != "maximize_return" ]; then
    echo "Error: mode must be 'minimize_risk' or 'maximize_return'"
    exit 1
fi

# Validate file exists
if [ ! -f "$DATA_FILE" ]; then
    echo "Error: file $DATA_FILE not found"
    exit 1
fi

# PSO parameters
N_SWARM=100
ITER=200
C1=1.7
C2=1.7
NUM_POINTS=25

echo "Generating frontier for mode=$MODE, file=$DATA_FILE"

# Get limits based on mode
if [ "$MODE" = "minimize_risk" ]; then
    # Need return limits
    LIMITS=$(python3 main.py --limits_return "$DATA_FILE" 2>/dev/null | grep -E "L_INF|L_SUP")
    TARGET_TYPE="return"
else
    # Need risk limits
    LIMITS=$(python3 main.py --limits_risk "$DATA_FILE" 2>/dev/null | grep -E "L_INF|L_SUP")
    TARGET_TYPE="risk"
fi

# Parse limits
L_INF=$(echo "$LIMITS" | grep "L_INF" | awk -F= '{print $2}')
L_SUP=$(echo "$LIMITS" | grep "L_SUP" | awk -F= '{print $2}')

if [ -z "$L_INF" ] || [ -z "$L_SUP" ]; then
    echo "Error: could not parse limits"
    exit 1
fi

echo "Target $TARGET_TYPE limits: $L_INF to $L_SUP"

# Calculate step
STEP=$(echo "scale=10; ($L_SUP - $L_INF) / ($NUM_POINTS - 1)" | bc)

# Clear previous results for this combination
PORTFOLIO_NUM=$(basename "$DATA_FILE" .txt | sed 's/port//')
if [ "$MODE" = "minimize_risk" ]; then
    FILENAME="results/min_return_p${PORTFOLIO_NUM}.csv"
else
    FILENAME="results/max_risk_p${PORTFOLIO_NUM}.csv"
fi

if [ -f "$FILENAME" ]; then
    rm "$FILENAME"
fi

echo "Running $NUM_POINTS PSO optimizations..."

# Run PSO for each point in the frontier
CURRENT=$(echo "$L_INF" | bc)
COUNT=1

while (( $(echo "$CURRENT <= $L_SUP" | bc -l) )); do
    echo "  [$COUNT/$NUM_POINTS] Target=$CURRENT"
    
    python3 main.py \
        --mode "$MODE" \
        --target_value "$CURRENT" \
        --n_swarm $N_SWARM \
        --iter $ITER \
        --C1 $C1 \
        --C2 $C2 \
        --save-result \
        "$DATA_FILE" > /dev/null 2>&1
    
    CURRENT=$(echo "$CURRENT + $STEP" | bc)
    ((COUNT++))
done

echo "Done! Results saved to $FILENAME"
