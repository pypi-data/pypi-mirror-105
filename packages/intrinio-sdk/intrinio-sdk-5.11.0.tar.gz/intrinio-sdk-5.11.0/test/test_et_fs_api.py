# coding: utf-8

"""
    Intrinio API

    Welcome to the Intrinio API! Through our Financial Data Marketplace, we offer a wide selection of financial data feed APIs sourced by our own proprietary processes as well as from many data vendors. For a complete API request / response reference please view the [Intrinio API documentation](https://intrinio.com/documentation/api_v2). If you need additional help in using the API, please visit the [Intrinio website](https://intrinio.com) and click on the chat icon in the lower right corner.  # noqa: E501

    OpenAPI spec version: 2.21.1
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from __future__ import absolute_import

import unittest

import intrinio_sdk
from intrinio_sdk.api.et_fs_api import ETFsApi  # noqa: E501
from intrinio_sdk.rest import ApiException


class TestETFsApi(unittest.TestCase):
    """ETFsApi unit test stubs"""

    def setUp(self):
        self.api = intrinio_sdk.api.et_fs_api.ETFsApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_get_all_etfs(self):
        """Test case for get_all_etfs

        All ETFs  # noqa: E501
        """
        pass

    def test_get_etf(self):
        """Test case for get_etf

        Lookup ETF  # noqa: E501
        """
        pass

    def test_get_etf_analytics(self):
        """Test case for get_etf_analytics

        ETF Analytics  # noqa: E501
        """
        pass

    def test_get_etf_holdings(self):
        """Test case for get_etf_holdings

        ETF Holdings  # noqa: E501
        """
        pass

    def test_get_etf_stats(self):
        """Test case for get_etf_stats

        Exchange Traded Fund (ETF) stats  # noqa: E501
        """
        pass

    def test_search_etfs(self):
        """Test case for search_etfs

        Search ETFs  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
