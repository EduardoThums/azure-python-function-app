#!/bin/bash

# Script to dispatch GitHub workflow based on branch
# Requires environment variables: GITHUB_TOKEN, GITHUB_OWNER, GITHUB_REPO, BRANCH

set -e

# Check required environment variables
if [ -z "$GITHUB_TOKEN" ]; then
  echo "Error: GITHUB_TOKEN environment variable is not set"
  echo "Please set it with: export GITHUB_TOKEN=your_token_here"
  exit 1
fi

if [ -z "$GITHUB_OWNER" ]; then
  echo "Error: GITHUB_OWNER environment variable is not set"
  echo "Please set it with: export GITHUB_OWNER=your_github_username"
  exit 1
fi

if [ -z "$GITHUB_REPO" ]; then
  echo "Error: GITHUB_REPO environment variable is not set"
  echo "Please set it with: export GITHUB_REPO=your_repository_name"
  exit 1
fi

if [ -z "$BRANCH" ]; then
  echo "Error: BRANCH environment variable is not set (must be 'main' or 'stage')"
  echo "Please set it with: export BRANCH=main  # or stage"
  exit 1
fi

if [ "$BRANCH" != "main" ] && [ "$BRANCH" != "stage" ]; then
  echo "Error: BRANCH must be 'main' or 'stage'"
  exit 1
fi

# API endpoint
API_URL="https://api.github.com/repos/$GITHUB_OWNER/$GITHUB_REPO/actions/workflows/deploy.yml/dispatches"

# Payload
PAYLOAD='{
  "ref": "'$BRANCH'"
}'

# Make the API request
echo "Dispatching workflow on $BRANCH branch..."
response=$(curl -s -w "%{http_code}" -o /tmp/response.json \
  -X POST "$API_URL" \
  -H "Authorization: token $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  -H "Content-Type: application/json" \
  -d "$PAYLOAD")

# Check response status
case $response in
  204)
    echo "Success: Workflow dispatched successfully"
    ;;
  401)
    echo "Error: Unauthorized. Check your GITHUB_TOKEN"
    exit 1
    ;;
  403)
    echo "Error: Forbidden. Token may lack required permissions"
    exit 1
    ;;
  404)
    echo "Error: Repository or workflow not found"
    exit 1
    ;;
  422)
    echo "Error: Invalid payload or workflow configuration"
    exit 1
    ;;
  429)
    echo "Error: Rate limit exceeded. Please wait and try again"
    exit 1
    ;;
  *)
    echo "Error: Unexpected HTTP status $response"
    if [ -f /tmp/response.json ]; then
      echo "Response details:"
      cat /tmp/response.json
    fi
    exit 1
    ;;
esac