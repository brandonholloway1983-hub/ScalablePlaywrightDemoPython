import pytest
import re
from pages.login_page import LoginPage
from pages.employee_list_page import EmployeeListPage

# ─────────────────────────────────────────────────────────
# Regression — Employee List
#
# Python/PyTest equivalent of employeeList.spec.js
# Table structure, record counts, search behavior, reset.
# ─────────────────────────────────────────────────────────

@pytest.fixture
def logged_in_page(page, base_url, credentials):
    """Fixture that logs in before each regression test.
    Equivalent to beforeEach in the JS test files."""
    login_page = LoginPage(page)
    login_page.page.goto(base_url + "/web/index.php/auth/login")
    login_page.login_with_credentials(credentials)
    return page


@pytest.mark.regression
@pytest.mark.critical
def test_employee_list_renders_correct_columns(logged_in_page):
    employee_list = EmployeeListPage(logged_in_page)
    employee_list.goto()

    expected_columns = [
        "Id",
        "First (& Middle) Name",
        "Last Name",
        "Job Title",
        "Employment Status",
        "Sub Unit",
        "Supervisor",
        "Actions",
    ]

    for column in expected_columns:
        header = logged_in_page.locator(".oxd-table-th").filter(
            has=logged_in_page.locator(f"text=\"{column}\"")
        ).first
        header.wait_for(state="visible", timeout=5000)

    print(f"✓ All {len(expected_columns)} columns present")


@pytest.mark.regression
@pytest.mark.critical
def test_employee_list_shows_record_count(logged_in_page):
    employee_list = EmployeeListPage(logged_in_page)
    employee_list.goto()

    count = employee_list.get_record_count()

    assert count is not None
    assert count > 0

    print(f"✓ Records found count displayed: {count}")


@pytest.mark.regression
def test_visible_row_count_matches_page_size(logged_in_page):
    employee_list = EmployeeListPage(logged_in_page)
    employee_list.goto()

    record_count = employee_list.get_record_count()
    visible_rows = employee_list.get_visible_row_count()

    expected_visible = min(record_count, 50)
    assert visible_rows == expected_visible

    print(f"✓ Visible rows ({visible_rows}) matches expected page size")


@pytest.mark.regression
@pytest.mark.critical
def test_search_by_employee_id_returns_match(logged_in_page):
    employee_list = EmployeeListPage(logged_in_page)
    employee_list.goto()

    first_row = employee_list.table_rows.first
    id_cell = first_row.locator(".oxd-table-cell").nth(1)
    target_id = id_cell.inner_text().strip()

    employee_list.search_by_employee_id(target_id)

    count = employee_list.get_record_count()
    assert count >= 1

    row = employee_list.get_row_by_id(target_id)
    row.wait_for(state="visible", timeout=10000)

    print(f"✓ Search by ID '{target_id}' returned matching record")


@pytest.mark.regression
def test_search_with_no_results_shows_zero(logged_in_page):
    employee_list = EmployeeListPage(logged_in_page)
    employee_list.goto()

    employee_list.search_by_employee_id("ZZZZ99999")
    logged_in_page.wait_for_timeout(1000)

    count = employee_list.get_record_count()
    assert count == 0

    print("✓ No results search correctly shows 0 records")


@pytest.mark.regression
@pytest.mark.critical
def test_reset_restores_full_list(logged_in_page):
    employee_list = EmployeeListPage(logged_in_page)
    employee_list.goto()

    baseline_count = employee_list.get_record_count()

    employee_list.search_by_employee_id("ZZZZ99999")
    logged_in_page.wait_for_timeout(1000)

    filtered_count = employee_list.get_record_count()
    assert filtered_count == 0

    employee_list.reset_search()

    restored_count = employee_list.get_record_count()
    assert restored_count == baseline_count

    print(f"✓ Reset restored full list — {restored_count} records")