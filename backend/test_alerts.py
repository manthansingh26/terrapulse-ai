#!/usr/bin/env python3
"""
TerraPulse AI - Email Alert Test Script
=========================================
Tests the complete email alert system end-to-end.

Run this script to verify:
1. Database connection works
2. AlertHistory table exists/gets created
3. Email configuration is valid
4. Test email can be sent
5. Alert can be logged to database

Usage:
    python test_alerts.py

Requirements:
    - Backend .env file configured with SMTP credentials
    - Database running on localhost:5432
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from datetime import datetime
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.db.database import engine, Base, test_connection
from app.models.models import AlertHistory, EnvironmentalData
from app.core.email import send_alert_email

settings = get_settings()

# Colors for output
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"
BOLD = "\033[1m"


def print_header(text):
    print(f"\n{BOLD}{BLUE}{'='*60}{RESET}")
    # Remove emojis for Windows compatibility
    safe_text = text.replace("🧪", "[TEST]").replace("📊", "[SUMMARY]")
    print(f"{BOLD}{BLUE}{safe_text:^60}{RESET}")
    print(f"{BOLD}{BLUE}{'='*60}{RESET}\n")


def print_success(text):
    print(f"{GREEN}[PASS] {text}{RESET}")


def print_error(text):
    print(f"{RED}[FAIL] {text}{RESET}")


def print_warning(text):
    print(f"{YELLOW}[WARN] {text}{RESET}")


def print_info(text):
    print(f"{BLUE}[INFO] {text}{RESET}")


# Track test results
tests_passed = 0
tests_failed = 0


def run_test(name, test_func):
    global tests_passed, tests_failed
    print(f"\n{BOLD}Test: {name}{RESET}")
    try:
        result = test_func()
        if result:
            print_success(f"{name} - PASSED")
            tests_passed += 1
        else:
            print_error(f"{name} - FAILED")
            tests_failed += 1
    except Exception as e:
        print_error(f"{name} - ERROR: {e}")
        tests_failed += 1
    return result


# ============ TEST FUNCTIONS ============


def test_database_connection():
    """Test 1: Verify database connection"""
    print_info(f"Connecting to: {settings.DATABASE_URL.split('@')[1] if '@' in settings.DATABASE_URL else 'unknown'}")
    return test_connection()


def test_alert_history_table_exists():
    """Test 2: Verify AlertHistory table exists or gets created"""
    print_info("Checking for AlertHistory table...")

    # Create all tables (this will create AlertHistory if it doesn't exist)
    Base.metadata.create_all(bind=engine)

    # Verify table exists
    inspector = inspect(engine)
    tables = inspector.get_table_names()

    if "alert_history" in tables:
        print_info("Table 'alert_history' found")
        return True
    else:
        print_error("Table 'alert_history' NOT found")
        return False


def test_email_configuration():
    """Test 3: Verify email configuration is present"""
    print_info("Checking email configuration...")
    print_info(f"SMTP Host: {settings.SMTP_HOST}")
    print_info(f"SMTP Port: {settings.SMTP_PORT}")
    print_info(f"SMTP User: {settings.SMTP_USER or '(not set)'}")
    print_info(f"Alert Email: {settings.ALERT_EMAIL}")
    print_info(f"AQI Threshold: {settings.AQI_ALERT_THRESHOLD}")

    if not settings.SMTP_USER or not settings.SMTP_PASSWORD:
        print_warning("SMTP credentials not configured - email sending will fail")
        print_warning("Update backend/.env with SMTP_USER and SMTP_PASSWORD")
        return False

    return True


def test_send_email():
    """Test 4: Send a test email"""
    print_info(f"Sending test email to {settings.ALERT_EMAIL}...")

    result = send_alert_email(
        city="Test City",
        aqi_value=250,
        recipient=settings.ALERT_EMAIL
    )

    if result:
        print_success(f"Email sent successfully to {settings.ALERT_EMAIL}")
    else:
        print_error(f"Failed to send email to {settings.ALERT_EMAIL}")
        print_info("Check SMTP credentials in backend/.env")
        print_info("For Gmail, you need an 'App Password', not your regular password")

    return result


def test_log_alert_to_database():
    """Test 5: Log an alert to the database"""
    print_info("Creating test alert record in database...")

    db = Session(bind=engine)
    try:
        alert = AlertHistory(
            city="Test City",
            aqi_value=250,
            alert_type="test",
            email_sent=False,
            email_recipient=settings.ALERT_EMAIL,
            last_alert_time=datetime.utcnow()
        )
        db.add(alert)
        db.commit()
        db.refresh(alert)

        print_success(f"Alert record created with ID: {alert.id}")

        # Verify we can query it back
        retrieved = db.query(AlertHistory).filter(AlertHistory.id == alert.id).first()
        if retrieved:
            print_success(f"Alert record retrieved: City={retrieved.city}, AQI={retrieved.aqi_value}")
            return True
        return False
    finally:
        db.close()


def test_env_file_exists():
    """Test 6: Verify .env file exists"""
    env_path = os.path.join(os.path.dirname(__file__), ".env")
    if os.path.exists(env_path):
        print_success(f".env file found at {env_path}")
        return True
    else:
        print_error(f".env file NOT found at {env_path}")
        print_info("Create backend/.env with your configuration")
        return False


# ============ MAIN ============


def main():
    print_header("🧪 TerraPulse AI - Email Alert Test Suite")

    print_info(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print_info(f"Database: {settings.DATABASE_URL.split('@')[1] if '@' in settings.DATABASE_URL else 'unknown'}")

    # Run all tests
    run_test("1. Database Connection", test_database_connection)
    run_test("2. .env File Exists", test_env_file_exists)
    run_test("3. AlertHistory Table Exists", test_alert_history_table_exists)
    run_test("4. Email Configuration", test_email_configuration)
    run_test("5. Send Test Email", test_send_email)
    run_test("6. Log Alert to Database", test_log_alert_to_database)

    # Print summary
    print_header("📊 Test Summary")
    print(f"{GREEN}Passed: {tests_passed}{RESET}")
    print(f"{RED}Failed: {tests_failed}{RESET}")
    print(f"Total:  {tests_passed + tests_failed}\n")

    if tests_failed == 0:
        print_success("All tests passed! Email alert system is ready.")
        print("\n" + "="*60)
        print("NEXT STEPS:")
        print("="*60)
        print("1. Start backend: cd backend && python -m uvicorn app.main:app --reload")
        print("2. Test API endpoint:")
        print("   curl -X POST http://localhost:8000/api/alerts/test \\")
        print("     -H 'Content-Type: application/json' \\")
        print("     -d '{\"city\": \"Ahmedabad\", \"aqi_value\": 250}'")
        print("3. Check your email at:", settings.ALERT_EMAIL)
        print("="*60 + "\n")
        return 0
    else:
        print_error(f"{tests_failed} test(s) failed. Please fix the issues above.")
        print("\n" + "="*60)
        print("TROUBLESHOOTING:")
        print("="*60)
        if not test_env_file_exists():
            print("- Create backend/.env file (copy from .env.example)")
        if settings.SMTP_USER == "your-email@gmail.com" or not settings.SMTP_USER:
            print("- Update SMTP_USER in .env with your Gmail address")
        if settings.SMTP_PASSWORD == "your-app-password" or not settings.SMTP_PASSWORD:
            print("- Update SMTP_PASSWORD with Gmail App Password")
            print("  (Get it from: https://myaccount.google.com/apppasswords)")
        print("="*60 + "\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())
