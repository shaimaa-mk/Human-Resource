# Copyright (c) 2023, Shaima'a Khashan and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):

	columns = [
		{'fieldname': 'employee', 'label': 'Employee', 'fieldtype': 'Link', 'options': 'Employee'},
		{'fieldname': 'employee_name', 'label': 'Employee Name', 'fieldtype': 'Data'},
		{'fieldname': 'attendance_date', 'label': 'Attendance Date', 'fieldtype': 'Date'},
		{'fieldname': 'department', 'label': 'Department', 'fieldtype': 'Link', 'options': 'Department'},
		{'fieldname': 'status', 'label': 'Status', 'fieldtype': 'Select', 'options': ['Present', 'Absent']},
		{'fieldname': 'check_in', 'label': 'Check In', 'fieldtype': 'Time'},
		{'fieldname': 'check_out', 'label': 'Check Out', 'fieldtype': 'Time'},
		{'fieldname': 'work_hours', 'label': 'Work Hours', 'fieldtype': 'Float'},
		{'fieldname': 'late_hours', 'label': 'Late Hours', 'fieldtype': 'Float'}]

	data = frappe.db.get_all("Attendance", ['employee', 'employee_name', 'attendance_date', 'department', 'status',
											'check_in', 'check_out', 'work_hours', 'late_hours'], filters=filters)
	return columns, data
