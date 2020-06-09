"""
    COVİD-19 salgını döneminde emek ihlalleri araştırması, taranan tweetlerin yorumlanması scripti,
    gereksiz yere harcadığım onca zamandan sonra şimdi oturup sabah kadar bu işi bitirmeye çalışacağım
    Aslı hocanın belki de hiç umudu yok :) .. ben Asla pes etmeyenlerdenim.. çok büyük konuşmadan işe girişelim derim ben :)
    16 Mayıs 2020 01:46
"""
import csv
import spacy
import bios
import re

"""
    DİZİLER tanımlanıyor,
    işlemlerin hızlı yapılması için diziler tanımladım en azından şimdilik sadece bunu biliyorum :)
    şimdilik :)
"""

# il ilçe isimleri
il_dizi = ["Adana","ADANA","ADIYAMAN","Adıyaman","Afyonkarahisar","AFYONKARAHİSAR","AGRI","Agrı","Aksaray","AKSARAY","Amasya","AMASYA","Ankara","ANKARA","Antalya","ANTALYA","Ardahan","ARDAHAN","Artvin","ARTVİN","AYDIN","Aydın","BALIKESİR","Balıkesir","BARTIN","Bartın","Batman","BATMAN","Bayburt","BAYBURT","Bilecik","BİLECİK","Bingol","BİNGOL","Bitlis","BİTLİS","Bolu","BOLU","Burdur","BURDUR","Bursa","BURSA","Canakkale","CANAKKALE","CANKIRI","Cankırı","Corum","CORUM","Denizli","DENİZLİ","DİYARBAKIR","Diyarbakır","Duzce","DUZCE","Edirne","EDİRNE","ELAZIG","Elazıg","Erzincan","ERZİNCAN","Erzurum","ERZURUM","Eskisehir","ESKİSEHİR","Gaziantep","GAZİANTEP","Giresun","GİRESUN","Gumushane","GUMUSHANE","Hakkari","HAKKARİ","Hatay","HATAY","IGDIR","Igdır","Isparta","ISPARTA","İstanbul","İSTANBUL","İzmir","İZMİR","Kahramanmaras","KAHRAMANMARAS","Karabuk","KARABUK","Karaman","KARAMAN","Kars","KARS","Kastamonu","KASTAMONU","Kayseri","KAYSERİ","Kilis","KİLİS","KIRIKKALE","KIRKLARELİ","KIRSEHİR","Kırıkkale","Kırklareli","Kırsehir","Kocaeli","KOCAELİ","Konya","KONYA","Kutahya","KUTAHYA","Malatya","MALATYA","Manisa","MANİSA","Mardin","MARDİN","Mersin","MERSİN","Mugla","MUGLA","Mus","MUS","Nevsehir","NEVSEHİR","Nigde","NİGDE","Ordu","ORDU","Osmaniye","OSMANİYE","Rize","RİZE","Sakarya","SAKARYA","Samsun","SAMSUN","SANLIURFA","Sanlıurfa","Siirt","SİİRT","Sinop","SİNOP","SIRNAK","Sivas","SİVAS","Sırnak","Tekirdag","TEKİRDAG","Tokat","TOKAT","Trabzon","TRABZON","Tunceli","TUNCELİ","Usak","USAK","Van","VAN","Yalova","YALOVA","Yozgat","YOZGAT","Zonguldak","ZONGULDAK"]

