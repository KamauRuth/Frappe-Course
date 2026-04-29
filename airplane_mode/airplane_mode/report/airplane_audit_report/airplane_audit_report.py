
import frappe


def _pick_field(available_fields, candidates):
    for fieldname in candidates:
        if fieldname in available_fields:
            return fieldname
    return None


def execute(filters=None):
    columns = [
        {"label": "Airplane", "fieldname": "airplane", "fieldtype": "Link", "options": "Airplane", "width": 180},
        {"label": "Audit Date", "fieldname": "audit_date", "fieldtype": "Date", "width": 120},
        {"label": "Audit Type", "fieldname": "audit_type", "fieldtype": "Data", "width": 140},
        {"label": "Status", "fieldname": "status", "fieldtype": "Data", "width": 120},
        {"label": "Audit Result", "fieldname": "audit_result", "fieldtype": "Data", "width": 220},
        {"label": "Inspector", "fieldname": "inspector", "fieldtype": "Data", "width": 160},
    ]

    meta = frappe.get_meta("Airplane Audit")
    available_fields = {field.fieldname for field in meta.fields}

    selected_fields = {
        "audit_date": _pick_field(available_fields, ["audit_date", "date"]),
        "audit_type": _pick_field(available_fields, ["audit_type", "type"]),
        "status": _pick_field(available_fields, ["status"]),
        "audit_result": _pick_field(available_fields, ["audit_result", "result", "remarks"]),
        "inspector": _pick_field(available_fields, ["inspector", "auditor", "performed_by"]),
    }

    query_fields = [field for field in selected_fields.values() if field] or ["name"]
    data = []

    for airplane in frappe.get_all("Airplane", fields=["name"]):
        filters = {"parent": airplane.name, "parenttype": "Airplane"}
        if "airplane" in available_fields:
            filters = {"airplane": airplane.name}

        audits = frappe.get_all("Airplane Audit", filters=filters, fields=query_fields)

        for audit in audits:
            row = {"airplane": airplane.name}
            for output_key, source_field in selected_fields.items():
                row[output_key] = audit.get(source_field) if source_field else None
            data.append(row)

    return columns, data