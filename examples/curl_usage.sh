#!/bin/bash
# API Canon — curl + jq examples
# Download the DB once and query it with jq

DB_URL="https://raw.githubusercontent.com/shivtcdfinance/api-canon/main/api_canon.min.json"

echo "=== Downloading API Canon ($(curl -sI $DB_URL | grep content-length | awk '{printf "%.0f KB", $2/1024}')) ==="
curl -s $DB_URL -o /tmp/api_canon.json

echo ""
echo "=== 1. Count by trust rating ==="
jq 'group_by(.trust) | map({trust: .[0].trust, count: length})' /tmp/api_canon.json

echo ""
echo "=== 2. Find free HTTPS APIs for weather ==="
jq '.[] | select(.trust == "trusted" and .auth == "no" and .https == true and (.name | test("weather"; "i"))) | {name, url, domain}' /tmp/api_canon.json

echo ""
echo "=== 3. All finance APIs (any trust) ==="
jq '.[] | select(.cat == "finance") | {name, trust, auth, domain}' /tmp/api_canon.json | head -20

echo ""
echo "=== 4. Zero-auth, HTTPS, trusted APIs (count by category) ==="
jq '[.[] | select(.trust == "trusted" and .auth == "no" and .https == true)] | group_by(.cat) | map({cat: .[0].cat, count: length}) | sort_by(-.count)' /tmp/api_canon.json
