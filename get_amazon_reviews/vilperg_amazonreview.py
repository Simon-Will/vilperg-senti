#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
from collections import namedtuple

import time
import datetime as dt
from enum import Enum

import urllib.parse as up
import urllib.request as ur
import urllib.error as ue
from bs4 import BeautifulSoup

HTML_PARSER = 'lxml'

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
    """An amazon page advertising multiple products.

    Attributes:
        url (str): The url of the overview site.
        html (str: The content of the overview site as html.
    """

    def __init__(self, url):
        """Initiate Amazon_overview by supplying its url."""
        self.url = url
        response = get_http_response(url)
        self.html = response.read()

    def __str__(self):
        s = '<Amazon_overview url={0} >'.format(self.url)
        return s

    def get_products(self):
        """Get all products on this overview as Amazon_product objects.

        Returns:
            products (list): All Amazon_product objects on this overview.
        """
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

            stars = 0
            review_number = 0
            i =  li.find('i', {'class' : 'a-icon-star'})
            if i is not None:
                # If the product has received no reviews, it has neither stars
                # nor reviews.
                star_span = i.span.get_text(strip=True)
                stars = get_stars(star_span)
                # XXX: There might be a better way to get the review_number_tag.
                review_number_tag = i.parent.parent.parent.parent.find(
                        'a', {'class' : 'a-link-normal'})
                try:
                    review_number_text = review_number_tag.get_text(strip=True)
                    review_number = int(re.sub(r'\.', '', review_number_text))
                except ValueError:
                    # If this does not work for some reason, just proceed with
                    # the next product.
                    continue

            products.append(
                    Amazon_product(url, id, title, review_number, stars))

        return products
    
    def get_next_overview(self):
        """Get the overview site following this one.

        Returns:
            next_overview (Amazon_overview): The next Amazon_overview site.
        """
        soup = BeautifulSoup(self.html, HTML_PARSER)
        # The div with the id 'pagn' contains the links to the other overviews.
        pagn = soup.find('div', id='pagn')
        found_cur = False
        for t in pagn:
            if t.name != 'span':
                continue

            if found_cur == True and 'pagnLink' in t['class']:
                # Found the t linking to the next overview. Construct it.
                url_part = t.a['href']
                url_part = up.quote(url_part)
                url = 'http://amazon.de/{0}'.format(url_part)
                return Amazon_overview(url)

            elif 'pagnCur' in t['class']:
                found_cur = True

        raise No_next_overview('This is the last overview page')

class No_next_overview(Exception):
    pass

