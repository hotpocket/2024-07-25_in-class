#!/usr/bin/env bash

echo
echo "--->verify static dict entries work"
curl -I localhost:8080/good

echo
echo "--->pre-add, verify what we are about to add does not exist"
curl -I localhost:8080/omg

echo
echo "---> POST: Create a new user"
curl -Ss -XPOST "localhost:8080/url" \
    -H 'Content-Type: application/json' \
    -d '{"code": "omg", "url": "https://omg.com"}'

echo
echo "---> verify it does exist"
curl -I localhost:8080/omg

echo
echo "--->DELETE: Remove a user - with a bad API KEY"
curl -Ss -XDELETE "localhost:8080/url/omg" \
    -H 'Content-Type: application/json' \
    -H 'API-KEY: BAD-KEY-JUNK-HERE'

echo
echo "--->DELETE: Remove a user - with a good API KEY"
curl -Ss -XDELETE "localhost:8080/url/omg" \
    -H 'Content-Type: application/json' \
    -H 'API-KEY: TEST-API-KEY'

echo
echo "--->verify it does not exist"
curl -I localhost:8080/omg
