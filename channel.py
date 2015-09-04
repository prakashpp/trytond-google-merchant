# -*- coding: utf-8 -*-
"""
    channel.py

    :copyright: (c) 2015 by Fulfil.IO Inc.
    :license: see LICENSE for more details.
"""
from trytond.pool import PoolMeta
from trytond.model import fields

__all__ = ['Channel']
__metaclass__ = PoolMeta


def submit_to_google(url, data):
    import requests
    import json

    return requests.post(
        url,
        data=json.dumps(data),
        headers={
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ya29.5AE7v1wOfgun1gR_iXwuGhMnt8nPNbT4C-Pd39DUnsNGb9I6U5FQqRJXNyPb3a0Dk1OWzA',  # noqa
        }
    )


class Channel:
    __name__ = "sale.channel"

    website = fields.Many2One('nereid.website', 'Website', select=True)

    @classmethod
    def upload_products_to_google_merchant(cls):
        pass
