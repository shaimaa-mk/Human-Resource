import frappe


@frappe.whitelist()
def get_employee_info(name: None):
    all_employee = []
    if name:
        all_employee = frappe.db.sql(""" SELECT * FROM `tabEmployee` WHERE name = %s; """,
                                     [name, ], as_dict=1)
    return all_employee

