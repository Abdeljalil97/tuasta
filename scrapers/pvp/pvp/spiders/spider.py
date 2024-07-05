import scrapy
import redis
redisClient = redis.from_url('redis://127.0.0.1:6379')
class SpiderSpider(scrapy.Spider):
    name = "pvp"
    

    allowed_domains = ["pvp.giustizia.it"]
    start_urls = ["https://pvp.giustizia.it/pvp/it/risultati_ricerca.page?tipo_bene=immobili&categoria=&geo=raggio&lat=&lng=&indirizzo=&raggio=25&prezzo_da=&prezzo_a=&tribunale=&procedura=&anno=&idInserzione=&ricerca_libera=&disponibilita=&ordinamento=data_vendita_cresc&ordine_localita=a_z&view=tab&elementiPerPagina=50",
                  "https://pvp.giustizia.it/pvp/it/risultati_ricerca.page?tipo_bene=mobili&categoria=&geo=raggio&lat=&lng=&indirizzo=&raggio=25&prezzo_da=&prezzo_a=&tribunale=&procedura=&anno=&idInserzione=&ricerca_libera=&modalita=&ordinamento=data_vendita_cresc&ordine_localita=a_z&view=tab&elementiPerPagina=50",
                  "https://pvp.giustizia.it/pvp/it/risultati_ricerca.page?tipo_bene=valoricrediti&categoria=&geo=raggio&lat=&lng=&indirizzo=&raggio=25&prezzo_da=&prezzo_a=&tribunale=&procedura=&anno=&idInserzione=&ricerca_libera=&ordinamento=data_vendita_cresc&ordine_localita=a_z&view=tab&elementiPerPagina=50",
                  "https://pvp.giustizia.it/pvp/it/risultati_ricerca.page?tipo_bene=aziende&categoria=&geo=raggio&lat=&lng=&indirizzo=&raggio=25&prezzo_da=&prezzo_a=&tribunale=&procedura=&anno=&idInserzione=&ricerca_libera=&ordinamento=data_vendita_cresc&ordine_localita=a_z&view=tab&elementiPerPagina=50",
                  "https://pvp.giustizia.it/pvp/it/risultati_ricerca.page?tipo_bene=altro&categoria=&geo=raggio&lat=&lng=&indirizzo=&raggio=25&prezzo_da=&prezzo_a=&tribunale=&procedura=&anno=&idInserzione=&ricerca_libera=&ordinamento=data_vendita_cresc&ordine_localita=a_z&view=tab&elementiPerPagina=50",
                  ]

    def parse(self, response):
        links_products = response.xpath('//*[@class="row tile-blocks"]//a/@href').getall()
        links_products = ["https://pvp.giustizia.it"+link for link in links_products]
        for link in links_products:
            redisClient.lpush('data_queue:pvp', link)
        #yield from response.follow_all(links_products, callback=self.parse_results)
        
        next_page = response.xpath('//*[@aria-label="Next"]/@href').get()
        if next_page:
            next_page  = "https://pvp.giustizia.it"+next_page
            yield scrapy.Request(url=next_page,callback=self.parse)