ilce_dizi = ["19 MAYIS","19 Mayıs","ABANA ","Abana ","ACIGÖL","ACIPAYAM","Acıgöl","Acıpayam","ADAKLI","Adaklı","ADALAR","Adalar","ADAPAZARI ","Adapazarı ","Adilcevaz ","ADİLCEVAZ ","Afşin ","AFŞİN ","AĞAÇÖREN","Ağaçören","AĞIN","Ağın","AĞLASUN ","Ağlasun ","AĞLI","Ağlı","AHIRLI","Ahırlı","AHLAT ","Ahlat ","Ahmetli ","AHMETLİ ","AKÇAABAT","Akçaabat","AKÇADAĞ ","Akçadağ ","AKÇAKALE","Akçakale","AKÇAKENT","Akçakent","AKÇAKOCA","Akçakoca","Akdağmadeni ","AKDAĞMADENİ ","Akdeniz ","AKDENİZ ","Akhisar ","AKHİSAR ","AKINCILAR ","Akıncılar ","AKKIŞLA ","Akkışla ","AKKUŞ ","Akkuş ","AKÖREN","Akören","AKPINAR ","Akpınar ","Akşehir ","AKŞEHİR ","Akseki","AKSEKİ","AKSU","Aksu","AKYAKA","Akyaka","AKYAZI","Akyazı","AKYURT","Akyurt","ALACA ","Alaca ","ALACAKAYA ","Alacakaya ","ALAÇAM","Alaçam","ALADAĞ","Aladağ","ALANYA","Alanya","ALAPLI","Alaplı","Alaşehir","ALAŞEHİR","Aliağa","ALİAĞA","ALMUS ","Almus ","ALPU","Alpu","ALTIEYLÜL ","ALTINDAĞ","ALTINEKİN ","ALTINORDU ","ALTINOVA","ALTINÖZÜ","ALTINTAŞ","ALTINYAYLA","Altıeylül ","Altındağ","Altınekin ","Altınordu ","Altınova","Altınözü","Altıntaş","Altınyayla","Altunhisar","ALTUNHİSAR","ALUCRA","Alucra","AMASRA","Amasra","ANAMUR","Anamur","ANDIRIN ","Andırın ","ANTAKYA ","Antakya ","ARABAN","Araban","ARAÇ","Araç","ARAKLI","Araklı","ARALIK","Aralık","Arapgir ","ARAPGİR ","ARDANUÇ ","Ardanuç ","ARDEŞEN ","Ardeşen ","ARGUVAN ","Arguvan ","Arhavi","ARHAVİ","ARICAK","Arifiye ","ARİFİYE ","Arıcak","ARMUTLU ","Armutlu ","ARNAVUTKÖY","Arnavutköy","ARPAÇAY ","Arpaçay ","Arsin ","ARSİN ","ARSUZ ","Arsuz ","ARTOVA","Artova","ARTUKLU ","Artuklu ","ASARCIK ","Asarcık ","AŞKALE","Aşkale","ASLANAPA","Aslanapa","ATABEY","Atabey","ATAKUM","Atakum","Ataşehir","ATAŞEHİR","ATKARACALAR ","Atkaracalar ","AVANOS","Avanos","AVCILAR ","Avcılar ","AYANCIK ","Ayancık ","AYAŞ","Ayaş","AYBASTI ","Aybastı ","AYDINCIK","AYDINTEPE ","Aydıncık","Aydıntepe ","AYRANCI ","Ayrancı ","AYVACIK ","Ayvacık ","AYVALIK ","Ayvalık ","AZDAVAY ","Azdavay ","Aziziye ","AZİZİYE ","BABADAĞ ","Babadağ ","Babaeski","BABAESKİ","BAFRA ","Bafra ","BAĞCILAR","Bağcılar","BAĞLAR","Bağlar","BAHÇE ","Bahçe ","Bahçelievler","BAHÇELİEVLER","BAHÇESARAY","Bahçesaray","BAHŞILI ","Bahşılı ","BAKIRKÖY","Bakırköy","BAKLAN","Baklan","BALA","Bala","BALÇOVA ","Balçova ","BALIŞEYH","Balışeyh","BALYA ","Balya ","BANAZ ","Banaz ","BANDIRMA","Bandırma","Başakşehir","BAŞAKŞEHİR","Başçiftlik","BAŞÇİFTLİK","Başiskele ","BAŞİSKELE ","BAŞKALE ","Başkale ","Baskil","BASKİL","BAŞMAKÇI","Başmakçı","BAŞYAYLA","Başyayla","Battalgazi","BATTALGAZİ","BAYAT ","Bayat ","BAYINDIR","Bayındır","BAYKAN","Baykan","BAYRAKLI","Bayraklı","Bayramiç","BAYRAMİÇ","BAYRAMÖREN","Bayramören","BAYRAMPAŞA","Bayrampaşa","Bekilli ","BEKİLLİ ","BELEN ","Belen ","BERGAMA ","Bergama ","Beşikdüzü ","BEŞİKDÜZÜ ","Beşiktaş","BEŞİKTAŞ","Beşiri","BEŞİRİ","Besni ","BESNİ ","BEYAĞAÇ ","Beyağaç ","BEYDAĞ","Beydağ","BEYKOZ","Beykoz","Beylikdüzü","BEYLİKDÜZÜ","Beylikova ","BEYLİKOVA ","BEYOĞLU ","Beyoğlu ","BEYPAZARI ","Beypazarı ","Beyşehir","BEYŞEHİR","BEYTÜŞŞEBAP ","Beytüşşebap ","Biga","BİGA","Bigadiç ","BİGADİÇ ","Birecik ","BİRECİK ","Bismil","BİSMİL","BODRUM","Bodrum","BOĞAZKALE ","Boğazkale ","BOĞAZLIYAN","Boğazlıyan","Bolvadin","BOLVADİN","BOR ","Bor ","BORÇKA","Borçka","BORNOVA ","Bornova ","BOYABAT ","Boyabat ","BOZCAADA","Bozcaada","BOZDOĞAN","Bozdoğan","BOZKIR","Bozkır","BOZKURT ","Bozkurt ","BOZOVA","Bozova","BOZTEPE ","Boztepe ","BOZÜYÜK ","Bozüyük ","BOZYAZI ","Bozyazı ","BUCA","Buca","BUCAK ","Bucak ","BUHARKENT ","Buharkent ","BULANCAK","Bulancak","BULANIK ","Bulanık ","BULDAN","Buldan","BÜNYAN","Bünyan","Burhaniye ","BURHANİYE ","BÜYÜKÇEKMECE","Büyükçekmece","BÜYÜKORHAN","Büyükorhan","Çağlayancerit ","ÇAĞLAYANCERİT ","ÇAL ","Çal ","ÇALDIRAN","Çaldıran","ÇAMARDI ","Çamardı ","ÇAMAŞ ","Çamaş ","Çameli","ÇAMELİ","ÇAMLIDERE ","ÇAMLIHEMŞİN ","ÇAMLIYAYLA","Çamlıdere ","Çamlıhemşin ","Çamlıyayla","ÇAMOLUK ","Çamoluk ","ÇAN ","Çan ","ÇANAKÇI ","Çanakçı ","ÇANDIR","Çandır","Canik ","CANİK ","ÇANKAYA ","Çankaya ","ÇARDAK","Çardak","ÇARŞAMBA","Çarşamba","ÇARŞIBAŞI ","Çarşıbaşı ","ÇAT ","Çat ","ÇATAK ","Çatak ","ÇATALCA ","Çatalca ","ÇATALPINAR","Çatalpınar","Çatalzeytin ","ÇATALZEYTİN ","Çavdarhisar ","ÇAVDARHİSAR ","ÇAVDIR","Çavdır","ÇAY ","Çay ","ÇAYBAŞI ","Çaybaşı ","ÇAYCUMA ","Çaycuma ","Çayeli","ÇAYELİ","ÇAYIRALAN ","ÇAYIRLI ","ÇAYIROVA","Çayıralan ","Çayırlı ","Çayırova","ÇAYKARA ","Çaykara ","ÇEKEREK ","Çekerek ","ÇEKMEKÖY","Çekmeköy","Çelebi","ÇELEBİ","Çelikhan","ÇELİKHAN","Çeltik","ÇELTİK","Çeltikçi","ÇELTİKÇİ","Çemişgezek","ÇEMİŞGEZEK","ÇERKEŞ","Çerkeş","ÇERKEZKÖY ","Çerkezköy ","Çermik","ÇERMİK","ÇEŞME ","Çeşme ","CEYHAN","Ceyhan","CEYLANPINAR ","Ceylanpınar ","ÇİÇEKDAĞI ","Çiçekdağı ","Cide","CİDE","Çifteler","ÇİFTELER","Çiftlik ","ÇİFTLİK ","Çiftlikköy","ÇİFTLİKKÖY","Çiğli ","ÇİĞLİ ","Cihanbeyli","CİHANBEYLİ","ÇILDIR","Çilimli ","ÇİLİMLİ ","ÇINAR ","ÇINARCIK","Çine","ÇİNE","Çivril","ÇİVRİL","Cizre ","CİZRE ","Çıldır","Çınar ","Çınarcık","ÇOBANLAR","Çobanlar","ÇORLU ","Çorlu ","ÇUBUK ","Çubuk ","ÇUKURCA ","Çukurca ","ÇUKUROVA","Çukurova","Cumayeri","CUMAYERİ","ÇUMRA ","Çumra ","ÇÜNGÜŞ","Çüngüş","DADAY ","Daday ","DALAMAN ","Dalaman ","DAMAL ","Damal ","DARENDE ","Darende ","Dargeçit","DARGEÇİT","DARICA","Darıca","DATÇA ","Datça ","DAZKIRI ","Dazkırı ","DEFNE ","Defne ","Delice","DELİCE","Demirci ","DEMİRCİ ","Demirköy","DEMİRKÖY","Demirözü","DEMİRÖZÜ","DEMRE ","Demre ","DERBENT ","Derbent ","DEREBUCAK ","Derebucak ","Derecik ","DERECİK ","Dereli","DERELİ","DEREPAZARI","Derepazarı","Derik ","DERİK ","Derince ","DERİNCE ","Derinkuyu ","DERİNKUYU ","DERNEKPAZARI","Dernekpazarı","Develi","DEVELİ","DEVREK","Devrek","Devrekani ","DEVREKANİ ","Dicle ","DİCLE ","Didim ","DİDİM ","Digor ","DİGOR ","Dikili","DİKİLİ","Dikmen","DİKMEN","DİLOVASI","Dilovası","Dinar ","DİNAR ","Divriği ","DİVRİĞİ ","Diyadin ","DİYADİN ","DODURGA ","Dodurga ","Doğanhisar","DOĞANHİSAR","DOĞANKENT ","Doğankent ","DOĞANŞAR","Doğanşar","Doğanşehir","DOĞANŞEHİR","DOĞANYOL","Doğanyol","DOĞANYURT ","Doğanyurt ","DOĞUBAYAZIT ","Doğubayazıt ","Domaniç ","DOMANİÇ ","Dörtdivan ","DÖRTDİVAN ","DÖRTYOL ","Dörtyol ","DÖŞEMEALTI","Döşemealtı","Dulkadiroğlu","DULKADİROĞLU","DUMLUPINAR","Dumlupınar","DURAĞAN ","Durağan ","DURSUNBEY ","Dursunbey ","Düziçi","DÜZİÇİ","DÜZKÖY","Düzköy","ECEABAT ","Eceabat ","Edremit ","EDREMİT ","EFELER","Efeler","Eflani","EFLANİ","Eğil","EĞİL","Eğirdir ","EĞİRDİR ","Ekinözü ","EKİNÖZÜ ","Elbeyli ","ELBEYLİ ","Elbistan","ELBİSTAN","Eldivan ","ELDİVAN ","Eleşkirt","ELEŞKİRT","ELMADAĞ ","Elmadağ ","ELMALI","Elmalı","EMET","Emet","Emirdağ ","EMİRDAĞ ","Emirgazi","EMİRGAZİ","ENEZ","Enez","ERBAA ","Erbaa ","Erciş ","ERCİŞ ","ERDEK ","Erdek ","Erdemli ","ERDEMLİ ","Ereğli","EREĞLİ","ERENLER ","Erenler ","ERFELEK ","Erfelek ","Ergani","ERGANİ","ERGENE","Ergene","ERMENEK ","Ermenek ","ERUH","Eruh","Erzin ","ERZİN ","ESENLER ","Esenler ","ESENYURT","Esenyurt","Eskil ","ESKİL ","Eskipazar ","ESKİPAZAR ","EŞME","Eşme","Espiye","ESPİYE","Etimesgut ","ETİMESGUT ","Evciler ","EVCİLER ","EVREN ","Evren ","Eynesil ","EYNESİL ","EYÜPSULTAN","Eyüpsultan","Eyyübiye","EYYÜBİYE","Ezine ","EZİNE ","Fatih ","FATİH ","FATSA ","Fatsa ","FEKE","Feke","Felahiye","FELAHİYE","Ferizli ","FERİZLİ ","Fethiye ","FETHİYE ","FINDIKLI","Finike","FİNİKE","Fındıklı","FOÇA","Foça","Gaziemir","GAZİEMİR","Gaziosmanpaşa ","GAZİOSMANPAŞA ","Gazipaşa","GAZİPAŞA","GEBZE ","Gebze ","Gediz ","GEDİZ ","GELENDOST ","Gelendost ","Gelibolu","GELİBOLU","GEMEREK ","Gemerek ","Gemlik","GEMLİK","GENÇ","Genç","GERCÜŞ","Gercüş","GEREDE","Gerede","GERGER","Gerger","Germencik ","GERMENCİK ","GERZE ","Gerze ","GEVAŞ ","Gevaş ","GEYVE ","Geyve ","GÖKÇEADA","Gökçeada","GÖKÇEBEY","Gökçebey","GÖKSUN","Göksun","GÖLBAŞI ","Gölbaşı ","GÖLCÜK","Gölcük","GÖLE","Göle","Gölhisar","GÖLHİSAR","GÖLKÖY","Gölköy","GÖLMARMARA","Gölmarmara","GÖLOVA","Gölova","GÖLPAZARI ","Gölpazarı ","GÖLYAKA ","Gölyaka ","GÖMEÇ ","Gömeç ","GÖNEN ","Gönen ","GÖRDES","Gördes","GÖRELE","Görele","GÖYNÜCEK","Göynücek","GÖYNÜK","Göynük","GÜCE","Güce","GÜÇLÜKONAK","Güçlükonak","GÜDÜL ","Güdül ","GÜLAĞAÇ ","Gülağaç ","GÜLNAR","Gülnar","Gülşehir","GÜLŞEHİR","GÜLYALI ","Gülyalı ","GÜMÜŞHACIKÖY","Gümüşhacıköy","GÜMÜŞOVA","Gümüşova","GÜNDOĞMUŞ ","Gündoğmuş ","GÜNEY ","Güney ","GÜNEYSINIR","Güneysınır","GÜNEYSU ","Güneysu ","GÜNGÖREN","Güngören","GÜNYÜZÜ ","Günyüzü ","GÜRGENTEPE","Gürgentepe","GÜROYMAK","Güroymak","GÜRPINAR","Gürpınar","GÜRSU ","Gürsu ","GÜRÜN ","Gürün ","GÜZELBAHÇE","Güzelbahçe","GÜZELYURT ","Güzelyurt ","HACIBEKTAŞ","HACILAR ","Hacıbektaş","Hacılar ","Hadim ","HADİM ","Hafik ","HAFİK ","Halfeti ","HALFETİ ","Haliliye","HALİLİYE","HALKAPINAR","Halkapınar","HAMAMÖZÜ","Hamamözü","HAMUR ","Hamur ","HAN ","Han ","HANAK ","Hanak ","Hani","HANİ","HANÖNÜ","Hanönü","HARMANCIK ","Harmancık ","HARRAN","Harran","Hasanbeyli","HASANBEYLİ","HASANKEYF ","Hasankeyf ","HASKÖY","Hasköy","HASSA ","Hassa ","HAVRAN","Havran","HAVSA ","Havsa ","HAVZA ","Havza ","HAYMANA ","Haymana ","HAYRABOLU ","Hayrabolu ","HAYRAT","Hayrat","HAZRO ","Hazro ","Hekimhan","HEKİMHAN","Hemşin","HEMŞİN","HENDEK","Hendek","Hilvan","HİLVAN","HINIS ","HİSARCIK","Hisarcık","Hizan ","HİZAN ","Hınıs ","HOCALAR ","Hocalar ","HONAZ ","Honaz ","HOPA","Hopa","HORASAN ","Horasan ","HOZAT ","Hozat ","HÜYÜK ","Hüyük ","İBRADI","İbradı","İdil","İDİL","İhsangazi ","İHSANGAZİ ","İhsaniye","İHSANİYE","İkizce","İKİZCE","İkizdere","İKİZDERE","ILGAZ ","Ilgaz ","ILGIN ","Ilgın ","İliç","İLİÇ","İLKADIM ","İlkadım ","İMAMOĞLU","İmamoğlu","İMRANLI ","İmranlı ","İNCESU","İncesu","İncirliova","İNCİRLİOVA","İNEBOLU ","İnebolu ","İNEGÖL","İnegöl","İnhisar ","İNHİSAR ","İNÖNÜ ","İnönü ","İPEKYOLU","İpekyolu","İPSALA","İpsala","İscehisar ","İSCEHİSAR ","İSKENDERUN","İskenderun","İskilip ","İSKİLİP ","İslahiye","İSLAHİYE","İspir ","İSPİR ","İvrindi ","İVRİNDİ ","İyidere ","İYİDERE ","İzmit ","İZMİT ","İznik ","İZNİK ","KABADÜZ ","Kabadüz ","KABATAŞ ","Kabataş ","KADIKÖY ","KADINHANI ","Kadirli ","KADİRLİ ","KADIŞEHRİ ","Kadıköy ","Kadınhanı ","Kadışehri ","KAĞITHANE ","KAĞIZMAN","Kağıthane ","Kağızman","KAHRAMANKAZAN ","Kahramankazan ","KAHTA ","Kahta ","KALE","Kale","Kalecik ","KALECİK ","KALKANDERE","Kalkandere","KAMAN ","Kaman ","KANDIRA ","Kandıra ","KANGAL","Kangal","KAPAKLI ","Kapaklı ","KARABAĞLAR","Karabağlar","KARABURUN ","Karaburun ","KARACABEY ","Karacabey ","KARACASU","Karacasu","KARAÇOBAN ","Karaçoban ","KARAHALLI ","Karahallı ","KARAİSALI ","Karaisalı ","Karakeçili","KARAKEÇİLİ","KARAKOÇAN ","Karakoçan ","KARAKÖPRÜ ","Karaköprü ","KARAKOYUNLU ","Karakoyunlu ","KARAMANLI ","Karamanlı ","KARAMÜRSEL","Karamürsel","KARAPINAR ","Karapınar ","KARAPÜRÇEK","Karapürçek","KARASU","Karasu","KARATAŞ ","Karataş ","KARATAY ","Karatay ","KARAYAZI","Karayazı","Karesi","KARESİ","KARGI ","Kargı ","KARKAMIŞ","Karkamış","KARLIOVA","Karlıova","KARPUZLU","Karpuzlu","KARŞIYAKA ","Karşıyaka ","KARTAL","Kartal","KARTEPE ","Kartepe ","KAŞ ","Kaş ","KAVAK ","Kavak ","KAVAKLIDERE ","Kavaklıdere ","KAYAPINAR ","Kayapınar ","KAYNARCA","Kaynarca","KAYNAŞLI","Kaynaşlı","KAZIMKARABEKİR","Kazımkarabekir","KEBAN ","Keban ","Keçiborlu ","KEÇİBORLU ","Keçiören","KEÇİÖREN","KELES ","Keles ","Kelkit","KELKİT","KEMAH ","Kemah ","Kemaliye","KEMALİYE","KEMALPAŞA ","Kemalpaşa ","KEMER ","Kemer ","KEPEZ ","Kepez ","KEPSUT","Kepsut","KEŞAN ","Keşan ","KEŞAP ","Keşap ","Keskin","KESKİN","KESTEL","Kestel","KIBRISCIK ","KİĞI","Kiğı","Kilimli ","KİLİMLİ ","KINIK ","Kiraz ","KİRAZ ","KIRIKHAN","KIRKAĞAÇ","KIZILCAHAMAM","KIZILIRMAK","KIZILÖREN ","KIZILTEPE ","Kıbrıscık ","Kınık ","Kırıkhan","Kırkağaç","Kızılcahamam","Kızılırmak","Kızılören ","Kızıltepe ","Kocaali ","KOCAALİ ","KOCAKÖY ","Kocaköy ","KOÇARLI ","Koçarlı ","Kocasinan ","KOCASİNAN ","KOFÇAZ","Kofçaz","KONAK ","Konak ","KONYAALTI ","Konyaaltı ","KÖPRÜBAŞI ","Köprübaşı ","KÖPRÜKÖY","Köprüköy","KÖRFEZ","Körfez","KORGAN","Korgan","KORGUN","Korgun","KORKUT","Korkut","Korkuteli ","KORKUTELİ ","KÖSE","Köse","KÖŞK","Köşk","KOVANCILAR","Kovancılar","Köyceğiz","KÖYCEĞİZ","Koyulhisar","KOYULHİSAR","KOZAKLI ","Kozaklı ","KOZAN ","Kozan ","KOZLU ","Kozlu ","KOZLUK","Kozluk","KÜÇÜKÇEKMECE","Küçükçekmece","KULA","Kula","KULP","Kulp","KULU","Kulu","KULUNCAK","Kuluncak","KUMLU ","Kumlu ","KUMLUCA ","Kumluca ","KUMRU ","Kumru ","KÜRE","Küre","KURŞUNLU","Kurşunlu","KURTALAN","Kurtalan","KÜRTÜN","Kürtün","Kurucaşile","KURUCAŞİLE","KUŞADASI","Kuşadası","KUYUCAK ","Kuyucak ","Laçin ","LAÇİN ","Ladik ","LADİK ","LALAPAŞA","Lalapaşa","Lapseki ","LAPSEKİ ","Lice","LİCE","LÜLEBURGAZ","Lüleburgaz","MAÇKA ","Maçka ","MADEN ","Maden ","Mahmudiye ","MAHMUDİYE ","Malazgirt ","MALAZGİRT ","MALKARA ","Malkara ","MALTEPE ","Maltepe ","MAMAK ","Mamak ","MANAVGAT","Manavgat","MANYAS","Manyas","MARMARA ","Marmara ","Marmaraereğlisi ","MARMARAEREĞLİSİ ","Marmaris","MARMARİS","Mazgirt ","MAZGİRT ","MAZIDAĞI","Mazıdağı","Mecitözü","MECİTÖZÜ","Melikgazi ","MELİKGAZİ ","MENDERES","Menderes","MENEMEN ","Menemen ","MENGEN","Mengen","MENTEŞE ","Menteşe ","MERAM ","Meram ","Meriç ","MERİÇ ","MERKEZ","Merkez","Merkezefendi","MERKEZEFENDİ","Merzifon","MERZİFON","Mesudiye","MESUDİYE","Mezitli ","MEZİTLİ ","Midyat","MİDYAT","Mihalgazi ","MİHALGAZİ ","MİHALIÇÇIK","Mihalıççık","Milas ","MİLAS ","MUCUR ","Mucur ","MUDANYA ","Mudanya ","MUDURNU ","Mudurnu ","Muradiye","MURADİYE","MURATLI ","Muratlı ","MURATPAŞA ","Muratpaşa ","MURGUL","Murgul","Musabeyli ","MUSABEYLİ ","MUSTAFAKEMALPAŞA","Mustafakemalpaşa","MUT ","Mut ","Mutki ","MUTKİ ","NALLIHAN","Nallıhan","NARLIDERE ","Narlıdere ","NARMAN","Narman","Nazilli ","NAZİLLİ ","NAZIMİYE","Nazımiye","Niksar","NİKSAR","Nilüfer ","NİLÜFER ","Nizip ","NİZİP ","NURDAĞI ","Nurdağı ","NURHAK","Nurhak","Nusaybin","NUSAYBİN","Ödemiş","ÖDEMİŞ","ODUNPAZARI","Odunpazarı","OF","Of","Oğuzeli ","OĞUZELİ ","OĞUZLAR ","Oğuzlar ","OLTU","Oltu","OLUR","Olur","Ömerli","ÖMERLİ","Onikişubat","ONİKİŞUBAT","Orhaneli","ORHANELİ","Orhangazi ","ORHANGAZİ ","ORTA","Orta","ORTACA","Ortaca","Ortahisar ","ORTAHİSAR ","ORTAKÖY ","Ortaköy ","OSMANCIK","Osmancık","Osmaneli","OSMANELİ","Osmangazi ","OSMANGAZİ ","Otlukbeli ","OTLUKBELİ ","OVACIK","Ovacık","ÖZALP ","Özalp ","ÖZVATAN ","Özvatan ","PALANDÖKEN","Palandöken","PALU","Palu","PAMUKKALE ","Pamukkale ","PAMUKOVA","Pamukova","Pasinler","PASİNLER","PATNOS","Patnos","PAYAS ","Payas ","PAZAR ","Pazar ","PAZARCIK","Pazarcık","PAZARLAR","Pazarlar","Pazaryeri ","PAZARYERİ ","PAZARYOLU ","Pazaryolu ","Pehlivanköy ","PEHLİVANKÖY ","Pendik","PENDİK","PERŞEMBE","Perşembe","PERTEK","Pertek","Pervari ","PERVARİ ","PINARBAŞI ","PINARHİSAR","Piraziz ","PİRAZİZ ","Pınarbaşı ","Pınarhisar","Polateli","POLATELİ","POLATLI ","Polatlı ","POSOF ","Posof ","POZANTI ","Pozantı ","PÜLÜMÜR ","Pülümür ","PURSAKLAR ","Pursaklar ","PÜTÜRGE ","Pütürge ","Refahiye","REFAHİYE","Reşadiye","REŞADİYE","REYHANLI","Reyhanlı","ŞABANÖZÜ","Şabanözü","SAFRANBOLU","Safranbolu","Şahinbey","ŞAHİNBEY","Saimbeyli ","SAİMBEYLİ ","Salihli ","SALİHLİ ","SALIPAZARI","Salıpazarı","ŞALPAZARI ","Şalpazarı ","SAMANDAĞ","Samandağ","SAMSAT","Samsat","SANCAKTEPE","Sancaktepe","SANDIKLI","Sandıklı","SAPANCA ","Sapanca ","ŞAPHANE ","Şaphane ","SARAY ","Saray ","SARAYDÜZÜ ","Saraydüzü ","SARAYKENT ","Saraykent ","SARAYKÖY","Sarayköy","SARAYÖNÜ","Sarayönü","SARICAKAYA","SARIÇAM ","SARIGÖL ","SARIKAMIŞ ","SARIKAYA","SARIOĞLAN ","SARIVELİLER ","SARIYAHŞİ ","SARIYER ","SARIZ ","Sarıcakaya","Sarıçam ","Sarıgöl ","Sarıkamış ","Sarıkaya","Sarıoğlan ","Sarıveliler ","Sarıyahşi ","Sarıyer ","Sarız ","Şarkikaraağaç ","ŞARKİKARAAĞAÇ ","ŞARKIŞLA","Şarkışla","ŞARKÖY","Şarköy","SARUHANLI ","Saruhanlı ","SASON ","Sason ","SAVAŞTEPE ","Savaştepe ","ŞAVŞAT","Şavşat","SAVUR ","Savur ","SEBEN ","Seben ","Şebinkarahisar","ŞEBİNKARAHİSAR","Şefaatli","ŞEFAATLİ","Seferihisar ","SEFERİHİSAR ","Şehitkamil","ŞEHİTKAMİL","ŞEHZADELER","Şehzadeler","SELÇUK","Selçuk","SELÇUKLU","Selçuklu","Selendi ","SELENDİ ","Selim ","SELİM ","Şemdinli","ŞEMDİNLİ","Senirkent ","SENİRKENT ","ŞENKAYA ","Şenkaya ","ŞENPAZAR","Şenpazar","Serdivan","SERDİVAN","Şereflikoçhisar ","ŞEREFLİKOÇHİSAR ","Serik ","SERİK ","Serinhisar","SERİNHİSAR","Seydikemer","SEYDİKEMER","Seydiler","SEYDİLER","Seydişehir","SEYDİŞEHİR","SEYHAN","Seyhan","Seyitgazi ","SEYİTGAZİ ","Şile","ŞİLE","Silifke ","SİLİFKE ","Silivri ","SİLİVRİ ","Silopi","SİLOPİ","Silvan","SİLVAN","Simav ","SİMAV ","Sinanpaşa ","SİNANPAŞA ","Sincan","SİNCAN","Sincik","SİNCİK","SINDIRGI","Şiran ","ŞİRAN ","Şirvan","ŞİRVAN","Şişli ","ŞİŞLİ ","SİVASLI ","Sivaslı ","Siverek ","SİVEREK ","Sivrice ","SİVRİCE ","Sivrihisar","SİVRİHİSAR","Sındırgı","SÖĞÜT ","Söğüt ","SÖĞÜTLÜ ","Söğütlü ","SÖKE","Söke","SOLHAN","Solhan","SOMA","Soma","SORGUN","Sorgun","ŞUHUT ","Şuhut ","SULAKYURT ","Sulakyurt ","SÜLEYMANPAŞA","Süleymanpaşa","SÜLOĞLU ","Süloğlu ","Sultanbeyli ","SULTANBEYLİ ","SULTANDAĞI","Sultandağı","Sultangazi","SULTANGAZİ","SULTANHANI","Sultanhanı","Sultanhisar ","SULTANHİSAR ","SULUOVA ","Suluova ","SULUSARAY ","Sulusaray ","SUMBAS","Sumbas","SUNGURLU","Sungurlu","SUR ","Sur ","SÜRMENE ","Sürmene ","SURUÇ ","Suruç ","Suşehri ","SUŞEHRİ ","SUSURLUK","Susurluk","SUSUZ ","Susuz ","SÜTÇÜLER","Sütçüler","TALAS ","Talas ","TARAKLI ","Taraklı ","TARSUS","Tarsus","TAŞKENT ","Taşkent ","TAŞKÖPRÜ","Taşköprü","TAŞLIÇAY","Taşlıçay","TAŞOVA","Taşova","TATVAN","Tatvan","TAVAS ","Tavas ","TAVŞANLI","Tavşanlı","Tefenni ","TEFENNİ ","TEKKEKÖY","Tekkeköy","TEKMAN","Tekman","TEPEBAŞI","Tepebaşı","TERCAN","Tercan","TERMAL","Termal","TERME ","Terme ","Tillo ","TİLLO ","Tire","TİRE","Tirebolu","TİREBOLU","TOMARZA ","Tomarza ","TONYA ","Tonya ","TOPRAKKALE","Toprakkale","TORBALI ","Torbalı ","TOROSLAR","Toroslar","TORTUM","Tortum","TORUL ","Torul ","TOSYA ","Tosya ","Tufanbeyli","TUFANBEYLİ","TURGUTLU","Turgutlu","TURHAL","Turhal","Türkeli ","TÜRKELİ ","TÜRKOĞLU","Türkoğlu","TUŞBA ","Tuşba ","TUT ","Tut ","TUTAK ","Tutak ","TUZLA ","Tuzla ","TUZLUCA ","Tuzluca ","TUZLUKÇU","Tuzlukçu","UĞURLUDAĞ ","Uğurludağ ","ULA ","Ula ","ULAŞ","Ulaş","ULUBEY","Ulubey","ULUBORLU","Uluborlu","ULUDERE ","Uludere ","ULUKIŞLA","Ulukışla","ULUS","Ulus","Ümraniye","ÜMRANİYE","ÜNYE","Ünye","ÜRGÜP ","Ürgüp ","URLA","Urla","ÜSKÜDAR ","Üsküdar ","ÜZÜMLÜ","Üzümlü","UZUNDERE","Uzundere","UZUNKÖPRÜ ","Uzunköprü ","VAKFIKEBİR","Vakfıkebir","VARTO ","Varto ","Vezirköprü","VEZİRKÖPRÜ","Viranşehir","VİRANŞEHİR","Vize","VİZE","YAĞLIDERE ","Yağlıdere ","Yahşihan","YAHŞİHAN","YAHYALI ","Yahyalı ","YAKAKENT","Yakakent","Yakutiye","YAKUTİYE","YALIHÜYÜK ","Yalıhüyük ","YALVAÇ","Yalvaç","YAPRAKLI","Yapraklı","YATAĞAN ","Yatağan ","Yavuzeli","YAVUZELİ","YAYLADAĞI ","Yayladağı ","YAYLADERE ","Yayladere ","YAZIHAN ","Yazıhan ","Yedisu","YEDİSU","Yeniçağa","YENİÇAĞA","Yenice","YENİCE","YENİFAKILI","Yenifakılı","Yenimahalle ","YENİMAHALLE ","Yenipazar ","YENİPAZAR ","Yenişarbademli","YENİŞARBADEMLİ","Yenişehir ","YENİŞEHİR ","YERKÖY","Yerköy","Yeşilhisar","YEŞİLHİSAR","Yeşilli ","YEŞİLLİ ","Yeşilova","YEŞİLOVA","Yeşilyurt ","YEŞİLYURT ","YIĞILCA ","YILDIRIM","YILDIZELİ ","Yığılca ","Yıldırım","Yıldızeli ","YOMRA ","Yomra ","YÜKSEKOVA ","Yüksekova ","YUMURTALIK","Yumurtalık","YUNAK ","Yunak ","YUNUSEMRE ","Yunusemre ","Yüreğir ","YÜREĞİR ","Yusufeli","YUSUFELİ","ZARA","Zara","Zeytinburnu ","ZEYTİNBURNU ","Zile","ZİLE"]

