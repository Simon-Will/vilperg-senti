#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import re
from collections import namedtuple

import datetime as dt
from enum import Enum

import urllib.request as ur
import urllib.error as ue
from bs4 import BeautifulSoup

HTML_PARSER = 'html.parser'

class GermanMonth(Enum):
    Januar = 1
    Februar = 2
    März = 3
    April = 4
    Mai = 5
    Juni = 6
    Juli = 7
    August = 8
    September = 9
    Oktober = 10
    November = 11
    Dezember = 12

class Amazon_overview:
    def __init__(self, url):
        self.url = url
        try:
            self.response = ur.urlopen(url)
        except ue.HTTPError as e:
            raise e
        except ue.URLError as e:
            raise e
        self.html = self.response.read()

    def get_products(self):
        products = []
        soup = BeautifulSoup(self.html, HTML_PARSER)
        for li in soup.find('div', id='atfResults').ul:
            # Collect the important information about each product and append
            # it to the product list.
            id = li['data-asin']
            a = ( li.find('div', {'class' : 's-item-container'}).
                    find('a', {'class' : 's-access-detail-page'}) )
            url = a['href']
            title = a['title']

            i =  li.find('i', {'class' : 'a-icon-star'})
            star_span = i.span.get_text(strip=True)
            stars = get_stars(star_span)

            # XXX: There might be a better way to get the review_number_tag.
            review_number_tag = i.parent.parent.parent.parent.find(
                    'a', {'class' : 'a-link-normal'})
            review_number = int(review_number_tag.get_text(strip=True))

            products.append(
                    Amazon_product(url, id, title, review_number, stars))

        return products
    
    def get_next_overview(self):
        pass

class No_next_overview(Exception):
    pass

class Amazon_product:
    def __init__(self, url, id, title, review_number, stars):
        self.url = url
        self.id = id
        self.title = title
        self.review_number = review_number
        self.stars = stars

    def get_reviews(self):
        reviews = []
        for rs in self.generate_reviews_sites():
            soup = BeautifulSoup(rs, HTML_PARSER)
            reviews.extend(get_reviews_from_soup(soup, self.id))
        return reviews

    def __str__(self):
        s1 = 'Product: {0.title}\n'
        s2 = 'Stars: {0.stars} | Reviews: {0.review_number} | ID: {0.id}'
        s = s1 + s2
        formatted = s.format(self)
        return formatted

    def generate_reviews_sites(self):
        reviews_url_pattern = (
                'http://www.amazon.de/product-reviews/{0}?pageNumber={1}' )
        # 10 reviews per site seems to be the default for amazon.
        # XXX: Can this be changed in amazon?
        reviews_per_site = 10
        max_site_number = (self.review_number // reviews_per_site) + 1
        for i in range(1, max_site_number + 1):
            reviews_url = reviews_url_pattern.format(self.id, i)
            reviews_site = ur.urlopen(reviews_url).read()
            yield reviews_site

Helpfulness = namedtuple('Helpfulness', 'helpful, total')

class Amazon_review:
    def __init__(self, id, title, text, stars, helpfulness, product_id, date):
        self.id = id
        self.title = title
        self.text = text
        self.stars = stars
        self.helpfulness = helpfulness
        self.product_id = product_id
        self.date = date

    def __str__(self):
        s1 = 'Title: {0.title}\n'
        s2 = 'Stars: {0.stars} | Helpfulness: {0.helpfulness} | ID: {0.id}'
        s = s1 + s2
        formatted = s.format(self)
        return formatted

def get_reviews_from_soup(soup, product_id):
    reviews = []
    for r in soup.find('div', {'id' : 'cm_cr-review_list'}):
        if 'review' not in r['class']:
            continue
        # Collect the important information about each product and
        # append it to the product list.
        id = r['id']
        title = r.find('a', {'class' : 'review-title'}).get_text(strip=True)
        text = r.find('span', {'class' : 'review-text'}).get_text(strip=True)

        star_span = ( r.find('i', {'class' : 'a-icon-star'}).
                span.get_text(strip=True) )
        stars = get_stars(star_span)

        try:
            helpfulness_span = ( r.find('div', {'class' : 'helpful-votes-count'}).
                    span.get_text(strip=True) )
            helpfulness = get_helpfulness(helpfulness_span)
        except AttributeError as e:
            # No-one has voted on the helpfulness of this review.
            helpfulness = Helpfulness(0, 0)

        date_span = ( r.find('span', {'class' : 'review-date'}).
                get_text(strip=True) )
        date = get_date(date_span)

        reviews.append(Amazon_review(id, title, text, stars, helpfulness,
            product_id, date))

    return reviews

def get_helpfulness(helpfulness_span):
    helpfulness_pattern = re.compile(r'^\s*(\d+)\s+von\s+(\d+)\s.*$')
    m = helpfulness_pattern.match(helpfulness_span)
    (helpful, total) = m.groups()
    return Helpfulness(helpful, total)

def get_date(date_span):
    date_pattern = re.compile(r'^\s*am\s+(\d+)\.\s+(\w+)\s+(\d+)\s*$')
    m = date_pattern.match(date_span)
    (day_string, month_string, year_string) = m.groups()
    month = GermanMonth[month_string].value
    day = int(day_string)
    year = int(year_string)
    return dt.date(year, month, day)

def get_stars(star_span):
    star_pattern = re.compile(r'^\s*(\d)(?:,(\d))?\s.*$')
    m = star_pattern.match(star_span)
    stars = None
    if m.groups()[1] is None:
        (units, tenths) = m.groups()
        stars = float('{0}.0'.format(units))
    else:
        (units, tenths) = m.groups()
        stars = float('{0}.{1}'.format(units, tenths))
    return stars

def get_all_reviews(start_url):
    overview = Amazon_overview(start_url)
    products = overview.get_products()
    reviews = []
    for p in products:
        reviews.extend(p.get_reviews())
    return reviews

def main():
    start_url = sys.argv[1]
    out_file = sys.argv[2]
    reviews = get_all_reviews(start_url)
    with open(out_file, 'w') as f:
        for r in reviews:
            f.write(str(r))
            f.write("\n")

if __name__ == '__main__':
    main()
