# Copyright (c) 2023, Shaima'a Khashan and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class Employee(Document):

	# this method will run every time a document is saved
	def before_save(self):
		self.full_name = f'{self.first_name} {self.middle_name} {self.last_name or ""}'
