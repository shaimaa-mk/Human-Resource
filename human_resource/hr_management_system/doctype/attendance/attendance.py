# Copyright (c) 2023, Shaima'a Khashan and contributors
# For license information, please see license.txt
import frappe
from frappe.utils.data import get_timedelta
from frappe.model.document import Document


class Attendance(Document):

    def time_diff(self, string_en_time, string_st_time):
        return get_timedelta(string_en_time) - get_timedelta(string_st_time)

    def time_diff_in_minutes(self, string_ed_time, string_st_time):
        return round(float(self.time_diff(string_ed_time, string_st_time).total_seconds()) / 60, 0)

    def time_diff_in_hours(self, string_ed_time, string_st_time):
        return round(float(self.time_diff(string_ed_time, string_st_time).total_seconds()) / 3600, 0)

    def get_work_hours(self):
        settings = frappe.get_doc("Attendance Settings")
        start = self.time_diff_in_minutes(self.check_in, settings.start_time)
        end = self.time_diff_in_minutes(settings.end_time, self.check_out)
        if start > 0 and end > 0:
            if start <= settings.late_entry_grace_period and end <= settings.early_exit_grace_period:
                self.work_hours = self.time_diff_in_hours(self.check_out, self.check_in)
                self.status == "Present"
            elif start > settings.late_entry_grace_period and end <= settings.early_exit_grace_period:
                rest = start - 30.0
                self.work_hours = self.time_diff_in_hours(self.check_out, self.check_in) - (rest / 60)
                self.status = "Present"
            elif start <= settings.late_entry_grace_period and end > settings.early_exit_grace_period:
                rest = end - 30.0
                self.work_hours = self.time_diff_in_hours(self.check_out, self.check_in) - (rest / 60)
                self.status = "Present"
            elif start > settings.late_entry_grace_period and end > settings.early_exit_grace_period:
                rest = (start - 30.0) + (end - 30.0)
                self.work_hours = self.time_diff_in_hours(self.check_out, self.check_in) - (rest / 60)
                self.status = "Present"
            else:
                self.work_hours = 0.0
                self.status = "Absent"
        else:
            self.status = "Absent"

    def get_late_hours(self):
        settings = frappe.get_doc("Attendance Settings")
        start = self.time_diff_in_minutes(self.check_in, settings.start_time)
        end = self.time_diff_in_minutes(settings.end_time, self.check_out)
        if start > 0 and end > 0:
            if start <= settings.late_entry_grace_period and end <= settings.early_exit_grace_period:
                self.late_hours = 0.0
                self.status == "Present"
            elif start > settings.late_entry_grace_period and end <= settings.early_exit_grace_period:
                self.late_hours = (start - 30) / 60
                self.status = "Present"
            elif start <= settings.late_entry_grace_period and end > settings.early_exit_grace_period:
                self.late_hours = (end - 30) / 60
                self.status = "Present"
            else:

                self.late_hours = ((start - 30) + (end - 30)) / 60
                self.status = "Present"
        else:
            self.status = "Absent"

    def validate(self):
        self.get_work_hours()
        self.get_late_hours()

