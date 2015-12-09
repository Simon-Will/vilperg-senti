#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import vilperg_amazonreview as amaz
import sys
import os

def get_all_products(start_url):
    """Get all products from an amazon overview site.
    
    Args:
        start_url: The url of the overview page.

    Returns:
        products (list): The Amazon_product objects for the products on the
            overview page.
    """
    overview = amaz.Amazon_overview(start_url)
    products = overview.get_products()
    return products

def write_products(products, out_dir):
    """Write products and their reviews to a directory structure under out_dir.

    For each product in the list, a directory is created under out_dir. In this
    directory, an info file and a reviews directory are created. The info file
    contains information about the product. The reviews directory contains
    files describing one review each.

    Args:
        products (list): A list of Amazon_product objects.
        out_dir (str): The top level directory under which the products and
            their reviews are written.
    """
    ensure_dir(out_dir)
    for p in products:
        p_dir = '{0}/{1}'.format(out_dir, p.id)
        ensure_dir(p_dir)
        p_info = '{0}/info'.format(p_dir)
        with open(p_info, 'w') as p_f:
            p_f.write('{0}\n'.format(p))
        r_dir = '{0}/reviews'.format(p_dir)
        write_reviews(p, r_dir)

def write_reviews(product, directory)
    """Write the reviews of a product in a directory.

    Args:
        product (Amazon_product): An Amazon_product object.
        directory (str): The directory the reviews should be written in.
    """
    reviews = product.get_reviews()
    ensure_dir(directory)
    for r in reviews:
        with open('{0}/{1}'.format(directory, r.id), 'w') as r_f:
            header = str(r)
            r_f.write('{0}\n\n{1}'.format(header, r.text))

def ensure_dir(d):
    """Ensure that the directory exists.
    
    Args:
        d (str): A directory.
    """
    if not os.path.exists(d):
        os.makedirs(d)

def main():
    """Get the amazon products and their reviews from an overview page and
    write all the products and their reviews to a directory structure, the top
    of which is out_dir.

    Command line arguments:
        start_url: The url of the overview page.
        out_dir: The top of the directory structure for the products and
            reviews.
    """
    start_url = sys.argv[1]
    out_dir = sys.argv[2]
    products = get_all_products(start_url)
    write_reviews_from_products(products, out_dir)

if __name__ == '__main__':
    main()
