import frappe


def _get_or_create_shop_type(display_name, enabled):
    existing_name = frappe.db.get_value("Shop Type", {"name1": display_name}, "name")
    if existing_name:
        frappe.db.set_value("Shop Type", existing_name, "enabled", enabled)
        return existing_name

    doc = frappe.get_doc(
        {
            "doctype": "Shop Type",
            "name1": display_name,
            "enabled": enabled,
        }
    )
    doc.insert(ignore_permissions=True)
    return doc.name


def _get_or_create_tenant(tenant_name, email, phone, address):
    existing_name = frappe.db.get_value("Tenant", {"tenant_name": tenant_name}, "name")
    if existing_name:
        frappe.db.set_value(
            "Tenant",
            existing_name,
            {
                "email": email,
                "phone": phone,
                "address": address,
            },
        )
        return existing_name

    doc = frappe.get_doc(
        {
            "doctype": "Tenant",
            "tenant_name": tenant_name,
            "email": email,
            "phone": phone,
            "address": address,
        }
    )
    doc.insert(ignore_permissions=True)
    return doc.name


def _upsert_shop(
    shop_number,
    shop_name,
    shop_type,
    tenant,
    contract_start_date,
    contract_end_date,
    rent_amount,
    rent_paid,
    rent_due_date,
    status,
):
    existing_name = frappe.db.get_value("Shop", {"shop_number": shop_number}, "name")
    values = {
        "shop_name": shop_name,
        "shop_type": shop_type,
        "tenant": tenant,
        "contract_start_date": contract_start_date,
        "contract_end_date": contract_end_date,
        "rent_amount": rent_amount,
        "rent_paid": rent_paid,
        "rent_due_date": rent_due_date,
        "status": status,
    }

    if existing_name:
        frappe.db.set_value("Shop", existing_name, values)
        return

    doc = frappe.get_doc(
        {
            "doctype": "Shop",
            "shop_number": shop_number,
            **values,
        }
    )
    doc.insert(ignore_permissions=True)


def execute():
    stall = _get_or_create_shop_type("Stall", 1)
    walkthrough = _get_or_create_shop_type("Walk-through", 1)
    normal = _get_or_create_shop_type("Normal", 1)
    kiosk = _get_or_create_shop_type("Kiosk", 0)

    john = _get_or_create_tenant(
        "John Doe", "johndoe@email.com", "123-456-7890", "123 Main St, City, Country"
    )
    alice = _get_or_create_tenant(
        "Alice Smith", "alicesmith@email.com", "987-654-3210", "456 Oak St, City, Country"
    )
    bob = _get_or_create_tenant(
        "Bob Lee", "boblee@email.com", "555-123-4567", "789 Pine St, City, Country"
    )
    sophie = _get_or_create_tenant(
        "Sophie Turner", "sophie@email.com", "111-222-3333", "321 Birch St, City, Country"
    )

    _upsert_shop(
        "001",
        "Tech Stall",
        stall,
        john,
        "2026-01-01",
        "2026-12-31",
        5000,
        2000,
        "2026-05-01",
        "Leased",
    )
    _upsert_shop(
        "002",
        "Electronics Walk-through",
        walkthrough,
        alice,
        "2026-02-01",
        "2026-11-30",
        10000,
        5000,
        "2026-06-01",
        "Leased",
    )
    _upsert_shop(
        "003",
        "Fashion Store",
        normal,
        bob,
        "2026-03-01",
        "2027-02-28",
        7000,
        3000,
        "2026-07-01",
        "Available",
    )
    _upsert_shop(
        "004",
        "Old Kiosk",
        kiosk,
        sophie,
        "2026-01-15",
        "2026-12-15",
        3000,
        1500,
        "2026-05-15",
        "Leased",
    )
