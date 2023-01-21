# Copyright (c) 2023, Shaima'a Khashan and contributors
# For license information, please see license.txt

# import frappe
from datetime import date

import frappe
from frappe.model.document import Document


class Employee(Document):

	# this method will run every time a document is saved
	def before_save(self):
		self.full_name = f'{self.first_name} {self.middle_name} {self.last_name or ""}'

	def validate(self):
		if self.status != 'Active':
			frappe.throw("Status Of Employee Must Be Active!")
		if self.get_age() <= 60:
			frappe.throw("Age must be more than 60 years!")
		if not (len(self.mobile) == 10 and self.mobile.startswith('059')):
			frappe.throw("Mobile No. Must Be 10 Digits!")
		if len(self.employee_education) > 1:
			frappe.throw("Employee Must Have 2 Educations!")

	@frappe.whitelist(allow_guest=False)
	def get_age(self):
		today = date.today()
		year, month, day = self.date_of_birth.split('-')
		one_zero = ((today.month, today.day) < (int(month), int(day)))
		year_difference = today.year - int(year)
		self.age = year_difference - one_zero
		return self.age