# İhlal türleri dizisi
ihlal_turleri = ["İşten çıkarma","İş güvenliğini almadan çalışmaya zorlama","İşyerinde pozitif vaka görülmesine rağmen çalışmaya zorlama ","Senelik izinden kullanmaya zorlama / izin borçlandırma","Ücretsiz izne zorlama","Ödenmemiş fazla mesai, iş yoğunluğunu artırma, ek iş kalemi çıkarma","Ücretlerini geciktirme / ödememe / eksik ödeme ","Yemek, sigorta, ulaşım haklarında kısıtlama","TİS haklarında kısıtlama ","Emekli olmaya zorlama","Sokağa çıkma yasağına rağmen çalışmaya devam etme"]
isten_cikarma = ["atıldı","işten Çıkarıldı","işten Çıkardı","İşten atıldı"]
zorla_calistirma = ["Covid19 önlemi","Korona Önlemi","salgına karşı önlem","kuyrukta önlem","test yapılmadı","tam donanımlı ekipmanları olmadan","maske verilmeden","maske verilmediğini","çalışma alanlarının dezenfekte","önlem almadan","alınmayan önlemler","verilmeyen maske","koğuş","yemekhane","kuyruk","maske","dezenfekte","önlem alınmıyor","iş güvenliğinin olmadığını","iş güvenliği yok","servisler"]
pozitif_vaka = ["testinin pozitif çıktığını fakat çalışmaya devam ettiklerini","Pozitif Vaka Çıkan İş Yerleri","COVİD-19'a yakalandı, çalışma devam ediyor","çalışma devam ediyor"]
senelik_izin = ["senelik izin"]
ucretsiz_izin = ["ücretsiz izin formu imzalatılıyor","ücretsiz izin","ücretsiz izne çıkardı","izin yaptırılıyor"]
angarya = ["mola kullanmadan","çalışma saatleri artırıldı","fazla mesai","zorla çalıştırıldıkları","siparişleri yürüyerek teslim","saat fazla çalıştırılma","fazla çalıştırma","iş yoğunluğu","hafta sonu zorla","ek iş"]
eksik_odeme = ["ödeme yapılmıyor","ödenmeyen ücretleri","maaşlardan düşürülüyor","nöbet ücretlerini","haklarını alamadıkları"]
sosyal_haklar = ["yemek parası ","yol parası","öğünde"]
tis = ["TİS","toplu iş sözleşmesi","emekli olmaya"]
emekli_edilme = ["emekli olmaya"]
sokaga_cikma = ["sokağa çıkma yasağı","sokağa çıkma yasağına rağmen","Sokağa çıkma yasağında da çalıştık","Şantiyede yatılı çalıştırma","özel çalışma izni"]

