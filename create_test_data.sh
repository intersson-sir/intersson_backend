#!/bin/bash

# Script to create test data for frontend development
# Создание тестовых данных для разработки frontend

API_URL="http://localhost:8000/api"

echo "🎨 Creating test data for Phil Backend..."
echo ""

# Check if backend is running
if ! curl -s "$API_URL/links/" > /dev/null 2>&1; then
    echo "❌ Backend is not running!"
    echo "Please start backend first: ./start.sh"
    exit 1
fi

echo "✅ Backend is running"
echo ""

# Create test links
echo "📝 Creating test links..."

# Facebook links
curl -s -X POST "$API_URL/links/" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://facebook.com/fake-news-post-123",
    "platform": "facebook",
    "type": "post",
    "status": "active",
    "priority": "high",
    "manager": "John Doe",
    "notes": "Spreading misinformation about company"
  }' > /dev/null

curl -s -X POST "$API_URL/links/" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://facebook.com/negative-review-456",
    "platform": "facebook",
    "type": "comment",
    "status": "in_work",
    "priority": "medium",
    "manager": "Jane Smith",
    "notes": "Reviewing with legal team"
  }' > /dev/null

curl -s -X POST "$API_URL/links/" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://facebook.com/defamatory-post-789",
    "platform": "facebook",
    "type": "post",
    "status": "removed",
    "priority": "high",
    "manager": "John Doe",
    "notes": "Successfully removed by Facebook team"
  }' > /dev/null

# Twitter links
curl -s -X POST "$API_URL/links/" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://twitter.com/badactor/status/123456789",
    "platform": "twitter",
    "type": "post",
    "status": "active",
    "priority": "high",
    "manager": "Mike Johnson",
    "notes": "Viral negative tweet"
  }' > /dev/null

curl -s -X POST "$API_URL/links/" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://twitter.com/complaint/status/987654321",
    "platform": "twitter",
    "type": "comment",
    "status": "pending",
    "priority": "low",
    "notes": "Waiting for review"
  }' > /dev/null

# YouTube links
curl -s -X POST "$API_URL/links/" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://youtube.com/watch?v=abc123",
    "platform": "youtube",
    "type": "video",
    "status": "in_work",
    "priority": "high",
    "manager": "Sarah Williams",
    "notes": "Video contains false claims"
  }' > /dev/null

curl -s -X POST "$API_URL/links/" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://youtube.com/watch?v=xyz789",
    "platform": "youtube",
    "type": "video",
    "status": "removed",
    "priority": "medium",
    "manager": "Sarah Williams",
    "notes": "Removed by YouTube after DMCA"
  }' > /dev/null

# Reddit links
curl -s -X POST "$API_URL/links/" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://reddit.com/r/technology/comments/abc123",
    "platform": "reddit",
    "type": "post",
    "status": "active",
    "priority": "medium",
    "manager": "John Doe",
    "notes": "Negative discussion thread"
  }' > /dev/null

curl -s -X POST "$API_URL/links/" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://reddit.com/r/news/comments/xyz789",
    "platform": "reddit",
    "type": "comment",
    "status": "pending",
    "priority": "low",
    "notes": "Under review"
  }' > /dev/null

# Other platform
curl -s -X POST "$API_URL/links/" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://medium.com/@author/negative-article",
    "platform": "other",
    "type": "article",
    "status": "active",
    "priority": "high",
    "manager": "Jane Smith",
    "notes": "Long-form negative content"
  }' > /dev/null

echo "✅ Created 10 test links"
echo ""

# Get stats
echo "📊 Current statistics:"
curl -s "$API_URL/stats/dashboard/" | python3 -c "
import sys, json
data = json.load(sys.stdin)
print(f'  Total links: {data[\"total\"]}')
print(f'  Active: {data[\"active\"]}')
print(f'  In Work: {data[\"in_work\"]}')
print(f'  Removed: {data[\"removed\"]}')
print(f'  Pending: {data[\"pending\"]}')
"

echo ""
echo "✨ Test data created successfully!"
echo ""
echo "You can now:"
echo "  - View links: curl $API_URL/links/"
echo "  - View stats: curl $API_URL/stats/dashboard/"
echo "  - Open in browser: http://localhost:8000/api/links/"
