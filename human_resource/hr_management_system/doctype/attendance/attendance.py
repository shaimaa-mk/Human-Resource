# Copyright (c) 2023, Shaima'a Khashan and contributors
# For license information, please see license.txt
import frappe
from frappe.utils.data import time_diff_in_hours, nowdate, get_timedelta, get_datetime, to_timedelta
from frappe.model.document import Document


class Attendance(Document):

    def get_work_hours(self):
        # settings.late_entry_grace_period
        # settings.early_exit_grace_period
        self.work_hours = time_diff_in_hours(self.check_out, self.check_in)

    def get_status(self):
        settings = frappe.get_doc("Attendance Settings")
        if self.work_hours >= settings.working_hours_threshold_for_absent:
            self.status == "Present"
        else:
            self.status = "Absent"

    def time_diff_in_minutes(self, string_ed_time, string_st_time):
        return round(float(to_timedelta(string_ed_time) - to_timedelta(string_st_time)) / 60, 6)

    def get_late_hours(self):
        settings = frappe.get_doc("Attendance Settings")
        st_check = get_datetime(self.check_in).time
        ed_check = get_datetime(self.check_out).time
        start = self.time_diff_in_minutes(st_check, settings.start_time)
        end = self.time_diff_in_minutes(settings.end_time, ed_check)
        self.late_hours = start + end

    def on_save(self):
        self.attendance_date = nowdate()

    def on_submit(self):
        self.get_work_hours()
        self.get_status()
        self.get_late_hours()