# direniş
direnis_dizi=["eylem yaptılar","iş bıraktı","işi durdurdu","yakın tehlike","direnmeye","isyan","işçiler üretimi durdurdu","direniş","şantiyeyi durdurdu","kaçınma hakkını","işçiler çalışmak istemeyince","iş durduran işçiler","işçiler durdurdu"]

# sirket uygulamaları
sirket_uygulama=["Üretime ara verildi","Evden çalışma ","Kısa çalışma ödeneği başvurusu","K.Ç.Ö","Ücretsiz izne çıkartıldı","Yıllık iznini kullandırma","Dönüşümlü çalışma","Faaliyet alanını değiştirme","E-ticaret'e","Ek işçi istihdam"]

# Multi language model dosyası eklendi.
nlp = spacy.load("xx_ent_wiki_sm")

# bos="firma;ana_firmaisyeri;is_kolu;ihlal_turu;covid_sirket_haber;covid_sirket_uygulama;tarih;il_ilce;ihlal_kaynak;direnis;direnis_Kaynak;ihlal_kelime;ozel_isim"
dosya = open("covid_ihlal.csv","w",encoding="utf-8")
dosya.write("firma,ana_firma,isyeri,is_kolu,ihlal_turu,covid_sirket_haber,covid_sirket_uygulama,tarih,il,ilce,ihlal_kaynak,direnis_var,direnis,siddet,direnis_Kaynak,PR,PR_Kaynak,ihlal_turu,ihlal_kelime,covid_sirket_uygulama,covid_sirket_uygulama,lokasyon,ozel_isim,buyuk_harfli\n")

