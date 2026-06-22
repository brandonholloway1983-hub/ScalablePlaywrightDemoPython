# ─────────────────────────────────────────────────────────
# BasePage — Foundation for all page objects
#
# Python equivalent of BasePage.js
# Same architecture, same purpose — shared patterns that
# every page object inherits, so common behavior is
# written once rather than duplicated per page.
# ─────────────────────────────────────────────────────────

class BasePage:
    def __init__(self, page):
        self.page = page
        self.loading_spinner = page.locator(".oxd-loading-spinner")
        self.toast_message = page.locator(".oxd-toast")
        self.table_rows = page.locator(".oxd-table-body .oxd-table-row")

    # ── Navigation ──────────────────────────────────────

    def goto(self, path="/"):
        self.page.goto(path, wait_until="domcontentloaded", timeout=30000)

    def get_title(self):
        return self.page.title()

    def get_url(self):
        return self.page.url

    # ── Wait strategies ─────────────────────────────────

    def wait_for_page_ready(self):
        try:
            self.loading_spinner.wait_for(state="hidden", timeout=10000)
        except Exception:
            # Spinner may not appear at all — that's fine
            pass
        self.page.wait_for_load_state("domcontentloaded")

    def wait_for_table_data(self, timeout=15000):
        self.table_rows.first.wait_for(state="visible", timeout=timeout)

    # ── Table helpers ───────────────────────────────────

    def get_row_count(self):
        self.wait_for_table_data()
        return self.table_rows.count()

    def get_row_by_text(self, text):
        return self.table_rows.filter(has_text=text)

    # ── Modal helpers ───────────────────────────────────

    def wait_for_modal(self):
        self.page.locator(".orangehrm-dialog-popup").wait_for(
            state="visible", timeout=10000
        )

    def confirm_modal(self):
        self.wait_for_modal()
        self.page.get_by_role("button", name="Yes, Delete").click()

    def dismiss_modal(self):
        self.wait_for_modal()
        self.page.get_by_role("button", name="No, Cancel").click()

    # ── Toast helper ────────────────────────────────────

    def wait_for_success_toast(self):
        self.toast_message.wait_for(state="visible", timeout=10000)
        return self.toast_message.inner_text()