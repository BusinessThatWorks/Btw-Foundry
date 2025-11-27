frappe.pages['customer-production-status'].on_page_load = function(wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'Customer Production Status',
		single_column: true
	});
}