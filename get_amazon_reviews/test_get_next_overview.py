#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import vilperg_amazonreview as amaz

def test():
    overview2 = amaz.Amazon_overview('http://www.amazon.de/s/ref=sr_pg_2?rh=n%3A562066%2Cn%3A%21569604%2Cn%3A1384526031%2Cn%3A3468301&page=2&ie=UTF8&qid=1449851661&spIA=B00XMQJ1I6,B00J4UUHWS,B0171MAZLS')
    print(overview2)
    #overview3 = overview2.get_next_overview()
    #print(overview3)

    overview399 = amaz.Amazon_overview('http://www.amazon.de/Handys-Smartphones-Zubeh%C3%B6r/s?ie=UTF8&page=399&rh=n%3A3468301')
    print(overview399)
    overview400 = overview399.get_next_overview()
    print(overview400)
    overview401 = overview400.get_next_overview()
    print(overview401)

if __name__ == '__main__':
    test()
