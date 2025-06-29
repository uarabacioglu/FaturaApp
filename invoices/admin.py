from django.contrib import admin, messages
from .models import Sirket, Musteri, Urun, Fatura, FaturaUrun
from .utils import create_invoice_pdf, send_invoice_email

class SirketAdmin(admin.ModelAdmin):
    list_display = ('title', 'email', 'tel', 'iban')
    search_fields = ('title', 'email')

admin.site.register(Sirket, SirketAdmin)


class FaturaUrunInline(admin.TabularInline):
    model = FaturaUrun
    extra = 1

@admin.action(description="Seçilen faturaları PDF olarak oluştur ve e-posta gönder")
def export_fatura_and_send_email(modeladmin, request, queryset):
    for fatura in queryset:
        pdf_path = create_invoice_pdf(fatura)
        try:
            send_invoice_email(fatura, pdf_path)
            messages.success(request, f"{fatura.fatura_no} başarıyla gönderildi.")
        except Exception as e:
            messages.error(request, f"{fatura.fatura_no} gönderilemedi: {str(e)}")

@admin.register(Fatura)
class FaturaAdmin(admin.ModelAdmin):
    list_display = ('fatura_no', 'date_created', 'bizim_firma', 'musteri')
    search_fields = ('fatura_no',)
    list_filter = ('date_created', 'bizim_firma')
    inlines = [FaturaUrunInline]
    actions = [export_fatura_and_send_email]
