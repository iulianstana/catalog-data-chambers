import scrapy
import logging
from datetime import datetime
import xmltodict

import catpol.loaders as loaders
import catpol.items as items
import catpol.http as http


class CdepVoting(scrapy.Spider):
    name = 'cdep_voting'
    year = None
    month = None
    day = None
    crawl_day = False
    crawl_year = False

    def __init__(self, year=None, month=None, day=None):
        logger = logging.getLogger(__name__)
        self.year = year
        self.month = month
        self.day = day

        if year:
            if month:
                if day:
                    self.crawl_day = True
            else:
                self.crawl_year = True
        else:
            now = datetime.now()
            self.year = now.year
            self.month = now.month
            self.day = now.day
            self.crawl_day = True

        try:
            self.day = '0' + self.day if len(self.day) == 1 else self.day
            self.month = '0' + self.month if len(self.month) == 1 else self.month
        except:
            pass

    def start_requests(self):
        if self.crawl_day:
            urls = [
                str(
                    'http://www.cdep.ro/pls/steno/evot2015.xml?'
                    'par1=1&par2={y}{m}{d}'
                )
                .format(y=self.year, m=self.month, d=self.day)
            ]
        elif self.crawl_year:
            urls = []
            for month in range(1, 13):
                urls.append(
                    str(
                        'http://www.cdep.ro/pls/steno/evot2015.zile_vot?'
                        'lu={m}&an={y}'
                    )
                    .format(m=month, y=self.year)
                )
        else:
            urls = [
                'http://www.cdep.ro/pls/steno/evot2015.zile_vot?lu={m}&an={y}'
                .format(m=self.month, y=self.year)
            ]

        if self.crawl_day:
            yield http.Reqo(url=urls[0], callback=self.parse_day)
        else:
            for url in urls:
                yield http.Reqo(url=url, callback=self.parse_month)

    def parse_month(self, response):
        for day in response.body.decode().split(','):
            if day:
                url = str(
                        'http://www.cdep.ro/pls/steno/evot2015.xml?'
                        'par1=1&par2='+day
                        )
                yield http.Reqo(url=url, callback=self.parse_day)

    def parse_day(self, response):
        response_dict = xmltodict.parse(response.body)
        votes = response_dict['ROWSET']['ROW']
        for vote in votes:
            voting_loader = loaders.VotingLoader(items.VotingItem())
            voting_loader.add_value('vote_id', vote['VOTID'])
            voting_loader.add_value('date', vote['TIME_VOT'])
            voting_loader.add_value('description', vote['DESCRIERE'])
            voting_loader.add_value('people_present', vote['PREZENTI'])
            voting_loader.add_value('abstention', vote.get('NU_AU_VOTAT',''))
            voting_loader.add_value('vote_yes', vote.get('AU_VOTAT_DA',''))
            voting_loader.add_value('vote_no', vote.get('AU_VOTAT_NU',''))
            voting_loader.add_value('vote_ab', vote.get('AU_VOTAT_AB',''))

            url = str(
                'http://www.cdep.ro/pls/steno/evot2015.xml?'
                'par1=2&par2='+vote['VOTID']
            )
            yield http.Reqo(url=url, callback=self.parse_vote, meta={'voting_loader': voting_loader})

    def parse_vote(self, response):
        response_dict = xmltodict.parse(response.body)
        voting_loader = response.meta['voting_loader']
        print(voting_loader)
        votes = response_dict['ROWSET']['ROW']
        votes_list = []
        for vote in votes:
            votes_loader = loaders.VotesLoader(items.VotesItem())
            votes_loader.add_value('vote_id', vote['VOTID'])
            votes_loader.add_value('first_name', vote['PRENUME'])
            votes_loader.add_value('last_name', vote['NUME'])
            votes_loader.add_value('party', vote['GRUP'])
            votes_loader.add_value('vote', vote['VOT'])
            votes_list.append(votes_loader.load_item())
        voting_loader.add_value('votes', {'people' : votes_list})
        yield voting_loader.load_item()

