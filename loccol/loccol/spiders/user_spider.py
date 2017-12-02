import scrapy

from loccol.items import UserItem

class UserSpider(scrapy.Spider):

    name = 'user'
    allowed_domains = ['github.com']

    def __init__(self, username=None, *args, **kwargs):
        super(UserSpider, self).__init__(*args, **kwargs)
        if username is None:
            raise Exception('username is None')
        self.username = username 
        print('self.username =', self.username)

    def start_requests(self):
        url = 'https://github.com/{}?tab=following'.format(self.username)
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):

        names = response.css('h1.vcard-names')
        username = names.css('span.vcard-username').xpath('text()').extract_first()
        fullname = names.css('span.vcard-fullname').xpath('text()').extract_first()

        linker = response.meta.get('linker', None)
        order = response.meta.get('order', 0)

        nr_follower = response.css('div.user-profile-nav')\
                .xpath('nav')\
                .xpath('a[@title="Followers"]')\
                .xpath('span/text()')\
                .extract_first()\
                .strip()
    
        location = response.xpath('//li[@aria-label="Home location"]')\
                .xpath('span/text()')\
                .extract_first()

        yield UserItem(username=username,
                order=order,
                linker=linker,
                fullname=fullname,
                followers=nr_follower,
                location=location) # location may be None

        metadata = {
            'linker': username,
            'order': order + 1,
        }

        for following in response.css('div.position-relative').css('div.d-table'):
            next_page = following.xpath('div[2]/a').xpath('@href').extract_first()
            if next_page is not None:
                next_page = response.urljoin(next_page) + '?tab=following'
                yield scrapy.Request(next_page, callback=self.parse, meta=metadata)

