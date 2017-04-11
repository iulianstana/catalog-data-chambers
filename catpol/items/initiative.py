# -*- coding: utf-8 -*-

import json
import scrapy
import hashlib

def equal_dict(d1, d2):
    set_keys_d1 = set(d1.keys())
    set_keys_d2 = set(d2.keys())
    if len(set_keys_d1.intersection(set_keys_d2)) != len(set_keys_d1.union(set_keys_d2)):
        return False
    res = True
    for k in d1.keys():
        if k not in d2:
            res = False
            break
        else:
            if type(d1[k]) is dict:
                res = res and equal_dict(d1[k], d2[k])
                if not res:
                    break
            else:
                if d1[k] != d2[k]:
                    res = False
                    break
    return res

class InitiativeItem(scrapy.Item):
    title = scrapy.Field()
    status = scrapy.Field()
    author = scrapy.Field()

    def eqs(self, other):
        self_dump = json.dumps(dict(self), sort_keys = True)
        other_dump = json.dumps(dict(other), sort_keys = True)
        # print(self_dump)
        # print("-------------")
        # print(other_dump)
        # print("====================")
        return self_dump == other_dump
