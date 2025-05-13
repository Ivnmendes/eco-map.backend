#!/bin/bash

API_URL="http://localhost:8000/api"

EMAIL="teste@example.com"
PASSWORD="SenhaForte123"
FIRST_NAME="João"
LAST_NAME="Silva"

echo "1. Registrando usuário..."
RESPONSE=$(curl -s -X POST "$API_URL/accounts/register/" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "'"$EMAIL"'",
    "password": "'"$PASSWORD"'",
    "confirm_password": "'"$PASSWORD"'",
    "first_name": "'"$FIRST_NAME"'",
    "last_name": "'"$LAST_NAME"'"
  }')

echo "Resposta bruta:"
echo "$RESPONSE"
echo "$RESPONSE" | jq .

echo -e "\n2. Logando usuário..."
LOGIN_RESPONSE=$(curl -s -X POST "$API_URL/accounts/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "'"$EMAIL"'",
    "password": "'"$PASSWORD"'"
  }')

echo "Resposta bruta do login:"
echo "$LOGIN_RESPONSE"

ACCESS=$(echo "$LOGIN_RESPONSE" | jq -r '.access')
REFRESH=$(echo "$LOGIN_RESPONSE" | jq -r '.refresh')

echo "Access Token: $ACCESS"
echo "Refresh Token: $REFRESH"

echo -e "\n3. Testando refresh..."
REFRESH_RESPONSE=$(curl -s -X POST "$API_URL/accounts/token/refresh/" \
  -H "Content-Type: application/json" \
  -d '{
    "refresh": $ACCESS
  }')

echo "Resposta bruta do refresh:"
echo "$REFRESH_RESPONSE"
echo "$REFRESH_RESPONSE" | jq .

echo -e "\n4. Logout (blacklist do refresh token)..."
LOGOUT_RESPONSE=$(curl -s -X POST "$API_URL/accounts/logout/" \
  -H "Authorization: Bearer $ACCESS"\
  -H "Content-Type: application/json" \
  -d '{
    "refresh": "'"$REFRESH"'"
  }')

echo "Resposta bruta do logout:"
echo "$LOGOUT_RESPONSE"
echo "$LOGOUT_RESPONSE" | jq .
