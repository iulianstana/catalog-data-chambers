from collections import defaultdict
import scrapy

import catpol.loaders as loaders
import catpol.items as items
import catpol.http as http

import catpol.cmdinput as cmdinput


class Cdep(scrapy.Spider):
    """This spider crawls for:
    - personal data
    - initiatives
    - plenery time
    - party migration
    """
    name = 'cdep'

    def __init__(self, legs=None):
        super().__init__()
        self.legs = cmdinput.expand_legs_str(legs)

    def start_requests(self):
        for leg in self.legs:
            url = 'http://www.cdep.ro/pls/parlam/structura2015.de?leg={leg}'.format(leg=leg)
            yield http.Reqo(url=url,
                            callback=self.parse_ids,
                            meta={'leg': leg})

    def parse_ids(self, response):
        """
        Example URLs:
        - http://www.cdep.ro/pls/parlam/structura2015.de?leg=2016
        - http://www.cdep.ro/pls/parlam/structura2015.de?leg=2012
        - http://www.cdep.ro/pls/parlam/structura2015.de?leg=2008

        Follows URLs to:
        - person
        """
        urls = response.css('div.grup-parlamentar-list.grupuri-parlamentare-list table tbody tr td:nth-child(2) a::attr(href)').extract()
        for url in urls:
            yield http.Reqo(url=response.urljoin(url),
                            callback=self.parse_person,
                            meta=response.meta)

    def parse_person(self, response):
        """
        Example URLs:
        - http://www.cdep.ro/pls/parlam/structura2015.mp?idm=103&cam=2&leg=2016
        - http://www.cdep.ro/pls/parlam/structura2015.mp?idm=92&cam=2&leg=2016
        - http://www.cdep.ro/pls/parlam/structura2015.mp?idm=300&cam=2&leg=2016

        Parses data about a single person:
        - full name
        - birthdate
        - parliamentary activity summary
        - politial party migration

        Follows URLs to:
        - plenery speaking
        - initiatives
        """

        # parse person name
        person_name = response.css(
            'div.profile-dep div.boxTitle h1::text'
        ).extract_first()

        # parse profile picture src
        profile_picture_src = response.urljoin(response.css('div.profile-dep div.profile-pic-dep img::attr(src)').extract_first())

        # parse birthdate
        birthdate = ''.join(response.css('div.profile-dep div.profile-pic-dep::text').extract()).strip()

        # parse parliamentary activity summary
        activity_dict = self.parse_activity(response)

        # parse parliamentary political party
        political_party_dict = self.parse_political_party(response)

        personal_data_loader = loaders.PersonalDataLoader(items.PersonalDataItem())
        personal_data_loader.add_value('activity', activity_dict)
        personal_data_loader.add_value('name', person_name)
        personal_data_loader.add_value('birthdate', birthdate)
        personal_data_loader.add_value('url', response.url)
        personal_data_loader.add_value('picture', profile_picture_src)
        personal_data_loader.add_value('leg', response.meta['leg'])
        personal_data_loader.add_value('formations', political_party_dict)
        yield personal_data_loader.load_item()

        # follow plenery speaking url
        field_name = 'Luari de cuvânt:'
        url = response.xpath(
            '//tr/td[text()=\'{}\']/following-sibling::td/a/@href'.format(field_name)).extract_first()
        yield http.Reqo(
            url=response.urljoin(url),
            callback=self.parse_plenery_time)

        # follow initiatives url
        url = response.xpath('//a[text()=\'Initiative legislative\']/@href').extract_first()
        yield http.Reqo(
            url=response.urljoin(url),
            callback=self.parse_initiatives)

    def parse_initiatives(self, response):
        """
        Example URLs:
        - http://www.cdep.ro/pls/parlam/structura2015.mp?idm=103&cam=2&leg=2016&pag=2
        - http://www.cdep.ro/pls/parlam/structura2015.mp?idm=92&cam=2&leg=2016&pag=2
        - http://www.cdep.ro/pls/parlam/structura2015.mp?idm=300&cam=2&leg=2016&pag=2

        Parses data about several initiatives:
        - author
        - status

        Does not follow any URLs.
        """
        author_name = response.css(
            'div.profile-dep div.boxTitle h1::text'
        ).extract_first()
        rows = response.css(
            'div.grup-parlamentar-list.grupuri-parlamentare-list tbody tr')
        cdep = rows.css('td:nth-child(2)')
        senat = rows.css('td:nth-child(3)')
        title = rows.css('td:nth-child(4)')
        status = rows.css('td:nth-child(5)')
        i = 0
        while i < len(title):
            status_loader = loaders.StatusLoader(items.StatusItem())
            if cdep[i].xpath('.//a/@href').extract_first():
                status_cdep_loader = loaders.LinkLoader(items.LinkItem())
                status_cdep_loader.add_value('title',
                                             cdep[i].xpath('.//text()').extract_first())
                status_cdep_loader.add_value('href',
                                             response.urljoin(cdep[i].xpath('.//a/@href').extract_first()))
                status_loader.add_value('cdep',
                                        dict(status_cdep_loader.load_item()))
            if senat[i].xpath('.//a/@href').extract_first():
                status_senat_loader = loaders.LinkLoader(items.LinkItem())
                status_senat_loader.add_value('title',
                                              senat[i].xpath('.//text()').extract_first())
                status_senat_loader.add_value('href',
                                              response.urljoin(senat[i].xpath('.//a/@href').extract_first()))
                status_loader.add_value('senat',
                                        dict(status_senat_loader.load_item()))
            status_loader.add_value('status',
                                    ' '.join(status[i].xpath('.//text()').extract()))
            loader = loaders.InitiativeLoader(items.InitiativeItem())
            loader.add_value('title',
                             title[i].xpath('.//text()').extract_first())
            loader.add_value('author', author_name)
            loader.add_value('status', dict(status_loader.load_item()))
            loader.add_value('url', response.url)
            yield loader.load_item()
            i += 1

    def parse_plenery_time(self, response):
        """Parses plenery time of a person."""
        loader = loaders.PleneryTimeLoader(item=items.PleneryTimeItem(), response=response)
        loader.add_xpath('duration', '//tr/td[text()=\'total durată video:\']/following-sibling::td//text()')
        loader.add_xpath('name', '//tr/td[text()=\'vorbitor:\']/following-sibling::td//text()')
        loader.add_value('url', response.url)
        yield loader.load_item()

    def parse_activity(self, response):
        """Parse parliamentary activity summary."""
        div_text = 'Activitatea parlamentara în cifre'
        activity_rows = response.xpath(
            '//text()[contains(.,\'{}\')]/../../table/tr'.format(div_text)
        )
        activity_dict = dict()
        for row in activity_rows:
            columns = row.xpath('.//td')
            if len(columns) == 2:
                key = ''.join(columns[0].xpath(
                    './/text()').extract()).strip(':')
                value = ''.join(columns[1].xpath('.//text()').extract())
                activity_dict[key] = value
        return activity_dict

    def parse_political_party(self, response):
        """Parse political party affiliation period.

        Return a dictionary of politician political parties, example:
        Multiple political parties {
            "PP-DD": [[" - până în  iun. 2014"]],
            "UNPR": [[" - din  iun. 2014"]]
        }
        Multiple times in a party: {
            "PP-DD": [[" - până în  apr. 2013"]],
            "independent": [[" - din  apr. 2013", " - până în  oct. 2013"], [" - din  noi. 2016"]],
            "UNPR": [[" - din  oct. 2013", " - până în  noi. 2016"]]}
        }
        A single party: {
            "PNL": [[]]
        }

        Member could be part of the same party in different periods. For this reason, each party has a list of lists.
        """
        PARTY_COLUMN = 2
        PARTY_PERIOD_COLUMN = 5
        INDEPENDENT_PERIOD_COLUMN = 4

        div_text = 'Formatiunea politica'
        political_party_rows = response.xpath(
            '//text()[contains(.,\'{}\')]/../../table/tr'.format(div_text)
        )

        political_party_dict = defaultdict(list)
        # save each political affiliation in a dictionary format
        for row in political_party_rows:
            columns = row.xpath('.//td')

            party = ''.join(columns[PARTY_COLUMN].xpath('.//text()').extract())
            # Check if politician was in a single party this legislation
            if len(political_party_rows) > 1:
                # Get leg period for independent member
                if party == 'independent':
                    period = columns[INDEPENDENT_PERIOD_COLUMN].xpath('.//text()').extract()
                else:
                    period = columns[PARTY_PERIOD_COLUMN].xpath('.//text()').extract()
            else:
                period = []
            political_party_dict[party].append(period)
        return political_party_dict
