
import twint


username= ['ailevecalisma','alpaslan_savas','artigercek','azeryadigar','barkodmarket','bbcturkce','besnatosun','bianet_org',
 'birlesiketal','canerdalgic','ccanozz','chp_istanbulil','devturizmmrm','devyapi_is','dgdsen','dikencomtr','dinergke',
'disk_arastirma','ect35uA','ekmekvegul','ekmekveonur','elif_grg','emeginhalleri','emekadalet','emekdunyasi','emekkocaeli',
'emekorgtr','ercmentakdeniz','evrenselgzt','gidaiscileri','grevgozcusu_','gulferakkaya','gulgndz','hsrtgltknkzn',
'hurayse','iscikomisyonu','ilerihaber','insaatsendika','isci_tv','isciyiz_biz','isciyiz_biz','isigmeclisi','kentemekcileri',
'kentemekcileri','koronaportali','koronareport','mmc_dayanisma','ozgurztrk_','pensendeyiz','satiburunucu','sendika_org','sendika_org2',
'serikirac','sevdakaraca','seyitaslann','sokiscileri','solhaberportali','subelerplatform','t24comtr','ttborgtr','tumcalisanlar','ucretliissizmim',
'umit_k','umut_sendikasi','yasarustaportal','yeni1mecra','yurticikargope','zundert1853','patronlar','kom_cal','aycasoylemez','BirGun_Gazetesi','burcuas ',
'diskgidais ','ev_iscileri','fatih_yasli','fpolat69','GazeteRED','gazeteyolculuk','kargo_iscileri','kizilbayraknet','kudretcobanli ','MngCal','RealMan___',
'samsunolay','SivanKrmzck','sukrandoganoz','TekstilDisk','yeniemekcalisma']


for user in username:
    c = twint.Config()
    c.Store_csv = True
    c.Output = "/home/dogacan/Documents/DataScience/korona/covidisci_search_hesaplar5.csv"
    c.Lang = "tr"
    c.Since="2020-03-11 00:00:00"
    c.Username=user
    twint.run.Search(c)
    