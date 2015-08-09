# -*- coding: utf-8 -*-
"""
    google_merchant.py

    :copyright: (c) 2015 by Fulfil.IO Inc.
    :license: see LICENSE for more details.
"""
from trytond.pool import PoolMeta

__all__ = [
    'Product', 'ProductGoogleTaxonomyRel', 'Attribute', 'GoogleTaxonomy',
]
__metaclass__ = PoolMeta


class Product:
    __name__ = 'product.product'

    # See
    # https://support.google.com/merchants/answer/188494#google_product_category
    google_product_category = fields.Many2One(
        'product.google_taxonomy', 'Google Product Category',
        help="If your items fall into multiple categories, include only"
        " one category which is the most relevant."
    )
    google_product_types = fields.Many2Many(
        'product.product-product.google_taxonomy', 'product', 'taxonomy',
        'Google Product Types'
    )

    def as_google_resource(self, channel):
        """
        Return a dictionary of product information that
        can be JSON serialized to be sent to google merchant
        center via API.

        :param channel: The channel to which the product is listed.
        """
        data = {
            'kind': 'content#product',
            'id': self.id,
            'mpn': self.code,
            'title': self.name,
            'description': self.description,
            'offerId': '%s:%s' % (channel.id, product.id),
            'channel': 'online' if channel.source == 'webshop' else 'local',
            'contentLanguage': Transaction().context['language'],

            # TODO
            'link': '',
            'imageLink': '',
            'additionalImageLinks': '',

            'customAttributes': [],
        }
        if self.get_availability()['quantity'] > 0.00:
            data['availability'] = 'in stock'
        else:
            data['availability'] = 'out of stock'

        if self.google_product_category:
            data['googleProductCategory'] = self.google_product_category.name
        if self.google_product_types:
            data['productType'] = ','.join([
                taxonomy.name for taxonomy in self.google_product_types
            ])

        if hasattr(self, 'attributes') and self.attributes:
            for prod_attr in self.attributes:
                data['customAttributes'].append({
                    'name': prod_attr.attribute.rec_name,
                    'type': prod_attr.attribute.get_google_type(),
                    'value': prod_attr.value,
                })
                if prod_attr.attribute.rec_name.lower() == 'brand':
                    data['brand'] = prod_attr.value
                if prod_attr.attribute.rec_name.lower() in ('color', 'colour'):
                    data['color'] = prod_attr.value
                if prod_attr.attribute.rec_name.lower() == 'material':
                    data['material'] = prod_attr.value
                if prod_attr.attribute.rec_name.lower() == 'pattern':
                    data['pattern'] = prod_attr.value
        return data


class Attribute:
    __name__ = 'product.attribute'

    def get_google_type(self):
        if self.type_ in ('boolean', 'float'):
            return self.type_
        elif self.type_ == 'integer':
            return 'int'
        elif self.type_ == 'numeric':
            return 'price'
        elif self.type_ == 'selection':
            return 'group'
        return 'string'


class GoogleTaxonomy(ModelSQL, ModelView):
    "Google product taxonomy"
    __name__ = 'product.google_taxonomy'

    google_id = fields.Integer('Google ID', required=True, select=True)
    name = fields.Char('Name', required=True, select=True)

    @classmethod
    def fetch_and_create(cls):
        """
        Fetch the entire taxonomy tree from google and create it
        """
        url = 'http://www.google.com/basepages/producttype/taxonomy-with-ids.en-US.txt'     # noqa
        data = []
        expr = re.compile(r'(\d+) - (.+)')
        for row in requests.get(url).content.split('\n'):
            match = expr.match(row)
            if match and not cls.search([('google_id', '=', int(match[0]))]):
                data.append({
                    'name': match[1],
                    'google_id': int(match[0]),
                })
        return cls.create(data)


class ProductGoogleTaxonomyRel(ModelSQL):
    "Product Google Taxonomy Relation"
    __name__ = 'product.product-product.google_taxonomy'

    product = fields.Many2One(
        'product.product', 'Product', required=True, select=True
    )
    taxonomy = fields.Many2One(
        'product.google_taxonomy', 'Taxonomy', required=True, select=True
    )
