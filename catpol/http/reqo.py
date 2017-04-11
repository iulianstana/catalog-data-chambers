import scrapy

class Reqo(scrapy.Request):
    def eqs(self, other):
        return self.url == other.url
