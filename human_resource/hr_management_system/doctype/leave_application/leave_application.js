// Copyright (c) 2023, Shaima'a Khashan and contributors
// For license information, please see license.txt

frappe.ui.form.on('Leave Application', {
	// refresh: function(frm) {
//
//	// }
    employee:
	    function(frm) {
            frm.trigger("get_leave_balance_before")
            },

    leave_type:
	    function(frm) {
            frm.trigger("get_leave_balance_before")
            },

    from_date:
        function(frm) {
            frm.trigger("get_leave_balance_before")
            },

	to_date:
	    function(frm) {
            frm.trigger("get_leave_balance_before")
            },

	get_leave_balance_before:
            function(frm){
            if( !frm.doc.from_date | !frm.doc.to_date | !frm.doc.employee | !frm.doc.leave_type){
                return;
            }
            frappe.call({
                    method:"human_resource.hr_management_system.doctype.leave_application.leave_application.get_leave_balance_before",
                    args:{
                        from_date: frm.doc.from_date,
                        to_date: frm.doc.to_date,
                        employee: frm.doc.employee,
                        leave_type: frm.doc.leave_type
                    },
                    callback: (r) =>{
                        frm.doc.leave_balance_before = r.message;
                        frm.refresh();
                    }
                })
            },
    //new trigger

});
