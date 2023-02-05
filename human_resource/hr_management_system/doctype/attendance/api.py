import frappe


@frappe.whitelist(allow_guest=True)
def add_employee_attendance(**kwargs):
    """
        This API aim to Employee able to add attendance details where this Employee already authorized as System User.
        Return : API Response with Employee Details.
        Args:
            kwargs which have to contain attendance date, check in time, check out time.
            attendance date as date format (YYYY-MM-DD) that represents attendance_date attribute in Attendance record.
            check in as time format (HH:MM:SS) that represents check_it attribute in Attendance record.
            check out at time format (HH:MM:SS)that represents check_out attribute in Attendance record.
        """
    data = kwargs

    if 'check_in' not in data:
        frappe.response = {'status': {False, 400, "Check In Required!"}}
        return
    check_in = data['check_in']

    if 'check_out' not in data:
        frappe.response = {'status': {False, 400, "Check Out Required!"}}
        return
    check_out = data['check_out']

    if 'date' not in data:
        frappe.response = {'status': {False, 400, "Date Required!"}}
        return
    date = data['date']

    # Getting User API Key to retrieve Employee who's related to that user.
    api_access = get_user_api_access()
    employee = get_employee(api_access)
    if not employee:
        return

    # Creating Attendance record for Employee in Attendance collection.
    attendance = frappe.get_doc({
        'doctype': 'Attendance',
        'employee': employee.name,
        'attendance_date': date,
        'department': employee.department,
        'check_in': check_in,
        'check_out': check_out,
    })
    save_doc(attendance)

    # Getting Success Response with Attendance Details.
    frappe.local.response['status'] = {True, 200, "Authorized Access"}
    frappe.local.response['data'] = {'Employee Attendance': attendance}


def get_user_api_access():
    """
    Aim: Ensure User already authorized to get access.
    Return: User API Key, API Secret.
    """
    if frappe.get_request_header('Authorization'):
        head_auth = frappe.get_request_header('Authorization').split(" ")
        if head_auth[0] != 'token' and len(head_auth) != 2:
            frappe.local.response['status'] = {False, 400, "Not Authorized3"}
            return
        api_access = head_auth[1].split(':')
        return api_access
    else:
        frappe.local.response['status'] = {False, 400, "Not Authorized4"}
        return


def get_employee(api_access):
    """
    Return: Employee Object.
    Args:
        api_access as hashable list with 2 items api_key, and api_secret.
    """
    if not frappe.db.exists("User", {'api_key': api_access[0]}):
        frappe.local.response['status'] = {False, 400, "Not Authorized1"}
        return
    user = frappe.get_doc('User', {'api_key': api_access[0]})
    if not frappe.db.exists("Employee", {'user': user.name}):
        frappe.local.response['status'] = {False, 400, "Not Authorized2"}
        return
    return frappe.get_doc("Employee", {'user': user.name})


def save_doc(doctype):
    """
    Aim: to save all changes on Human Resource records without user permissions and insertion conditions.
    Args:
        Document object requires to save after creation or updates.
    """
    doctype.flags.ignore_permissions = True
    doctype.flags.ignore_mandatory = True
    doctype.save()
    frappe.db.commit()