with open('covid_tweet_temiz.csv') as dosya:
    oku = csv.reader(dosya, delimiter=";")
# covid_tweet_temiz.csv dosyasında sadece tweet sekmesi okunacak.
# spacy kullanarak isimleri bulmaya çalışacağım
    kontrol=0
    for satir in oku:
        tweet=nlp(satir[5])
        firma=ana_firma=is_kolu=isyeri=ihlal_turu=covid_sirket_haber=covid_sirket_uygulama=tarih=il=ilce=ihlal_kaynak=direnis_var=direnis=siddet=direnis_Kaynak=PR=PR_Kaynak=ihlal_turu=ihlal_kelime=covid_sirket_uygulama=covid_sirket_uygulama=lokasyon=ozel_isim=buyuk_harfli=""

        for tanimlama in tweet.ents:
            etiket=tanimlama.label_
            if etiket=="ORG":
                isyeri+=str(tanimlama.text)+';'
            elif etiket=="LOC":
                lokasyon+=str(tanimlama.text)+';'
            elif etiket=="DATE":
                tarih+=str(tanimlama.text)+';'
            elif etiket=="PER":
                #isim+=str(tanimlama.text)+','
                ozel_isim+=str(tanimlama.text)+';'
            elif etiket=="MISC":
                #unvan+=str(tanimlama.text)+','
                ozel_isim+=str(tanimlama.text)+';'