class Amazon_product:
    """A product on amazon.

    Attributes:
        url (str): The url of the product site.
        id (str): The id of the product. This is called ASIN in amazon.
        title (str): The name of the product.
        review_number (int): The number of reviews of the product.
        stars (int): The number of stars (as rating) of the product (out of 5).
    """

    def __init__(self, url, id, title, review_number, stars):
        """Initiate Amazon_product with all its attributes."""
        self.url = url
        self.id = id
        self.title = title
        self.review_number = review_number
        self.stars = stars

    def get_reviews(self):
        """Get all reviews of the product."""

        if self.review_number == 0:
            return []

        reviews = []
        for rs in self.generate_reviews_sites():
            soup = BeautifulSoup(rs, HTML_PARSER)
            reviews.extend(get_reviews_from_reviews_soup(soup, self.id))
        return reviews

    def __str__(self):
        """Return string holding title, url, stars, reviews and id."""
        s1 = 'Product: {0.title}\n'
        s2 = 'URL: {0.url}\n'
        s3 = 'Stars: {0.stars} | Reviews: {0.review_number} | ID: {0.id}'
        s = s1 + s2 + s3
        formatted = s.format(self)
        return formatted

    def generate_reviews_sites(self):
        """Generate the amazon sites that hold the reviews.

        Typically, they each hold 10 reviews.

        Yields:
            reviews_site (str): An amazon site holding 10 reviews.
        """
        reviews_url_pattern = (
                'http://www.amazon.de/product-reviews/{0}?pageNumber={1}' )
        # 10 reviews per site seems to be the default for amazon.
        # XXX: Can this be changed in amazon?
        reviews_per_site = 10
        max_site_number = (self.review_number // reviews_per_site) + 1
        for i in range(1, max_site_number + 1):
            reviews_url = reviews_url_pattern.format(self.id, i)
            reponse = get_http_response(reviews_url)
            reviews_site = reponse.read()
            yield reviews_site

class Amazon_review:
    """A review for an amazon product.

    Attributes:
        id (str): The id of the review.
        title (str): The title of the review.
        text (str): The content of the review.
        stars (float): The stars given as a rating by the reviewer.
        helpfulness (Helpfulness): The helpfulness of the review.
        product_id (str): The id of the product the review belongs to.
        date (datetime.date): The date on which the review was submitted.
    """

    def __init__(self, id, title, text, stars, helpfulness, product_id, date):
        """Initiate Amazon_product with all its attributes."""
        self.id = id
        self.title = title
        self.text = text
        self.stars = stars
        self.helpfulness = helpfulness
        self.product_id = product_id
        self.date = date

    def __str__(self):
        """Return string holding title, stars, helpfulness, date and id."""
        s1 = 'Title: {0.title}\n'
        s2 = 'Stars: {0.stars} | Helpfulness: {0.helpfulness}'
        s3 = 'Date: {0.date} | ID: {0.id}'
        s = s1 + s2 + s3
        formatted = s.format(self)
        return formatted

def get_reviews_from_reviews_soup(soup, product_id):
    """Get all reviews as Amazon_review objects on a reviews site.
    
    The reviews are constructed from a BeautifulSoup representation of that
    site.

    Args:
        soup (BeautifulSoup): A BeautifulSoup representation of the html of
        a reviews site.

    Returns:
        reviews (list): All reviews on that site as Amazon_review objects.
    """
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
        except AttributeError:
            # No-one has voted on the helpfulness of this review.
            helpfulness = Helpfulness(0, 0)

        date_span = ( r.find('span', {'class' : 'review-date'}).
                get_text(strip=True) )
        date = get_date(date_span)

        reviews.append(Amazon_review(id, title, text, stars, helpfulness,
            product_id, date))

    return reviews

Helpfulness = namedtuple('Helpfulness', 'helpful, total')

def formatHelpfulness(helpfulness):
    """Format a Helpfulness namedtuple and return a string representation.

    Args:
        helpfulness (Helpfulness): The Helpfulness namedtuple

    Returns:
        formatted (str): The Helpfulness namedtuple as a string.

    >>> formatHelpfulness(Helpfulness(24, 45))
    'Helpful: 24/45'
    """
    return 'Helpful: {0.helpful}/{0.total}'.format(helpfulness)

def get_helpfulness(helpfulness_span):
    """Extract the helpfulness from an amazon helpful_span.

    Args:
        helpfulness_span (str): A string like
            '63 von 67 Kunden fanden die folgende Rezension hilfreich'.

    Returns:
        helpfulness (Helpfulness): A Helpfulness namedtuple.

    >>> get_helpfulness('63 von 67 Kunden fanden die folgende Rezension hilfreich')
    Helpfulness(helpful=63, total=67)
    """
    helpfulness_pattern = re.compile(r'^\s*(\d+)\s+von\s+(\d+)\s.*$')
    m = helpfulness_pattern.match(helpfulness_span)
    (helpful, total) = m.groups()
    return Helpfulness(int(helpful), int(total))

def get_date(date_span):
    """Extract the date from an amazon date_span.

    Args:
        date_span (str): A string like 'am 20 März 1994'.

    Returns:
        date (datetime.date): The date.

    >>> get_date('am 20. März 1994')
    datetime.date(1994, 3, 20)
    """
    date_pattern = re.compile(r'^\s*am\s+(\d+)\.\s+(\w+)\s+(\d+)\s*$')
    m = date_pattern.match(date_span)
    (day_string, month_string, year_string) = m.groups()
    month = GermanMonth[month_string].value
    day = int(day_string)
    year = int(year_string)
    return dt.date(year, month, day)

def get_stars(star_span):
    """Extract the number of stars from a star_span from amazon.

    Args:
        star_span (str): A string like '2.3 von 5 Sternen' or
            '4 von 5 Sternen'

    Returns:
        star_number (float): The number of stars.

    >>> get_stars('2,3 von 5 Sternen')
    2.3
    >>> get_stars('4 von 5 Sternen')
    4.0
    """
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

def get_http_response(url, max_tries=None):
    """Try to get an HTTPResponse from a url with a number of tries.

    Args:
        url (str): An http url.
        max_tries (int): How often the response should be requested.
            Default: None

    Returns:
        response (http.client.HTTPRespone): An HTTPResponse object.
    """
    url_request_successful = False
    tries = 0
    reponse = None
    while not url_request_successful:
        # If the http request was unsuccessful, don't give up.
        # Wait a moment and try it again.
        try:
            response = ur.urlopen(url)
            url_request_successful = True
        except ue.HTTPError:
            time.sleep(0.2)
        except ue.URLError as e:
            raise e

        if max_tries is not None and tries >= max_tries:
            mess = 'Could not get {0} after {1} tries'.format(url, max_tries)
            raise ue.HTTPError(mess)
        else:
            tries += 1

    return response

def test():
    import doctest
    doctest.testmod()

if __name__ == '__main__':
    test()
