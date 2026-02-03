#!/bin/bash
# Script to find companies for the 15 biggest cities in Europe for 2025
# With graceful error handling and appropriate sleep intervals

set -o pipefail

# Configuration
TIME_START="2025-01-01"
TIME_END="2025-12-31"
SLEEP_SUCCESS=60
SLEEP_ERROR=180

# 15 EU cities prioritized by tech summit activity and Erasmus internship popularity
CITIES=(
    "Berlin"        # Germany - major tech hub, strong Erasmus
    "Amsterdam"     # Netherlands - huge startup/tech scene
    "Paris"         # France - major tech conferences
    "Barcelona"     # Spain - tech summits, top Erasmus destination
    "Dublin"        # Ireland - tech company HQs
    "Lisbon"        # Portugal - Web Summit host, growing tech
    "Munich"        # Germany - tech hub
    "Madrid"        # Spain - tech scene, Erasmus popular
    "Stockholm"     # Sweden - strong startup ecosystem
    "Milan"         # Italy - tech/business hub
    "Vienna"        # Austria - central Europe tech hub
    "Copenhagen"    # Denmark - tech scene
    "Helsinki"      # Finland - tech hub
    "Warsaw"        # Poland - growing tech, Erasmus
    "Prague"        # Czech Republic - tech scene, Erasmus
)

# Counters for summary
SUCCESS_COUNT=0
ERROR_COUNT=0
FAILED_CITIES=()

echo "========================================"
echo "Starting company finder for European cities"
echo "Time range: $TIME_START to $TIME_END"
echo "Total cities: ${#CITIES[@]}"
echo "========================================"
echo ""

for i in "${!CITIES[@]}"; do
    CITY="${CITIES[$i]}"
    CITY_NUM=$((i + 1))
    
    echo "----------------------------------------"
    echo "[$CITY_NUM/${#CITIES[@]}] Processing: $CITY"
    echo "Started at: $(date '+%Y-%m-%d %H:%M:%S')"
    echo "----------------------------------------"
    
    # Run the command and capture exit status
    if python -m src.main "$CITY" "$TIME_START" "$TIME_END"; then
        echo "✓ Successfully processed: $CITY"
        ((SUCCESS_COUNT++))
        
        # Sleep between calls (except for the last city)
        if [ $CITY_NUM -lt ${#CITIES[@]} ]; then
            echo "Sleeping for $SLEEP_SUCCESS seconds before next city..."
            sleep $SLEEP_SUCCESS
        fi
    else
        echo "✗ Error processing: $CITY"
        ((ERROR_COUNT++))
        FAILED_CITIES+=("$CITY")
        
        # Longer sleep after error (except for the last city)
        if [ $CITY_NUM -lt ${#CITIES[@]} ]; then
            echo "Error occurred. Sleeping for $SLEEP_ERROR seconds before next city..."
            sleep $SLEEP_ERROR
        fi
    fi
    
    echo ""
done

# Print summary
echo "========================================"
echo "SUMMARY"
echo "========================================"
echo "Total cities processed: ${#CITIES[@]}"
echo "Successful: $SUCCESS_COUNT"
echo "Failed: $ERROR_COUNT"

if [ ${#FAILED_CITIES[@]} -gt 0 ]; then
    echo ""
    echo "Failed cities:"
    for CITY in "${FAILED_CITIES[@]}"; do
        echo "  - $CITY"
    done
fi

echo ""
echo "Completed at: $(date '+%Y-%m-%d %H:%M:%S')"
echo "========================================"

# Exit with error if any cities failed
if [ $ERROR_COUNT -gt 0 ]; then
    exit 1
fi

exit 0