# il ilçe arar
        il=""
        il_var=0
        for il_ara in il_dizi:
            il_varmi = re.search(str(il_ara),satir[5])
            if il_varmi:
                il+=il_ara+';'
                il_var=1

        if il_var==0:
            il=""

        ilce=""
        ilce_var=0
        for ilce_ara in ilce_dizi:
            ilce_varmi = re.search(str(ilce_ara),satir[5])
            if ilce_varmi:
                ilce+=ilce_ara+';'
                ilce_var=1

        if ilce_var==0:
            ilce=""

# ihlal araştırması
        ihlal_var=direnis_var=covid_sirket_uygulama_var=0

        for isten_cikarma_ara in isten_cikarma:
            isten_cikarma_varmi = re.search(str(isten_cikarma_ara),satir[5])
            if isten_cikarma_varmi:
                ihlal_kelime+=isten_cikarma_ara+';'
                ihlal_turu=1
                ihlal_var=1

        for zorla_calistirma_ara in zorla_calistirma:
            zorla_calistirma_varmi = re.search(str(zorla_calistirma_ara),satir[5])
            if zorla_calistirma_varmi:
                ihlal_kelime+=zorla_calistirma_ara+';'
                ihlal_turu=2
                ihlal_var=1

        for pozitif_vaka_ara in pozitif_vaka:
            pozitif_vaka_varmi = re.search(str(pozitif_vaka_ara),satir[5])
            if pozitif_vaka_varmi:
                ihlal_kelime+=pozitif_vaka_ara+';'
                ihlal_turu=3
                ihlal_var=1

        for senelik_izin_ara in senelik_izin:
            senelik_izin_varmi = re.search(str(senelik_izin_ara),satir[5])
            if senelik_izin_varmi:
                ihlal_kelime+=senelik_izin_ara+';'
                ihlal_turu=4
                ihlal_var=1

        for ucretsiz_izin_ara in ucretsiz_izin:
            ucretsiz_izin_varmi = re.search(str(ucretsiz_izin_ara),satir[5])
            if ucretsiz_izin_varmi:
                ihlal_kelime+=ucretsiz_izin_ara+';'
                ihlal_turu=5
                ihlal_var=1

        for angarya_ara in angarya:
            angarya_varmi = re.search(str(angarya_ara),satir[5])
            if angarya_varmi:
                ihlal_kelime+=angarya_ara+';'
                ihlal_turu=6
                ihlal_var=1

        for eksik_odeme_ara in eksik_odeme:
            eksik_odeme_varmi = re.search(str(eksik_odeme_ara),satir[5])
            if eksik_odeme_varmi:
                ihlal_kelime+=eksik_odeme_ara+';'
                ihlal_turu=7
                ihlal_var=1

        for sosyal_haklar_ara in sosyal_haklar:
            sosyal_haklar_varmi = re.search(str(sosyal_haklar_ara),satir[5])
            if sosyal_haklar_varmi:
                ihlal_kelime+=sosyal_haklar_ara+';'
                ihlal_turu=8
                ihlal_var=1

        for tis_ara in tis:
            tis_varmi = re.search(str(tis_ara),satir[5])
            if tis_varmi:
                ihlal_kelime+=tis_ara+';'
                ihlal_turu=9
                ihlal_var=1

        for emekli_edilme_ara in emekli_edilme:
            emekli_edilme_varmi = re.search(str(emekli_edilme_ara),satir[5])
            if emekli_edilme_varmi:
                ihlal_kelime+=emekli_edilme_ara+';'
                ihlal_turu=10
                ihlal_var=1

        for sokaga_cikma_ara in sokaga_cikma:
            sokaga_cikma_varmi = re.search(str(sokaga_cikma_ara),satir[5])
            if sokaga_cikma_varmi:
                ihlal_kelime+=sokaga_cikma_ara+';'
                ihlal_turu=11
                ihlal_var=1

        if ihlal_var==0:
            ihlal_turu=""
            ihlal_kelime=""
        else:
            ihlal_kaynak=satir[7]

        for direnis_dizi_ara in direnis_dizi:
            direnis_dizi_varmi = re.search(str(direnis_dizi_ara),satir[5])
            if direnis_dizi_varmi:
                direnis+=direnis_dizi_ara+';'
                direnis_var=1

        if direnis_var==0:
            direnis_var="Hayır"
            direnis=""
            direnis_Kaynak=""
        else :
            direnis_Kaynak=satir[7]
            direnis_var="Evet"

        for sirket_uygulama_ara in sirket_uygulama:
            sirket_uygulama_varmi = re.search(str(sirket_uygulama_ara),satir[5])
            if sirket_uygulama_varmi:
                covid_sirket_uygulama+=sirket_uygulama_ara+';'
                covid_sirket_uygulama_var=1

        if covid_sirket_uygulama_var==0:
            covid_sirket_uygulama=""
            covid_sirket_haber=""
        else:
            covid_sirket_haber=satir[7]

# tüm büyük harfli kelimeleri bulur.
        kelimeler = satir[5].split()
        for kelime in kelimeler:
            buyuk_harf = re.findall("^[A-Z]+[a-z]+",kelime)
            if buyuk_harf:
                    buyuk_harfli+=str(buyuk_harf)


        csv_yaz = firma+","+ana_firma+","+isyeri+","+is_kolu+","+str(ihlal_turu)+","+covid_sirket_haber+","+covid_sirket_uygulama+","+tarih+","+il+","+ilce+","+ihlal_kaynak+","+direnis_var+","+direnis+","+siddet+","+direnis_Kaynak+","+PR+","+PR_Kaynak+","+str(ihlal_turu)+","+ihlal_kelime+","+covid_sirket_uygulama+","+covid_sirket_uygulama+","+lokasyon+","+ozel_isim+","+buyuk_harfli

        with open("covid_ihlal.csv","a",encoding="utf-8") as dosya:
            dosya.write(csv_yaz)
            dosya.write("\n")
