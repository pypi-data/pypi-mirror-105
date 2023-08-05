# coding: utf-8

"""
    Intrinio API

    Welcome to the Intrinio API! Through our Financial Data Marketplace, we offer a wide selection of financial data feed APIs sourced by our own proprietary processes as well as from many data vendors. For a complete API request / response reference please view the [Intrinio API documentation](https://intrinio.com/documentation/api_v2). If you need additional help in using the API, please visit the [Intrinio website](https://intrinio.com) and click on the chat icon in the lower right corner.  # noqa: E501

    OpenAPI spec version: 2.21.1
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six

from intrinio_sdk.models.forex_pair import ForexPair  # noqa: F401,E501
from intrinio_sdk.models.forex_price import ForexPrice  # noqa: F401,E501


class ApiResponseForexPrices(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'prices': 'list[ForexPrice]',
        'pair': 'ForexPair',
        'next_page': 'str'
    }

    attribute_map = {
        'prices': 'prices',
        'pair': 'pair',
        'next_page': 'next_page'
    }

    def __init__(self, prices=None, pair=None, next_page=None):  # noqa: E501
        """ApiResponseForexPrices - a model defined in Swagger"""  # noqa: E501

        self._prices = None
        self._pair = None
        self._next_page = None
        self.discriminator = None

        if prices is not None:
            self.prices = prices
        if pair is not None:
            self.pair = pair
        if next_page is not None:
            self.next_page = next_page

    @property
    def prices(self):
        """Gets the prices of this ApiResponseForexPrices.  # noqa: E501


        :return: The prices of this ApiResponseForexPrices.  # noqa: E501
        :rtype: list[ForexPrice]
        """
        return self._prices
        
    @property
    def prices_dict(self):
        """Gets the prices of this ApiResponseForexPrices.  # noqa: E501


        :return: The prices of this ApiResponseForexPrices.  # noqa: E501
        :rtype: list[ForexPrice]
        """

        result = None

        value = self.prices
        if isinstance(value, list):
            result = list(map(
                lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                value
            ))
        elif hasattr(value, "to_dict"):
            result = value.to_dict()
        elif isinstance(value, dict):
            result = dict(map(
                lambda item: (item[0], item[1].to_dict())
                if hasattr(item[1], "to_dict") else item,
                value.items()
            ))
        else:
            result = { 'prices': value }

        
        return result
        

    @prices.setter
    def prices(self, prices):
        """Sets the prices of this ApiResponseForexPrices.


        :param prices: The prices of this ApiResponseForexPrices.  # noqa: E501
        :type: list[ForexPrice]
        """

        self._prices = prices

    @property
    def pair(self):
        """Gets the pair of this ApiResponseForexPrices.  # noqa: E501

        The Forex currency pair for which prices were requested  # noqa: E501

        :return: The pair of this ApiResponseForexPrices.  # noqa: E501
        :rtype: ForexPair
        """
        return self._pair
        
    @property
    def pair_dict(self):
        """Gets the pair of this ApiResponseForexPrices.  # noqa: E501

        The Forex currency pair for which prices were requested as a dictionary. Useful for Panda Dataframes.  # noqa: E501

        :return: The pair of this ApiResponseForexPrices.  # noqa: E501
        :rtype: ForexPair
        """

        result = None

        value = self.pair
        if isinstance(value, list):
            result = list(map(
                lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                value
            ))
        elif hasattr(value, "to_dict"):
            result = value.to_dict()
        elif isinstance(value, dict):
            result = dict(map(
                lambda item: (item[0], item[1].to_dict())
                if hasattr(item[1], "to_dict") else item,
                value.items()
            ))
        else:
            result = { 'pair': value }

        
        return result
        

    @pair.setter
    def pair(self, pair):
        """Sets the pair of this ApiResponseForexPrices.

        The Forex currency pair for which prices were requested  # noqa: E501

        :param pair: The pair of this ApiResponseForexPrices.  # noqa: E501
        :type: ForexPair
        """

        self._pair = pair

    @property
    def next_page(self):
        """Gets the next_page of this ApiResponseForexPrices.  # noqa: E501

        The token required to request the next page of the data. If null, no further results are available.  # noqa: E501

        :return: The next_page of this ApiResponseForexPrices.  # noqa: E501
        :rtype: str
        """
        return self._next_page
        
    @property
    def next_page_dict(self):
        """Gets the next_page of this ApiResponseForexPrices.  # noqa: E501

        The token required to request the next page of the data. If null, no further results are available. as a dictionary. Useful for Panda Dataframes.  # noqa: E501

        :return: The next_page of this ApiResponseForexPrices.  # noqa: E501
        :rtype: str
        """

        result = None

        value = self.next_page
        if isinstance(value, list):
            result = list(map(
                lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                value
            ))
        elif hasattr(value, "to_dict"):
            result = value.to_dict()
        elif isinstance(value, dict):
            result = dict(map(
                lambda item: (item[0], item[1].to_dict())
                if hasattr(item[1], "to_dict") else item,
                value.items()
            ))
        else:
            result = { 'next_page': value }

        
        return result
        

    @next_page.setter
    def next_page(self, next_page):
        """Sets the next_page of this ApiResponseForexPrices.

        The token required to request the next page of the data. If null, no further results are available.  # noqa: E501

        :param next_page: The next_page of this ApiResponseForexPrices.  # noqa: E501
        :type: str
        """

        self._next_page = next_page

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, ApiResponseForexPrices):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
