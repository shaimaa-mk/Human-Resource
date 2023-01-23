# Copyright (c) 2023, Shaima'a Khashan and contributors
# For license information, please see license.txt

import frappe
from datetime import date
from frappe.model.document import Document


class LeaveApplication(Document):

	@frappe.whitelist(allow_guest=False)
	def get_y_m_d(self, dat):
		d = list(map(int, dat.split('-')))
		return d

	@frappe.whitelist(allow_guest=False)
	def get_days(self):
		start = self.get_y_m_d(self.from_date)
		end = self.get_y_m_d(self.to_date)
		if end[0] == start[0] and end[1] == start[1]:
			days = end[2] - start[2]
			return days
		elif end[0] == start[0] and end[1] != start[1]:
			days = (end[1] - start[1]) * 30 + (end[2] - start[2])
			return days
		elif end[0] != start[0]:
			days = (end[0] - start[0]) * 365 + (end[1] - start[1]) * 30 + (end[2] - start[2])
			return days
		return

	@frappe.whitelist(allow_guest=False)
	def get_balance_before(self):
		emp_docs = frappe.get_all('Leave Allocation', ['name'], filters={
			'employee': self.employee,
			'leave_type': self.leave_type
			})
		if emp_docs:
			emp_doc = frappe.get_doc('Leave Allocation', emp_docs[0].name)
			s_duration = emp_doc.from_date
			e_duration = emp_doc.to_date
			start = self.get_y_m_d(self.from_date)
			end = self.get_y_m_d(self.to_date)
			s_leave = date(start[0], start[1], start[2])
			e_leave = date(end[0], end[1], end[2])
			if s_duration > s_leave or e_duration < e_leave:
				frappe.throw("Check Your Start & End Allocation Dates Please.")

			balance_before = emp_doc.get_value('total_leave_allocate')
			if balance_before >= self.total_days:
				emp_doc.set('total_leave_allocate', balance_before - self.total_days)
				emp_doc.flags.ignore_permissions = True
				emp_doc.flags.ignore_mandatory = True
				emp_doc.save()
				frappe.db.commit()
				return balance_before
			else:
				frappe.throw("Check Your Rest Allocation Days Please.")
		else:
			frappe.throw("No Leave Allocation Exists!")

	def before_save(self):
		self.total_days = float(self.get_days())
		self.leave_balance_before = self.get_balance_before()
