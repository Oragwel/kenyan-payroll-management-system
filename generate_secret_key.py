#!/usr/bin/env python3
"""
Generate a secure Django secret key for production deployment
"""

import secrets

def generate_secret_key():
    """Generate a secure secret key for Django"""
    return secrets.token_urlsafe(50)

if __name__ == "__main__":
    secret_key = generate_secret_key()
    print("=" * 60)
    print("🔐 DJANGO SECRET KEY GENERATED")
    print("=" * 60)
    print(f"SECRET_KEY={secret_key}")
    print("=" * 60)
    print("⚠️  IMPORTANT: Keep this secret key secure!")
    print("   - Do not commit it to version control")
    print("   - Add it to your Vercel environment variables")
    print("   - Use it only for production deployment")
    print("=" * 60)
