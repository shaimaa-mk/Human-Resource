
import frappe


@frappe.whitelist(allow_guest=True)
def add_employee_attendance(**kwargs):
    data = kwargs

    if 'check_in' not in data:
        frappe.response(False, 400, "Check In Required!", None)
        return
    check_in = data['check_in']

    if 'check_out' not in data:
        frappe.response(False, 400, "Check Out Required!", None)
        return
    check_in = data['check_in']

    if 'name' not in data:
        frappe.response(False, 400, "Employee Doc Name Required!", None)
        return
    name = data['name']

    if 'full_name' not in data:
        frappe.response(False, 400, "Employee Doc Name Required!", None)
        return
    full_name = data['full_name']





