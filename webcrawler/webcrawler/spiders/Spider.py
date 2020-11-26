import datetime
from urllib.parse import urljoin
import scrapy
from ..items import WebcrawlerItem
import pandas as pd

def turn_excel():
    try:
        d = pd.read_csv("item.csv")
        d = d[['IlanNo', 'Fiyat', 'YeniFiyat', 'Il', 'Ilce', 'Mahalle', 'IlanTarihi', 'GuncellemeTarihi', 'IlanDurumu',
               'YeniDurum', 'KonutSekli', 'OdaSayisi', 'M2','BulunduguKat', 'BinaYasi', 'Isinma', 'KatSayisi', 'Kredi',
               'Esya', 'BanyoSayisi', 'YapiTipi','YapiDurumu','KullanimDurumu', 'Tapu', 'Takas', 'Cephe','KiraGetirisi',
               'YakitTipi']]

        d.to_excel("item.xlsx", index=False)
    except:
        print("\"scrapy crawl hurriyetEmlak -o item.csv\" şeklinde terminale giriniz.")


def cmp(list, element):
    for i in list:
        if (i==element):
            return True
    return False

class Spider(scrapy.Spider):
    name = "hurriyetEmlak"
    start_urls = ["https://www.hurriyetemlak.com/canakkale-merkez-satilik?page=1"
                ]
    tabindex = 1

    def parse(self, response):

        base = "https://www.hurriyetemlak.com"
        links = response.css('.card-link').xpath("@href").extract()
        for link in links:
            link = urljoin(base,link)
            yield scrapy.Request(link,callback=self.parse_page)

        flag = response.css('section.pagination a')[-1].extract()
        flag = int(flag.split(sep="\"", maxsplit=2)[1])

        if(flag!=-1):
            Spider.tabindex+=1
            nextPage= "https://www.hurriyetemlak.com/canakkale-merkez-satilik?page={}".format(Spider.tabindex)
            yield scrapy.Request(nextPage,callback=self.parse)
        turn_excel()



    def parse_page(self, response):
        item = WebcrawlerItem()
        item_info = ['IlanNo', 'IlanDurumu', 'KonutSekli', 'OdaSayisi',
                     'M2', 'BulunduguKat', 'BinaYasi', 'Isinma',
                     'KatSayisi', 'Kredi', 'Esya', 'BanyoSayisi',
                     'YapiTipi', 'YapiDurumu', 'KullanimDurumu',
                     'Tapu', 'Takas', 'Cephe', 'KiraGetirisi', 'YakitTipi']

        site_info = ['İlan no', 'İlan Durumu', 'Konut Şekli', 'Oda + Salon Sayısı',
                     'Brüt / Net M2', 'Bulunduğu Kat', 'Bina Yaşı', 'Isınma Tipi',
                     'Kat Sayısı', 'Krediye Uygunluk', 'Eşya Durumu', 'Banyo Sayısı',
                     'Yapı Tipi', 'Yapının Durumu', 'Kullanım Durumu',
                     'Tapu Durumu', 'Takas', 'Cephe ', 'Kira Getirisi', 'Yakıt Tipi']

        an = datetime.datetime.now()
        item['IlanTarihi'] = str(an.day) + "." + str(an.month) + "." + str(an.year)
        price = response.css('div.right p::text').extract()
        item['Fiyat'] = price[0].replace("\n", "")

        all_head = response.css('div.det-title-bottom')
        list = all_head.css('li::text').extract()
        item['Il'] = list[0].replace("\n", "")
        item['Ilce'] = list[1].replace("\n", "")
        item['Mahalle'] = list[2].replace("\n", "")
        item['Fiyat'] = price[0].replace("\n", "")

        all_text = response.css('div.det-adv-info')
        list1 = all_text.css('span.txt::text').extract()    #İlanda Bulunan Özellikler
        list2 = all_text.css('span::text').extract()    #İlanda Bulunan Özellikler ve Verileri
        list2.pop(0)    #İlan Bilgileri
        j = 0
        for k,l in enumerate(site_info):
            if (cmp(list1, l)):
                if l == list2[j]:
                    item[item_info[k]] = list2[j + 1]
                    before = item_info[k]
                    j += 2
                    list1.pop(0)
                else:
                    if (list1[0] == list2[j]):  #İstemediğimiz özellikler
                        list1.pop(0)
                        while (list2[j] != l):
                            if (list1[0] == list2[j]):
                                list1.pop(0)
                            j += 1
                        item[item_info[k]] = list2[j + 1]
                        before = item_info[k]
                        j += 2
                        list1.pop(0)
                    else:   #İstediğimiz özellik birden fazla değere sahipken
                        while (True):
                            item[before] = item[before] + list2[j]
                            j += 1
                            if (list2[j] == l):
                                item[item_info[k]] = list2[j + 1]
                                before = item_info[k]
                                list1.pop(0)
                                j += 2
                                break
                            elif (list1[0] == list2[j]):
                                list1.pop(0)
                                while (l != list2[j]):
                                    j += 1
                                item[item_info[k]] = list2[j + 1]
                                before = item_info[k]
                                list1.pop(0)
                                j += 2
                                break
            else:
                item[item_info[k]] = ""
        yield item
