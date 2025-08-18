import frappe

def get_address_and_contact(customer: str) -> list:
    """Get address and contact details for a given customer.
        returns a list containing the address and contact details.
    """
    customer_doc = frappe.get_doc("Customer", customer)
    if not customer_doc.customer_primary_address:
        return ["", ""]
    address = frappe.get_doc("Address", customer_doc.customer_primary_address)
    if not customer_doc:
        return ["", ""]

    if not frappe.db.exists("Contact", customer_doc.customer_primary_contact):
        return ["", ""]

    contact = frappe.get_doc("Contact", customer_doc.customer_primary_contact)
    return [f"<p>{address.address_line1}</p><p>{address.city}</p>", contact.phone]

def get_company_address(company: str) -> str:
    """Get the address of the company."""
    address = frappe.db.sql("""
        SELECT addr.address_line1, addr.city, addr.state, addr.country
        FROM `tabAddress` addr
        LEFT JOIN `tabDynamic Link` dl ON addr.name = dl.parent
        WHERE dl.link_name = %s and dl.link_doctype = 'Company'
    """, (company,), as_dict=True)
    if not len(address):
        return ""
    address = address[0]
    return f"<p>{address.address_line1}</p><p>{address.city}</p>"