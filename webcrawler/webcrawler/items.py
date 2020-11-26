# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class WebcrawlerItem(scrapy.Item):
    Fiyat = scrapy.Field()
    YeniFiyat = scrapy.Field()
    Il = scrapy.Field()
    Ilce = scrapy.Field()
    Mahalle = scrapy.Field()
    IlanTarihi = scrapy.Field()
    GuncellemeTarihi = scrapy.Field()
    YeniDurum = scrapy.Field()
    IlanNo = scrapy.Field()
    IlanDurumu = scrapy.Field()
    KonutSekli = scrapy.Field()
    OdaSayisi = scrapy.Field()
    M2 = scrapy.Field()
    BulunduguKat = scrapy.Field()
    BinaYasi = scrapy.Field()
    Isinma = scrapy.Field()
    KatSayisi = scrapy.Field()
    Kredi = scrapy.Field()
    Esya = scrapy.Field()
    BanyoSayisi = scrapy.Field()
    YapiTipi = scrapy.Field()
    YapiDurumu = scrapy.Field()
    KullanimDurumu = scrapy.Field()
    Tapu = scrapy.Field()
    Takas = scrapy.Field()
    Cephe = scrapy.Field()
    KiraGetirisi = scrapy.Field()
    YakitTipi = scrapy.Field()

