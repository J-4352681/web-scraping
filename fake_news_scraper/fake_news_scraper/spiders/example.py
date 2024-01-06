import scrapy

class Spider1(scrapy.Spider):
    name = 'spdr1'
    start_urls = ['https://votaciones.diputados.gob.ar/']

    def parse(self, response):
        rows = response.css('table > tbody > .row-acta')

        for line in rows:
            fields = line.css('td')

            title = fields[1].css('::text').get().strip()
            result = fields[3].css('center > span::text').get().strip()
            id = line.xpath('@id').get()

            yield {
                'titulo': title,
                'resultado': result,
                'id': id,
            }
            return
