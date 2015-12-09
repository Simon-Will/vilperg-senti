#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import vilperg_amazonreview as amaz
import sys
import os

def get_all_products(start_url):
    overview = amaz.Amazon_overview(start_url)
    products = overview.get_products()
    return products

def write_reviews_from_products(products, out_dir):
    ensure_dir(out_dir)
    for p in products:
        p_dir = '{0}/{1}'.format(out_dir, p.id)
        ensure_dir(p_dir)
        p_info = '{0}/info'.format(p_dir)
        with open(p_info, 'w') as p_f:
            p_f.write('{0}\n'.format(p))

        reviews = products.get_reviews()
        r_dir = '{0}/{1}'.format(p_dir, reviews)
        ensure_dir(r_dir)
        for r in reviews:
            with open('{0}/{1}'.format(r_dir, r.id)) as r_f:
                header = str(r)
                r_f.write('{0}\n\n{1}'.format(header, r.text))

def ensure_dir(d):
    if not os.path.exists(d):
        os.makedirs(d)

def main():
    start_url = sys.argv[1]
    out_dir = sys.argv[2]
    products = get_all_products(start_url)
    write_reviews_from_products(products, out_dir)

if __name__ == '__main__':
    main()
