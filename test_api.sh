#!/bin/bash

# Test script for Phil Backend API
# This script tests all endpoints to ensure they work correctly

BASE_URL="http://localhost:8000/api"

echo "🧪 Testing Phil Backend API"
echo "=============================="
echo ""

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

test_endpoint() {
    local method=$1
    local endpoint=$2
    local data=$3
    local description=$4
    
    echo -n "Testing: $description... "
    
    if [ "$method" = "GET" ]; then
        response=$(curl -s -w "\n%{http_code}" "$BASE_URL$endpoint")
    elif [ "$method" = "POST" ]; then
        response=$(curl -s -w "\n%{http_code}" -X POST "$BASE_URL$endpoint" \
            -H "Content-Type: application/json" \
            -d "$data")
    elif [ "$method" = "PATCH" ]; then
        response=$(curl -s -w "\n%{http_code}" -X PATCH "$BASE_URL$endpoint" \
            -H "Content-Type: application/json" \
            -d "$data")
    elif [ "$method" = "DELETE" ]; then
        response=$(curl -s -w "\n%{http_code}" -X DELETE "$BASE_URL$endpoint")
    fi
    
    http_code=$(echo "$response" | tail -n1)
    
    if [ "$http_code" -ge 200 ] && [ "$http_code" -lt 300 ]; then
        echo -e "${GREEN}✓ PASS${NC} (HTTP $http_code)"
    else
        echo -e "${RED}✗ FAIL${NC} (HTTP $http_code)"
    fi
}

# Test 1: Get all links (should work even if empty)
test_endpoint "GET" "/links/" "" "GET all links"

# Test 2: Create a new link
echo ""
echo "Creating test links..."
CREATE_DATA='{
  "url": "https://facebook.com/test-negative-post",
  "platform": "facebook",
  "type": "post",
  "status": "active",
  "priority": "high",
  "manager": "John Doe",
  "notes": "Test link"
}'

response=$(curl -s -X POST "$BASE_URL/links/" \
    -H "Content-Type: application/json" \
    -d "$CREATE_DATA")

LINK_ID=$(echo "$response" | grep -o '"id":"[^"]*"' | head -1 | cut -d'"' -f4)

if [ ! -z "$LINK_ID" ]; then
    echo -e "${GREEN}✓${NC} Link created with ID: $LINK_ID"
else
    echo -e "${RED}✗${NC} Failed to create link"
    echo "Response: $response"
fi

echo ""

# Test 3: Get single link
if [ ! -z "$LINK_ID" ]; then
    test_endpoint "GET" "/links/$LINK_ID/" "" "GET single link"
fi

# Test 4: Update link
if [ ! -z "$LINK_ID" ]; then
    UPDATE_DATA='{"status": "in_work", "notes": "Updated via test"}'
    test_endpoint "PATCH" "/links/$LINK_ID/" "$UPDATE_DATA" "PATCH update link"
fi

# Test 5: Filters
test_endpoint "GET" "/links/?platform=facebook" "" "Filter by platform"
test_endpoint "GET" "/links/?status=active" "" "Filter by status"
test_endpoint "GET" "/links/?priority=high" "" "Filter by priority"
test_endpoint "GET" "/links/?search=facebook" "" "Search filter"

# Test 6: Bulk operations
if [ ! -z "$LINK_ID" ]; then
    echo ""
    echo "Testing bulk operations..."
    
    BULK_STATUS_DATA="{\"ids\": [\"$LINK_ID\"], \"status\": \"removed\"}"
    test_endpoint "POST" "/links/bulk-update-status/" "$BULK_STATUS_DATA" "Bulk update status"
    
    BULK_MANAGER_DATA="{\"ids\": [\"$LINK_ID\"], \"manager\": \"Jane Smith\"}"
    test_endpoint "POST" "/links/bulk-assign-manager/" "$BULK_MANAGER_DATA" "Bulk assign manager"
fi

# Test 7: Statistics
echo ""
echo "Testing statistics endpoints..."
test_endpoint "GET" "/stats/dashboard/" "" "Dashboard statistics"
test_endpoint "GET" "/stats/platform/facebook/" "" "Platform statistics"

# Test 8: Cleanup - Delete test link
if [ ! -z "$LINK_ID" ]; then
    echo ""
    test_endpoint "DELETE" "/links/$LINK_ID/" "" "DELETE link"
fi

echo ""
echo "=============================="
echo "✅ API Tests Complete!"
echo ""
echo "💡 Tips:"
echo "   - Check detailed responses with: curl http://localhost:8000/api/links/ | jq"
echo "   - View API in browser: http://localhost:8000/api/"
echo "   - See API_EXAMPLES.md for more examples"
