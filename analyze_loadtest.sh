#!/bin/bash
# Load Test Results Analyzer (CSV format)

echo "═══════════════════════════════════════════════════════════"
echo "  JMeter Load Test Results Analysis"
echo "═══════════════════════════════════════════════════════════"
echo ""

JTL_FILE="${1:-results/loadtest_standard.jtl}"

if [ ! -f "$JTL_FILE" ]; then
    echo "❌ Error: File not found: $JTL_FILE"
    exit 1
fi

echo "📁 Results File: $JTL_FILE"
echo ""

# Skip header and count total lines
TOTAL=$(($(wc -l < "$JTL_FILE") - 1))
echo "📊 Total Samples: $TOTAL"

# Count passed (success=true)
PASSED=$(grep 'true' "$JTL_FILE" | wc -l)
echo "✅ Passed: $PASSED"

# Count failed (success=false)
FAILED=$(grep 'false' "$JTL_FILE" | wc -l)
echo "❌ Failed: $FAILED"

# Calculate error rate
if [ $TOTAL -gt 0 ]; then
    ERROR_RATE=$(awk "BEGIN {printf \"%.2f\", ($FAILED / $TOTAL) * 100}")
    PASS_RATE=$(awk "BEGIN {printf \"%.2f\", ($PASSED / $TOTAL) * 100}")
    echo "⚠️  Error Rate: ${ERROR_RATE}%"
    echo "✅ Pass Rate: ${PASS_RATE}%"
fi

echo ""
echo "─────────────────────────────────────────────────────────────"

# Get unique failure messages
echo ""
echo "🔍 Failure Analysis:"
grep 'false' "$JTL_FILE" | cut -d',' -f4 | sort | uniq -c | head -3 | while read count error; do
    echo "   • $error (Count: $count)"
done

echo ""
echo "─────────────────────────────────────────────────────────────"

# Test status
if [ "$ERROR_RATE" = "100.00" ] || [ "$ERROR_RATE" = "100" ]; then
    echo ""
    echo "🔴 TEST STATUS: FAILED"
    echo "   Error Rate: 100% - All requests failed"
    echo "   Likely Cause: Variable substitution issue or server connectivity"
elif [ "${ERROR_RATE%.*}" -gt 5 ]; then
    echo ""
    echo "🔴 TEST STATUS: FAILED"
    echo "   Error Rate: > 5%"
elif [ "${ERROR_RATE%.*}" -gt 1 ]; then
    echo ""
    echo "🟡 TEST STATUS: MARGINAL"
    echo "   Error Rate: 1-5%"
else
    echo ""
    echo "🟢 TEST STATUS: PASSED"
    echo "   Error Rate: < 1%"
fi

echo "═══════════════════════════════════════════════════════════"
