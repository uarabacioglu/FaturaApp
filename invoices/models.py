from django.db import models

# 1. Şirket Modeli
class Sirket(models.Model):
    title = models.CharField(max_length=255)
    logo = models.ImageField(upload_to='logos/', blank=True, null=True)
    adres = models.TextField()
    tel = models.CharField(max_length=50)
    mobil = models.CharField(max_length=50)
    web = models.URLField(blank=True, null=True)
    email = models.EmailField()
    bank = models.CharField(max_length=255)
    iban = models.CharField(max_length=34)
    bic_no = models.CharField(max_length=15)

    def __str__(self):
        return str(self.title)

# 2. Müşteri Modeli
class Musteri(models.Model):
    title = models.CharField(max_length=255)
    adres = models.TextField()
    tel = models.CharField(max_length=50)
    email = models.EmailField()
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.title)

# 4. Ürün Modeli
class Urun(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='urunler/', blank=True, null=True)
    birim_fiyat = models.DecimalField(max_digits=10, decimal_places=2)
    kdv_orani = models.DecimalField(max_digits=4, decimal_places=2)
    birim_kdv_tutari = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return str(self.title)

# 3. Fatura Modeli
class Fatura(models.Model):
    fatura_no = models.CharField(max_length=50, unique=True, blank=False, null=False)
    date_created = models.DateTimeField(auto_now_add=True)
    bizim_firma = models.ForeignKey(Sirket, on_delete=models.CASCADE)
    musteri = models.ForeignKey(Musteri, on_delete=models.CASCADE)
    urunler = models.ManyToManyField(Urun, through='FaturaUrun')

    def __str__(self):
        return f"Fatura {self.fatura_no}"

# Ara model: Fatura <-> Ürün ilişkisi + miktar
class FaturaUrun(models.Model):
    fatura = models.ForeignKey(Fatura, on_delete=models.CASCADE)
    urun = models.ForeignKey(Urun, on_delete=models.CASCADE)
    aciklama = models.TextField(blank=True, null=True)
    adet = models.PositiveIntegerField()
    kdvsiz_toplam = models.DecimalField(max_digits=10, decimal_places=2)
    kdvli_toplam = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.adet} x {self.urun.title} (Fatura: {self.fatura.fatura_no})"
