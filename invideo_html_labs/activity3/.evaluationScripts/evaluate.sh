#!/bin/bash

# Define paths to the two scripts
SCRIPT1="/home/.evaluationScripts/images_eval/evaluate_0.sh"
SCRIPT2="/home/.evaluationScripts/multimedia_eval/evaluate_0.sh"

# Run the first script
#echo "Running script1..."
bash "$SCRIPT1"

sleep 1

# Run the second script
#echo "Running script2..."
bash "$SCRIPT2"

