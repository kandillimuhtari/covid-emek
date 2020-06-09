
import twint
search_terms=['covid işçi','korona işçi','corona işçi','pandemi işçi','virüs işçi','salgın işçi',
             'covid emekçi','korona emekçi','corona emekçi','pandemi emekçi','virüs emekçi','salgın emekçi',
             'covid çalışan','korona çalışan','corona çalışan','pandemi çalışan','virüs çalışan','salgın çalışan',
             'covid personel','korona personel','corona personel','pandemi personel','virüs personel','salgın personel',
             'covid fabrika','korona fabrika','corona fabrika','pandemi fabrika','virüs fabrika','salgın fabrika',
             'covid işveren','korona işveren','corona işveren','pandemi işveren','virüs işveren','salgın işveren',
             'covid patron','korona patron','corona patron','pandemi patron','virüs patron','salgın patron',
             'covid ücretsiz izin','korona ücretsiz izin','corona ücretsiz izin','pandemi ücretsiz izin','virüs ücretsiz izin','salgın ücretsiz izin',
             'covid zorunlu izin','korona zorunlu izin','corona zorunlu izin','pandemi zorunlu izin','virüs zorunlu izin','salgın zorunlu izin',
             'covid işten çıkarma','korona işten çıkarma','corona işten çıkarma','pandemi işten çıkarma','virüs işten çıkarma','salgın işten çıkarma',
             'covid işten atma','korona işten atma','corona işten atma','pandemi işten atma','virüs işten atma','salgın işten atma',
             'covid iş güvenliği','korona iş güvenliği','corona iş güvenliği','pandemi iş güvenliği','virüs iş güvenliği','salgın iş güvenliği']




for keyword in search_terms:
    c = twint.Config()
    c.Store_csv = True
    c.Output = "/home/dogacan/Documents/DataScience/korona/covid_isci_search_keywords2.csv"
    c.Lang = "tr"
    c.Since="2020-03-11 00:00:00"
    c.Search=keyword
    twint.run.Search(c)
    