from pages.base_page import BasePage

# ─────────────────────────────────────────────────────────
# EmployeeListPage — PIM > Employee List
#
# Python equivalent of EmployeeListPage.js
# Search form, table interactions, row actions.
# ─────────────────────────────────────────────────────────

class EmployeeListPage(BasePage):
    def __init__(self, page):
        super().__init__(page)

        self.add_button = page.get_by_role("button", name="Add")
        self.search_button = page.get_by_role("button", name="Search")
        self.reset_button = page.get_by_role("button", name="Reset")

        self.employee_id_field = (
            page.locator(".oxd-input-group")
            .filter(has_text="Employee Id")
            .locator(".oxd-input")
        )

    def goto(self):
        super().goto("/web/index.php/pim/viewEmployeeList")
        self.wait_for_page_ready()
        self.wait_for_table_data()

    def search_by_employee_id(self, employee_id):
        self.employee_id_field.fill(employee_id)
        self.search_button.click()
        self.wait_for_page_ready()

    def reset_search(self):
        self.reset_button.click()
        self.wait_for_page_ready()
        self.wait_for_table_data()

    def get_record_count(self):
        count_span = (
            self.page.locator("span.oxd-text")
            .filter(has_text="Record")
        )
        count_span.wait_for(state="visible", timeout=10000)
        text = count_span.inner_text()

        if "No Records" in text:
            return 0

        import re
        match = re.search(r"\((\d+)\)", text)
        return int(match.group(1)) if match else None

    def get_visible_row_count(self):
        return self.table_rows.count()

    def get_row_by_id(self, employee_id):
        return self.table_rows.filter(
            has=self.page.locator(".oxd-table-cell")
            .nth(1)
            .filter(has_text=__import__("re").compile(f"^\\s*{employee_id}\\s*$"))
        )