import scrapy
import datetime
import pandas as pd


def update(liste):
    if len(liste) == 4:
        d = pd.read_excel("item.xlsx")
        for k,l in d.iterrows():
            if (list(l)[0]==liste[0]):
                d.loc[k,"YeniFiyat"] = liste[1]
                d.loc[k,"YeniDurum"] = liste[2]
                d.loc[k,"GuncellemeTarihi"] = liste[3]
                break
        d.to_excel("item.xlsx",index=False)

def getIlanNo():
    d = pd.read_excel("item.xlsx")
    IlanNo = []
    for i in d['IlanNo']:
        IlanNo.append(i)
    return IlanNo

def getLinks():
    base = "https://www.hurriyetemlak.com/canakkale-merkez/daire/"
    Links = []
    IlanNo = getIlanNo()
    for i in IlanNo:
        Links.append(base + i)
    return Links

def getPriceState():

    d = pd.read_excel("item.xlsx")
    Fiyat = []
    Durum =[]
    IlanNo ={}
    Ilan= getIlanNo()
    for i in d['Fiyat']:
        Fiyat.append(i)
    for j in d['IlanDurumu']:
        Durum.append(j)
    for k,l in enumerate(Ilan):
        IlanNo[l] = [Fiyat[k],Durum[k]]
    return IlanNo


def cmp(f1,f2):
    f1 = f1.replace(" ", "")
    f2 = f2.replace(" ", "")
    if(len(f1)==len(f2)):
        for i,j in enumerate(f1):
            if j == f2[i]:
                continue
            return False
        return True
    else:
        return False



class Spider2(scrapy.Spider):
    name = "Guncelleme"
    try:
        Links = getLinks()
        start_urls = [Links[0]]
        IlanNo = getPriceState()

    except:
        pass
    Count = 0

    def parse(self, response):
        list = []
        x=response.css('.redy ::text').extract()
        list.append(x[0])
        PaS = Spider2.IlanNo.get(list[0])
        price = response.css('div.right p::text').extract()
        price = price[0].replace("\n","")
        Flag1 = cmp(price,PaS[0])

        state = response.css('.short-info-list li ::text')[3].extract()
        Flag2 = cmp(state,PaS[1])

        if (Flag1 == False or Flag2 == False):
            if Flag1 == False:
                list.append(price)
            else:
                list.append("")
            if Flag2 == False:
                list.append(state)
            else:
                list.append("")
            an = datetime.datetime.now()
            list.append(str(an.day) + "." + str(an.month) + "." + str(an.year))
        update(list)
        Spider2.Count +=1

        yield {'item': list}

        yield scrapy.Request(Spider2.Links[Spider2.Count],callback=self.parse)





