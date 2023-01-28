# Copyright (c) 2023, Shaima'a Khashan and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils.data import date_diff, getdate
from datetime import date


class LeaveApplication(Document):

	def get_total_days(self):
		if self.from_date and self.to_date:
			total_days = date_diff(self.to_date, self.from_date)
			return total_days + 1

	def get_allocate_doc(self):
		allocate_docs = frappe.get_all('Leave Allocation', ['name'], filters={
			'employee': self.employee,
			# 'from_date': [''],
			# 'to_date': [''],
			'leave_type': self.leave_type
		})
		if allocate_docs:
			allocate_doc = frappe.get_doc('Leave Allocation', allocate_docs[0].name)
			return allocate_doc
		else:
			frappe.throw("No Leave Allocation Exists!")

	def check_application_docs(self):
		if self.from_date:
			application_docs = frappe.get_all('Leave Application', ['name'], filters={
				'employee': self.employee,
				'status': 'Submitted',
				'from_date': getdate(self.from_date)
			})
			if application_docs:
				frappe.throw("A Leave Application Exists On The Same Date Of Start!")
		if self.to_date:
			application_docs = frappe.get_all('Leave Application', ['name'], filters={
				'employee': self.employee,
				'status': 'Submitted',
				'to_date': getdate(self.to_date)
			})
			if application_docs:
				frappe.throw("A Leave Application Exists On The Same Date Of End!")

	def check_application_dates(self):
		if getdate(self.to_date) < getdate(self.from_date):
			frappe.throw("Start Date Must Be Before End Date")

	def check_max_allowed_days(self):
		if self.from_date:
			leave_type_doc = frappe.get_doc('Leave Type', self.leave_type)
			max_days = leave_type_doc.max_days_allowed
			diff = date_diff(getdate(self.from_date), self.to_date) + 1
			if diff > int(max_days):
				frappe.throw(f"You're allowed just {max_days} days continue!")

	def check_applicable_after(self):
		if self.from_date:
			leave_type_doc = frappe.get_doc('Leave Type', self.leave_type)
			after_days = leave_type_doc.applicable_after
			diff = date_diff(getdate(self.from_date), date.today()) + 1
			if diff > int(after_days):
				frappe.throw(f"You Have To Apply Before {after_days}!")
	#
	# def get_leave_balance_before(self):
	# 	if self.employee and self.leave_type and self.from_date and self.to_date:
	# 		allocate_doc = self.get_allocate_doc()
	# 		if allocate_doc.from_date > getdate(self.from_date) or allocate_doc.to_date < getdate(self.to_date):
	# 			frappe.throw("Check Your Start & End Allocation Dates Please.")
	# 		balance_before = allocate_doc.get_value('total_leave_allocate')
	# 		return balance_before

	def on_submit_total_leave_allocate(self, balance):
		leave_type_doc = frappe.get_doc('Leave Type', self.leave_type)
		check_box = leave_type_doc.allow_negative_balance
		if check_box:
			allocate_doc = self.get_allocate_doc()
			allocate_doc.set('total_leave_allocate', balance - self.total_days)
			allocate_doc.flags.ignore_permissions = True
			allocate_doc.flags.ignore_mandatory = True
			allocate_doc.save()
			frappe.db.commit()
		else:
			if balance >= self.total_days:
				allocate_doc = self.get_allocate_doc()
				allocate_doc.set('total_leave_allocate', balance - self.total_days)
				allocate_doc.flags.ignore_permissions = True
				allocate_doc.flags.ignore_mandatory = True
				allocate_doc.save()
				frappe.db.commit()

			else:
				frappe.throw("Check Your Rest Allocation Days Please.")

	def on_cancel_total_leave_allocate(self):
		allocate_doc = self.get_allocate_doc()
		allocate_doc.set('total_leave_allocate', allocate_doc.total_leave_allocate + self.total_days)
		allocate_doc.flags.ignore_permissions = True
		allocate_doc.flags.ignore_mandatory = True
		allocate_doc.save()
		frappe.db.commit()

	def validate(self):
		self.check_application_dates()
		self.check_application_docs()
		self.check_max_allowed_days()
		self.check_applicable_after()
		self.total_days = float(self.get_total_days())
		# self.leave_balance_before = self.get_leave_balance_before()

	def on_submit(self):
		self.on_submit_total_leave_allocate(self.leave_balance_before)

	def on_cancel(self):
		self.on_cancel_total_leave_allocate()


def get_allocate_doc(employee, leave_type):
	allocate_docs = frappe.get_all('Leave Allocation', ['name'], filters={
		'employee': employee,
		# 'from_date': [''],
		# 'to_date': [''],
		'leave_type': leave_type
	})
	if allocate_docs:
		allocate_doc = frappe.get_doc('Leave Allocation', allocate_docs[0].name)
		return allocate_doc
	else:
		frappe.throw("No Leave Allocation Exists!")


@frappe.whitelist(allow_guest=False)
def get_leave_balance_before(employee, leave_type, from_date, to_date):
	if employee and leave_type and from_date and to_date:
		allocate_doc = get_allocate_doc(employee, leave_type)
		if allocate_doc.from_date > getdate(from_date) or allocate_doc.to_date < getdate(to_date):
			frappe.throw("Check Your Start & End Allocation Dates Please.")
		balance_before = allocate_doc.get_value('total_leave_allocate')
		return balance_before


