import scrapy

class LocSpider(scrapy.Spider):

    name = 'loc'

    def start_requests(self):
        urls = [
            'https://github.com/nettee?tab=following'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):

        names = response.css('h1.vcard-names')
        username = names.css('span.vcard-username').xpath('text()').extract_first()
        fullname = names.css('span.vcard-fullname').xpath('text()').extract_first()

        nr_follower = response.css('div.user-profile-nav')\
                .xpath('nav')\
                .xpath('a[@title="Followers"]')\
                .xpath('span/text()')\
                .extract_first()\
                .strip()
    
        location = response.xpath('//li[@aria-label="Home location"]')\
                .xpath('span/text()')\
                .extract_first()
        if location is not None:
            yield {
                'username': username,
                'fullname': fullname,
                'followers': nr_follower,
                'location': location,
            }

        for following in response.css('div.position-relative').css('div.d-table'):
            next_page = following.xpath('div[2]/a').xpath('@href').extract_first()
            if next_page is not None:
                next_page = response.urljoin(next_page) + '?tab=following'
                yield scrapy.Request(next_page, callback=self.parse)

