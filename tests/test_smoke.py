import pytest
from pages.login_page import LoginPage
from pages.employee_list_page import EmployeeListPage

# ─────────────────────────────────────────────────────────
# Smoke Tests — Critical path
#
# Python/PyTest equivalent of smoke.spec.js
# Same coverage — login page loads, valid auth works,
# invalid auth blocked, employee list loads.
#
# Note: Python's is_visible() is a snapshot check, not an
# auto-retrying assertion like JavaScript's expect().toBeVisible().
# We explicitly wait_for() before asserting visibility.
# ─────────────────────────────────────────────────────────

@pytest.mark.smoke
def test_login_page_loads(page, base_url):
    login_page = LoginPage(page)
    login_page.page.goto(base_url + "/web/index.php/auth/login")

    assert "auth/login" in page.url

    login_page.username_field.wait_for(state="visible", timeout=10000)
    login_page.password_field.wait_for(state="visible", timeout=10000)
    login_page.login_button.wait_for(state="visible", timeout=10000)

    assert login_page.username_field.is_visible()
    assert login_page.password_field.is_visible()
    assert login_page.login_button.is_visible()

    print("✓ Login page loaded and fields visible")


@pytest.mark.smoke
def test_valid_credentials_authenticate(page, base_url, credentials):
    login_page = LoginPage(page)
    login_page.page.goto(base_url + "/web/index.php/auth/login")
    login_page.login_with_credentials(credentials)
    login_page.verify_login_successful()

    assert "dashboard" in page.url
    print("✓ Login successful — landed on dashboard")


@pytest.mark.smoke
def test_invalid_credentials_show_error(page, base_url):
    login_page = LoginPage(page)
    login_page.page.goto(base_url + "/web/index.php/auth/login")
    login_page.login_expecting_failure("invalid_user", "wrong_password")

    error = login_page.get_error_message()
    assert error

    print(f"✓ Invalid login correctly blocked — message: {error}")


@pytest.mark.smoke
def test_employee_list_loads_after_login(page, base_url, credentials):
    login_page = LoginPage(page)
    employee_list = EmployeeListPage(page)

    login_page.page.goto(base_url + "/web/index.php/auth/login")
    login_page.login_with_credentials(credentials)
    employee_list.goto()

    count = employee_list.get_record_count()
    assert count is not None
    assert count > 0

    print(f"✓ Employee list loaded — {count} records found")