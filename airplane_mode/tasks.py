
import frappe
from frappe.utils import today, add_months
from frappe import _

def send_rent_reminder():
    settings = frappe.get_single("Airport Setting")
    if not settings.enable_rent_reminders:
        return
    
    contracts = frappe.get_all(
        "Shop Contract",
        filters={
            "status": "Active",
            "start_date": ["<=", today()],
            "end_date": [">=", today()],
        },
        fields=["name", "tenant", "shop", "start_date", "end_date", "airport", "monthly_rent", "tenant_name"]
    )

    for row in contracts:
        next_billing_date = add_months(row.start_date, 1)
        print(next_billing_date)
        
        if next_billing_date <= row.end_date:
            print("pass")
            tenant_email = frappe.db.get_value("Shop Tenant", row.tenant, "email_id")
            row.email_id = tenant_email
            row.next_billing_date = next_billing_date
            send_mail(row)

def send_mail(data):
    message = f"""
        Dear {data.tenant_name},

        RENT PAYMENT REMINDER
        =====================

        Shop: {data.shop} ({data.airport})
        Contract ID: {data.name}
        Amount Due: ${data.monthly_rent}
        Due Date: {data.next_payment_date}

        Please ensure payment is made on time to avoid:
        • Late payment fees (5% of rent)
        • Service interruption
        • Contractual penalties

        PAYMENT OPTIONS:
        1. Online via portal: https://bts.airport.com
        2. Bank transfer: Account #7124-1207--001
        3. In-person at Airport Admin Office

        If payment is already made, please ignore this notice.

        For assistance:
        📧 accounts@airport.com
        📞 +97471241207

        Best regards,
        BTS Airport Management Team

        ---
        This is an automated message. Do not reply.
        © {frappe.utils.now_datetime().year} Airport Management
    """

    frappe.sendmail(
        recipients=data.email_id,
        subject=f"Rent Payment Due Soon - Shop {data.shop}",
        message=message,
        reference_doctype="Shop Contract",
        reference_name=data.name,
        now=True
    )


@frappe.whitelist()
def get_default_rent():
    default_rent_amount = frappe.db.get_single_value("Airport Setting", "default_rent_amount")
    return default_rent_amount
        