# -*- coding: utf-8 -*-
"""
    __init__.py

    :copyright: (c) 2015 by Fulfil.IO Inc.
    :license: see LICENSE for details.
"""
from trytond.pool import Pool

from product import Product, ProductGoogleTaxonomyRel, Attribute, GoogleTaxonomy
from channel import Channel


def register():
    Pool.register(
        GoogleTaxonomy,
        ProductGoogleTaxonomyRel,
        Product,
        Attribute,
        Channel,
        module='google_merchant', type_='model'
    )
