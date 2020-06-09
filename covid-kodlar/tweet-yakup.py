"""
    COVİD-19 salgını döneminde emek ihlalleri araştırması, taranan tweetlerin yorumlanması scripti,
    gereksiz yere harcadığım onca zamandan sonra şimdi oturup sabah kadar bu işi bitirmeye çalışacağım
    Aslı hocanın belki de hiç umudu yok :) .. ben Asla pes etmeyenlerdenim.. çok büyük konuşmadan işe girişelim derim ben :)
    16 Mayıs 2020 01:46
"""

import spacy
import bios
import csv
import re

diziler = {"iller":{},"ilçeler":{},"ihlal":{},"direniş":{},"covid şirket uygulama":{}}
ihlal_turleri = [None]
for i in zip(*csv.reader(open('covid_kaynak2.csv',"r"))):
    i = list(i)
    i = [x for x in i if x != '']
    diziler[i[0]][i[2]] = i[3:]
    if i[0] == "ihlal":
        ihlal_turleri.append(i[2])


# Multi language model dosyası eklendi.
nlp = spacy.load("xx_ent_wiki_sm")

dosya_ihlal = open("covid_sontweet.csv","w",encoding="utf-8")
yaz = csv.writer(dosya_ihlal)
yaz.writerow("link,firma,ana_firma,isyeri,is_kolu,ihlal_turu,covid_sirket_haber,covid_sirket_uygulama,tarih,il,ilce,ihlal_kaynak,direnis_var,direnis,siddet,direnis_Kaynak,PR,PR_Kaynak,ihlal_turu,ihlal_kelime,covid_sirket_uygulama,covid_sirket_uygulama,lokasyon,ozel_isim,buyuk_harfli".split(","))

with open('covidisci.csv') as dosya:
    oku = csv.reader(dosya, delimiter=",")
    # covid_tweet_temiz.csv dosyasında sadece tweet sekmesi okunacak.
    # spacy kullanarak isimleri bulmaya çalışacağım

    kontrol=0
    for satir in oku:
        print(kontrol, end="\r")
        kontrol += 1
        if kontrol <= 1:
            continue

        tweet_metin = satir[5] #.replace("I","ı").lower()
        tweet=nlp(tweet_metin)

        firma = []
        ana_firma = []
        is_kolu = []
        isyeri = []
        covid_sirket_haber = []
        covid_sirket_uygulama = []
        tarih = []
        il = []
        ilce = []
        ihlal_kaynak = []
        direnis_var = []
        direnis = []
        siddet = []
        direnis_Kaynak = []
        PR = []
        PR_Kaynak = []
        ihlal_turu = []
        ihlal_kelime = []
        covid_sirket_uygulama = []
        lokasyon = []
        ozel_isim = []
        buyuk_harfli = []

        for tanimlama in tweet.ents:
            etiket=tanimlama.label_
            if etiket=="ORG":
                isyeri.append(str(tanimlama.text))
            elif etiket=="LOC":
                lokasyon.append(str(tanimlama.text))
            elif etiket=="DATE":
                tarih.append(str(tanimlama.text))
            elif etiket in ["PER","MISC"]:
                ozel_isim.append(str(tanimlama.text))


        # tüm aramalar

        for genel_tur in diziler:
            for tur in diziler[genel_tur]:
                dizi = diziler[genel_tur][tur]
                for tekil in dizi:
                    if genel_tur == "ihlal":
                        if re.search(tekil,tweet_metin):
                            ihlal_kelime.append(tekil)
                            ihlal_turu.append(str(ihlal_turleri.index(tur)))
                    else:
                        x = eval(tur)
                        if re.search(tekil,tweet_metin):
                            x.append(tekil)

        # tüm büyük harfli kelimeleri bulur.
        kelimeler = satir[5].split(" ")
        for kelime in kelimeler:
            if re.findall("^[A-ZÇĞİÖŞÜ]+[a-zçğıöşü]*$",kelime.strip()):
                buyuk_harfli.append(kelime)


        degerler = ["firma","ana_firma","isyeri","is_kolu","ihlal_turu","covid_sirket_haber","covid_sirket_uygulama","tarih","il","ilce","ihlal_kaynak","direnis_var","direnis","siddet","direnis_Kaynak","PR","PR_Kaynak","ihlal_turu","ihlal_kelime","covid_sirket_uygulama","covid_sirket_uygulama","lokasyon","ozel_isim","buyuk_harfli"]

        yazilacak = [satir[14]]
        for deger in degerler:
            yazilacak.append("; ".join(eval(deger)))

        yaz.writerow(yazilacak)

