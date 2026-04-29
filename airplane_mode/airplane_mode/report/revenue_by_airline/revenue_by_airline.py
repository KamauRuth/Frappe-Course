import frappe

def execute(filters=None):
    # Fetch all airlines
    airlines = frappe.get_all("Airline", fields=["name"])
    data = []

    # Loop through each airline and calculate total revenue
    for airline in airlines:
        # Query total revenue for each airline
        total_revenue = frappe.db.sql("""
            SELECT SUM(flight_price)
            FROM `tabAirplane Ticket`
            WHERE airline = %s AND docstatus = 1
        """, (airline.name,), as_list=True)
        
        # If revenue exists, use it; otherwise, set it to 0
        revenue = total_revenue[0][0] if total_revenue else 0

        # Append results to data list
        data.append({
            "Airline": airline.name,
            "Revenue": revenue
        })

    return data