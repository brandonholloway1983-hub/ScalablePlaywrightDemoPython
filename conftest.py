import pytest
from dotenv import load_dotenv
import os

load_dotenv()

# ─────────────────────────────────────────────────────────
# conftest.py — shared fixtures for the entire test suite
#
# This is the Python/PyTest equivalent of playwright.config.js
# Fixtures defined here are automatically available to any
# test function that requests them by name as a parameter.
# ─────────────────────────────────────────────────────────

@pytest.fixture(scope="session")
def base_url():
    return "https://opensource-demo.orangehrmlive.com"


@pytest.fixture(scope="session")
def credentials():
    return {
        "username": os.getenv("OHR_USERNAME"),
        "password": os.getenv("OHR_PASSWORD"),
    }


# Configure browser launch behavior
@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "viewport": {"width": 1280, "height": 720},
    }