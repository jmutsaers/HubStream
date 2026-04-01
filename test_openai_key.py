"""
Test OpenAI API key and quota
"""
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    print("❌ No API key found in .env file")
    exit(1)

print(f"API Key found: {api_key[:20]}...")
print("\nTesting OpenAI Connection...")

try:
    client = OpenAI(api_key=api_key)
    
    # Try a simple API call
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": "Say 'Hello' only."}
        ],
        max_tokens=10
    )
    
    print("✅ API Key is VALID and WORKING!")
    print(f"✅ Response: {response.choices[0].message.content}")
    print("\n📊 Account Status: ✅ HAS QUOTA AVAILABLE")
    
except Exception as e:
    error_str = str(e)
    print(f"❌ Error: {error_str}")
    
    if "insufficient_quota" in error_str:
        print("\n⚠️  QUOTA ISSUE DETECTED")
        print("Solutions:")
        print("1. Check OpenAI billing: https://platform.openai.com/account/billing/overview")
        print("2. Verify your plan is PAID (not free trial)")
        print("3. Check if you have available credits/balance")
        print("4. Make sure the API key belongs to the account with paid plan")
    
    elif "invalid_api_key" in error_str:
        print("\n⚠️  INVALID API KEY")
        print("Solutions:")
        print("1. Get a NEW API key from: https://platform.openai.com/account/api-keys")
        print("2. Make sure you're using the CURRENT key (not an old/revoked one)")
        print("3. Copy the FULL key including 'sk-proj-' prefix")
    
    elif "401" in error_str or "Incorrect API" in error_str:
        print("\n⚠️  AUTHENTICATION FAILED")
        print("The API key is invalid or expired")
    
    else:
        print("\n⚠️  OTHER ERROR - Check internet connection and OpenAI status")
