from io import BytesIO

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


def build_statement_pdf(account):
    buffer = BytesIO()
    document = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=42,
        leftMargin=42,
        topMargin=42,
        bottomMargin=42,
    )
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph("State Bank of India", styles["Title"]))
    story.append(Paragraph("Account Statement", styles["Heading2"]))
    story.append(Spacer(1, 0.18 * inch))

    details = [
        ["Account Number", account.account_no],
        ["Customer Name", account.name],
        ["Phone", account.phone or "-"],
        ["KYC Status", account.kyc_status or "Pending"],
        ["Current Balance", f"Rs. {account.get_balance():,.2f}"],
    ]
    details_table = Table(details, colWidths=[1.8 * inch, 4.7 * inch])
    details_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#eaf2fb")),
        ("TEXTCOLOR", (0, 0), (-1, -1), colors.HexColor("#142033")),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#d8e4ee")),
        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
        ("PADDING", (0, 0), (-1, -1), 8),
    ]))
    story.append(details_table)
    story.append(Spacer(1, 0.25 * inch))

    transaction_rows = [["Type", "Amount", "Date"]]
    for transaction in account.transactions:
        transaction_rows.append([
            transaction.transaction_type,
            f"Rs. {float(transaction.amount):,.2f}",
            transaction.date,
        ])

    if len(transaction_rows) == 1:
        transaction_rows.append(["No transactions found", "-", "-"])

    transaction_table = Table(transaction_rows, colWidths=[1.8 * inch, 1.8 * inch, 2.9 * inch])
    transaction_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0b4ea2")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#d8e4ee")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f8fbff")]),
        ("PADDING", (0, 0), (-1, -1), 8),
    ]))
    story.append(Paragraph("Transaction History", styles["Heading3"]))
    story.append(transaction_table)

    document.build(story)
    buffer.seek(0)
    return buffer.getvalue()
