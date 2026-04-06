from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def create_test_contract():
    c = canvas.Canvas("test_contract.pdf", pagesize=letter)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(200, 750, "SERVICE AGREEMENT")
    
    c.setFont("Helvetica", 11)
    content = [
        "",
        "This Service Agreement is entered into as of March 1, 2026, between:",
        "",
        "CLIENT: RetailPlus Inc., 123 Commerce Street, Austin, TX 78701",
        "SERVICE PROVIDER: Charles Cox Consulting, Remote",
        "",
        "SERVICES:",
        "Charles Cox Consulting agrees to design and implement an AI-powered",
        "customer support automation system for RetailPlus Inc. The system will",
        "include email triage, automated response generation, and an observability",
        "dashboard tracking resolution rates.",
        "",
        "TIMELINE:",
        "Project start date: April 1, 2026",
        "Project completion date: June 30, 2026",
        "Total project duration: 3 months",
        "",
        "PAYMENT TERMS:",
        "Total contract value: $18,000 USD",
        "Payment schedule:",
        "  - 33% deposit due April 1, 2026: $6,000",
        "  - 33% due May 1, 2026: $6,000",
        "  - 34% due upon completion June 30, 2026: $6,120",
        "",
        "Late payments will incur a 1.5% monthly interest charge.",
        "",
        "INTELLECTUAL PROPERTY:",
        "All work product created under this agreement becomes the property",
        "of RetailPlus Inc. upon final payment.",
        "",
        "CONFIDENTIALITY:",
        "Both parties agree to keep all project details and business information",
        "confidential for a period of 2 years following project completion.",
        "",
        "TERMINATION:",
        "Either party may terminate this agreement with 30 days written notice.",
        "Client is responsible for payment of all work completed prior to termination.",
        "",
        "NOTE: This agreement has not yet been signed by RetailPlus Inc.",
        "Signature deadline: March 15, 2026 - OVERDUE",
        "",
        "Signed: Charles Cox, Charles Cox Consulting",
        "Date: March 1, 2026",
    ]

    y = 720
    for line in content:
        c.drawString(72, y, line)
        y -= 18
        if y < 72:
            c.showPage()
            y = 750

    c.save()
    print("Created test_contract.pdf")

create_test_contract()
