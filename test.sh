#!/usr/bin/env bash

curl -s localhost:8080 > /dev/null

if [ $? -ne 0 ]; then
    echo "❌ Server is not running"
    exit 1
fi

# helper function for fancy status outputs
printStatus() {
    if [ $? -eq 0 ]; then
        echo -n "✅ "
    else
        echo -n "❌ "
    fi
}

url='localhost:8080/good'
curl -sI $url  | grep -q '301 MOVED'
printStatus ; echo "$url should redirect"

url='localhost:8080/omg'
curl -sI $url | grep -q '200 OK'
printStatus ; echo "$url should not redirect"

url='localhost:8080/url'
curl -Ss -XPOST "$url" \
    -H 'Content-Type: application/json' \
    -H 'API-KEY: TEST-API-KEY' \
    -d '{"code": "omg", "url": "https://omg.com"}' | grep -q 'omg is now pointing to: https://omg.com'
printStatus ; echo "$url should POST and create 'omg' as a new short url"

url='localhost:8080/omg'
curl -sI $url | grep -q '301 MOVED'
printStatus ; echo "$url should redirect to https://omg.com"

url='localhost:8080/url/omg'
curl -Ss -XDELETE "$url" \
    -H 'Content-Type: application/json' \
    -H 'API-KEY: BAD-KEY-JUNK-HERE' | grep -q 'API-KEY is not valid'
printStatus ; echo "$url should not DELETE if API-KEY is incorrect"

curl -Ss -XDELETE "$url" \
    -H 'Content-Type: application/json' \
    -H 'API-KEY: TEST-API-KEY' | grep -q 'omg has been removed'
printStatus ; echo "$url should DELETE given valid API-KEY"

url='localhost:8080/omg'
curl -sI $url | grep -q '200 OK'
printStatus ; echo "$url should have been deleted and no longer redirect"
