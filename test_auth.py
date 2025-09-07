#!/usr/bin/env python3
"""
Test authentication endpoints
Run this to verify authentication is working correctly
"""

import requests
import json
import sys

# Configuration
BASE_URL = "https://compliance-server-ly2j.onrender.com"
# For local testing, use: BASE_URL = "http://localhost:8000"

def test_endpoints():
    """Test various endpoints"""
    print("🚀 Testing authentication endpoints...")
    
    # Test 1: Ping endpoint
    print("\n1. Testing ping endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/ping")
        if response.status_code == 200:
            print("✅ Ping endpoint working")
            print(f"   Response: {response.json()}")
        else:
            print(f"❌ Ping endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Ping endpoint error: {e}")
    
    # Test 2: Health endpoint
    print("\n2. Testing health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✅ Health endpoint working")
            health_data = response.json()
            print(f"   Database: {health_data.get('database', 'unknown')}")
            print(f"   Environment: {health_data.get('environment', 'unknown')}")
        else:
            print(f"❌ Health endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Health endpoint error: {e}")
    
    # Test 3: Test auth endpoint
    print("\n3. Testing auth info endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/test-auth")
        if response.status_code == 200:
            print("✅ Auth info endpoint working")
            auth_data = response.json()
            print(f"   Demo credentials available: {list(auth_data.get('demo_credentials', {}).keys())}")
        else:
            print(f"❌ Auth info endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Auth info endpoint error: {e}")
    
    # Test 4: Login with admin credentials
    print("\n4. Testing admin login...")
    try:
        login_data = {"username": "admin", "password": "admin123"}
        response = requests.post(
            f"{BASE_URL}/api/v1/auth/login-json",
            json=login_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            print("✅ Admin login successful")
            token_data = response.json()
            print(f"   Token type: {token_data.get('token_type')}")
            print(f"   Access token: {token_data.get('access_token', '')[:20]}...")
            
            # Test 5: Get current user with token
            print("\n5. Testing get current user...")
            headers = {"Authorization": f"Bearer {token_data.get('access_token')}"}
            user_response = requests.get(f"{BASE_URL}/api/v1/auth/me", headers=headers)
            
            if user_response.status_code == 200:
                print("✅ Get current user successful")
                user_data = user_response.json()
                print(f"   Username: {user_data.get('username')}")
                print(f"   Email: {user_data.get('email')}")
                print(f"   Role: {user_data.get('role')}")
            else:
                print(f"❌ Get current user failed: {user_response.status_code}")
                print(f"   Response: {user_response.text}")
        else:
            print(f"❌ Admin login failed: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ Admin login error: {e}")
    
    # Test 6: Login with demo credentials
    print("\n6. Testing demo login...")
    try:
        login_data = {"username": "demo", "password": "demo123"}
        response = requests.post(
            f"{BASE_URL}/api/v1/auth/login-json",
            json=login_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            print("✅ Demo login successful")
            token_data = response.json()
            print(f"   Token type: {token_data.get('token_type')}")
        else:
            print(f"❌ Demo login failed: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ Demo login error: {e}")
    
    # Test 7: Test invalid credentials
    print("\n7. Testing invalid credentials...")
    try:
        login_data = {"username": "invalid", "password": "invalid"}
        response = requests.post(
            f"{BASE_URL}/api/v1/auth/login-json",
            json=login_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 401:
            print("✅ Invalid credentials properly rejected")
            print(f"   Error message: {response.json().get('detail', 'No detail')}")
        else:
            print(f"❌ Invalid credentials not properly handled: {response.status_code}")
    except Exception as e:
        print(f"❌ Invalid credentials test error: {e}")

if __name__ == "__main__":
    test_endpoints()
    print("\n🎉 Authentication testing completed!")
