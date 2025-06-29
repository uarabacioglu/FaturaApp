import tempfile
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from xhtml2pdf import pisa
from django.utils.timezone import localtime

def create_invoice_pdf(fatura, request=None):
    items = fatura.faturaurun_set.all()

    # Hesaplamalar
    subtotal = sum([item.kdvsiz_toplam for item in items])
    total = sum([item.kdvli_toplam for item in items])
    tax = total - subtotal

    # Tarih ve logo URL'si
    invoice_date = localtime(fatura.date_created).strftime("%d.%m.%Y")
    logo_url = request.build_absolute_uri(fatura.bizim_firma.logo.url) if request else ''

    # HTML render
    html = render_to_string("pdf/fatura_template.html", {
        "fatura": fatura,
        "items": items,
        "subtotal": subtotal,
        "tax": tax,
        "total": total,
        "invoice_date": invoice_date,
        "logo_url": logo_url
    })

    # PDF oluştur
    result = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    with open(result.name, "w+b") as output_file:
        pisa.CreatePDF(html, dest=output_file)
    return result.name

def send_invoice_email(fatura, pdf_path):
    subject = f"Fatura {fatura.fatura_no}"
    message = "Faturanızı ekte PDF olarak bulabilirsiniz."
    from_email = fatura.bizim_firma.email
    to_emails = [fatura.musteri.email, fatura.bizim_firma.email]

    email = EmailMessage(subject, message, from_email, to_emails)
    email.attach_file(pdf_path)
    email.send()
