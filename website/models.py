from django.db import models
from cloudinary.models import CloudinaryField


class Takim(models.Model):
    ad = models.CharField(max_length=200)
    logo = CloudinaryField('image', blank=True, null=True)

    def __str__(self):
        return self.ad


class Oyuncu(models.Model):
    takim = models.ForeignKey(Takim, on_delete=models.CASCADE, related_name="oyuncular")

    ad = models.CharField(max_length=100)
    pozisyon = models.CharField(max_length=50)
    numara = models.IntegerField()

    olusturma_tarihi = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.ad} - #{self.numara}"


class Mac(models.Model):
    STATUS_CHOICES = [
        ('kazanildi', 'Kazanıldı'),
        ('berabere', 'Berabere'),
        ('kaybedildi', 'Kaybedildi'),
        ('gelecek', 'Gelecek'),
    ]

    takim = models.ForeignKey(Takim, on_delete=models.CASCADE, related_name="maclar")

    ev_sahibi = models.CharField(max_length=100)
    misafir = models.CharField(max_length=100)

    ev_sahibi_gol = models.IntegerField(default=0)
    misafir_gol = models.IntegerField(default=0)

    tarih = models.DateTimeField()
    lig = models.CharField(max_length=100)
    durum = models.CharField(max_length=20, choices=STATUS_CHOICES, default='gelecek')

    def __str__(self):
        return f"{self.ev_sahibi} vs {self.misafir}"


class Haber(models.Model):
    başlık = models.CharField(max_length=200)
    içerik = models.TextField()
    görsel = CloudinaryField('image', blank=True, null=True)

    yayınlama_tarihi = models.DateTimeField(auto_now_add=True)
    güncellenme_tarihi = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-yayınlama_tarihi']

    def __str__(self):
        return self.başlık


import re
from django.db import models
from cloudinary.models import CloudinaryField

class GaleriÖğesi(models.Model):
    KATEGORI_CHOICES = [
        ('maçlar', 'Maçlar'),
        ('antrenman', 'Antrenman'),
        ('etkinlik', 'Etkinlikler'),
    ]

    # Başlık zorunlu değil, toplu yüklemede otomatik atanabilir
    başlık = models.CharField(max_length=200, blank=True, null=True)
    açıklama = models.TextField(blank=True)
    kategori = models.CharField(max_length=50, choices=KATEGORI_CHOICES, default='maçlar')

    # Eğer video eklersen, bu resim videonun kapak fotoğrafı olur!
    resim = CloudinaryField('sevgisk/image', blank=True, null=True) 
    
    # Videolar için iki farklı seçenek
    video_dosya = CloudinaryField(resource_type="video", blank=True, null=True, folder="sevgisk/videolar/")
    video_url = models.URLField(blank=True, null=True, help_text="YouTube veya başka bir video linki")

    oluşturma_tarihi = models.DateTimeField(auto_now_add=True)
    sıra = models.IntegerField(default=0)

    class Meta:
        ordering = ['-sıra', '-oluşturma_tarihi']

    def __str__(self):
        return self.başlık if self.başlık else f"Galeri Öğesi #{self.id}"

    # --- AKILLI KONTROLLER ---
    @property
    def is_video(self):
        # Dosya veya link varsa bu bir videodur
        return bool(self.video_dosya or self.video_url)

    @property
    def has_youtube_video(self):
        # Eğer video_url boşsa (None ise) hiç kontrol etmeden direkt False dön
        if not self.video_url:
            return False
        
        # Eğer doluysa içinde youtube geçiyor mu diye bak
        return "youtube.com" in self.video_url or "youtu.be" in self.video_url

    # YENİ EKLENEN 1: YouTube linkinden 11 haneli ID'yi ayıklayan fonksiyon
    @property
    def get_youtube_id(self):
        if not self.video_url:
            return None
            
        url = self.video_url.strip()
        
        # Admin panelden direkt 11 haneli kod girildiyse
        if re.match(r'^[a-zA-Z0-9_-]{11}$', url):
            return url
            
        pattern = r'(?:v=|\/embed\/|youtu\.be\/|\/shorts\/|\/live\/)([a-zA-Z0-9_-]{11})'
        match = re.search(pattern, url)
        
        if match:
            return match.group(1)
            
        return None

    # YENİ EKLENEN 2: Yerel video (dosya) var mı kontrolü
    @property
    def has_local_video(self):
        return bool(self.video_dosya)

    # YENİ EKLENEN 3: Yerel video için Thumbnail oluşturucu (Cloudinary destekli)
    @property
    def video_thumbnail(self):
        # Eğer videoya özel manuel bir resim yüklenmişse onu kullan
        if self.resim:
            return self.resim.url
            
        # Resim yüklenmemişse, Cloudinary'nin otomatik video kapağı özelliğini kullan (.mp4 yerine .jpg)
        if self.video_dosya:
            video_url = self.video_dosya.url
            if video_url:
                return video_url.rsplit('.', 1)[0] + '.jpg'
                
        return ""
     
class KurucuUye(models.Model):
    ad_soyad = models.CharField(max_length=120)
    unvan    = models.CharField(max_length=80,   help_text="Başkan, Sekreter…")
    gorev    = models.CharField(max_length=120,  blank=True)
    telefon  = models.CharField(max_length=20)
    foto     = models.ImageField(upload_to='yonetim/', blank=True, null=True)
    sira     = models.PositiveSmallIntegerField(default=0)
 
    class Meta:
        ordering = ['sira']
        verbose_name = 'Kurucu Üye'
        verbose_name_plural = 'Kurucu Üyeler'
 
    def __str__(self):
        return self.ad_soyad