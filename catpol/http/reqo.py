import scrapy


class Reqo(scrapy.Request):
    def __eq__(self, other):
        if hasattr(self, 'url') and hasattr(other, 'url'):
            return self.url == other.url
        elif not hasattr(self, 'url') and not hasattr(other, 'url'):
            return True
        return False

    def __hash__(self):
        if hasattr(self, 'url'):
            return hash(self.url)
        return 0
