#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import vilperg_amazonreview as amaz
import sys

def get_all_reviews(start_url):
    overview = amaz.Amazon_overview(start_url)
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
