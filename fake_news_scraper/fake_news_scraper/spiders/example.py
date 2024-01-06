import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

class TableSpider(scrapy.Spider):
    name = 'table_spdr'
    vot_dip_url = 'https://votaciones.diputados.gob.ar/'
    start_urls = [vot_dip_url]

    def gen_dict(self, row, slctd_flds, slctd_attrs):
        fields = row.css('td')

        get_selected_field = lambda name, index: (
            name, ''.join(fields[index].xpath('.//text()').extract()).strip()
        )

        get_selected_attr = lambda name, attr_name: (
            name, row.xpath('@' + attr_name).get()
        )

        dct = dict(
            get_selected_field(*slctd_fld)
            for slctd_fld in slctd_flds
        )

        dct.update(
            get_selected_attr(*slctd_attr)
            for slctd_attr in slctd_attrs
        )

        return dct

    def parse(self, response):
        rows = response.css('table > tbody > tr')

        for row in rows:
            self.table_data = self.gen_dict(row, [
                ('title', 1),
                ('result', 3),
            ], [
                ('id', 'id'),
            ])

            # Preparo el el mismo spider para llamarlo anidado
            process = CrawlerProcess(get_project_settings())

            def callback(response):
                data = response.meta['data']
                # yield {'data': data}
                self.table_data['votes'] = data

            process.crawl(
                TableSpider,
                url=self.vot_dip_url + 'votacion/' + self.table_data['id'],
                callback=callback
            )

            yield self.table_data
            return
