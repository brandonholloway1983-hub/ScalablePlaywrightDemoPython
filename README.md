# ScalablePlaywrightDemoPython

A Python/PyTest port of [ScalablePlaywrightDemo](https://github.com/brandonholloway1983-hub/ScalablePlaywrightDemo) — built to demonstrate the same Page Object Model architecture, testing patterns, and CI practices in Python rather than JavaScript.

Built against OrangeHRM, an enterprise HR management system used as an analog for complex, data-heavy enterprise applications.

---

## Why This Exists

The original ScalablePlaywrightDemo was built in JavaScript. This version mirrors the same architecture, selectors, and test coverage in Python using PyTest — demonstrating that the underlying testing concepts (Page Object Model, fixtures, tagged execution, CI gating) transfer directly between languages. Only the syntax changes.

---

## Framework Architecture

    ScalablePlaywrightDemoPython/
      pages/
        base_page.py           # Foundation — all page objects inherit from here
        login_page.py          # Authentication flows
        employee_list_page.py  # Search, filter, table, row actions
      tests/
        test_smoke.py           # Critical path gate tests
        test_employee_list.py   # Full workflow regression coverage
      conftest.py                # Shared fixtures — equivalent to playwright.config.js
      pytest.ini                 # Marker registration
      .github/workflows/
        pytest.yml               # Two-stage CI — smoke gates regression

---

## Key Differences from the JavaScript Version

| Concept | JavaScript | Python |
|---------|-----------|--------|
| Inheritance | `class LoginPage extends BasePage` | `class LoginPage(BasePage):` |
| Constructor | `constructor(page) { super(page); }` | `def __init__(self, page): super().__init__(page)` |
| Async | `await element.click()` | `element.click()` — sync API, no await |
| Tags | `{ tag: ['@smoke'] }` | `@pytest.mark.smoke` |
| Setup/teardown | `test.beforeEach()` | Fixtures (`@pytest.fixture`) |
| Config | `playwright.config.js` | `conftest.py` + `pytest.ini` |
| Package manager | npm | pip |

---

## Tag Strategy

| Marker | Purpose |
|--------|---------|
| `@pytest.mark.smoke` | Critical path gate — runs first |
| `@pytest.mark.regression` | Full suite |
| `@pytest.mark.critical` | Highest priority within regression |

```bash
# Run smoke only
pytest tests/test_smoke.py -m smoke -v

# Run regression only
pytest tests/test_employee_list.py -m regression -v
```

---

## CI Pipeline

Two-stage GitHub Actions workflow — smoke gates regression, same pattern as the JavaScript version. Runs on every push and pull request to main.

---

## Setup

```bash
# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate          # Windows
source venv/bin/activate       # Mac/Linux

# Install dependencies
pip install pytest-playwright python-dotenv
playwright install chromium

# Configure environment
# Create .env with OHR_USERNAME and OHR_PASSWORD

# Run tests
pytest tests/test_smoke.py -m smoke -v
pytest tests/test_employee_list.py -m regression -v
```

### GitHub Secrets required for CI
- `OHR_USERNAME`
- `OHR_PASSWORD`

---

## Related

See [ScalablePlaywrightDemo](https://github.com/brandonholloway1983-hub/ScalablePlaywrightDemo) for the original JavaScript implementation with additional features including an AI-powered failure analyzer, storageState authentication, and API/UI cross-validation tests.