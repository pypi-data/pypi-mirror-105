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


class ZacksEPSSurpriseSummary(object):
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
        'id': 'str',
        'fiscal_year': 'float',
        'fiscal_quarter': 'str',
        'calendar_year': 'float',
        'calendar_quarter': 'str',
        'actual_reported_date': 'date',
        'actual_reported_time': 'str',
        'actual_reported_code': 'str',
        'actual_reported_desc': 'str',
        'eps_actual': 'float',
        'eps_actual_zacks_adj': 'float',
        'eps_mean_estimate': 'float',
        'eps_amount_diff': 'float',
        'eps_percent_diff': 'float',
        'eps_count_estimate': 'float',
        'eps_std_dev_estimate': 'float'
    }

    attribute_map = {
        'id': 'id',
        'fiscal_year': 'fiscal_year',
        'fiscal_quarter': 'fiscal_quarter',
        'calendar_year': 'calendar_year',
        'calendar_quarter': 'calendar_quarter',
        'actual_reported_date': 'actual_reported_date',
        'actual_reported_time': 'actual_reported_time',
        'actual_reported_code': 'actual_reported_code',
        'actual_reported_desc': 'actual_reported_desc',
        'eps_actual': 'eps_actual',
        'eps_actual_zacks_adj': 'eps_actual_zacks_adj',
        'eps_mean_estimate': 'eps_mean_estimate',
        'eps_amount_diff': 'eps_amount_diff',
        'eps_percent_diff': 'eps_percent_diff',
        'eps_count_estimate': 'eps_count_estimate',
        'eps_std_dev_estimate': 'eps_std_dev_estimate'
    }

    def __init__(self, id=None, fiscal_year=None, fiscal_quarter=None, calendar_year=None, calendar_quarter=None, actual_reported_date=None, actual_reported_time=None, actual_reported_code=None, actual_reported_desc=None, eps_actual=None, eps_actual_zacks_adj=None, eps_mean_estimate=None, eps_amount_diff=None, eps_percent_diff=None, eps_count_estimate=None, eps_std_dev_estimate=None):  # noqa: E501
        """ZacksEPSSurpriseSummary - a model defined in Swagger"""  # noqa: E501

        self._id = None
        self._fiscal_year = None
        self._fiscal_quarter = None
        self._calendar_year = None
        self._calendar_quarter = None
        self._actual_reported_date = None
        self._actual_reported_time = None
        self._actual_reported_code = None
        self._actual_reported_desc = None
        self._eps_actual = None
        self._eps_actual_zacks_adj = None
        self._eps_mean_estimate = None
        self._eps_amount_diff = None
        self._eps_percent_diff = None
        self._eps_count_estimate = None
        self._eps_std_dev_estimate = None
        self.discriminator = None

        if id is not None:
            self.id = id
        if fiscal_year is not None:
            self.fiscal_year = fiscal_year
        if fiscal_quarter is not None:
            self.fiscal_quarter = fiscal_quarter
        if calendar_year is not None:
            self.calendar_year = calendar_year
        if calendar_quarter is not None:
            self.calendar_quarter = calendar_quarter
        if actual_reported_date is not None:
            self.actual_reported_date = actual_reported_date
        if actual_reported_time is not None:
            self.actual_reported_time = actual_reported_time
        if actual_reported_code is not None:
            self.actual_reported_code = actual_reported_code
        if actual_reported_desc is not None:
            self.actual_reported_desc = actual_reported_desc
        if eps_actual is not None:
            self.eps_actual = eps_actual
        if eps_actual_zacks_adj is not None:
            self.eps_actual_zacks_adj = eps_actual_zacks_adj
        if eps_mean_estimate is not None:
            self.eps_mean_estimate = eps_mean_estimate
        if eps_amount_diff is not None:
            self.eps_amount_diff = eps_amount_diff
        if eps_percent_diff is not None:
            self.eps_percent_diff = eps_percent_diff
        if eps_count_estimate is not None:
            self.eps_count_estimate = eps_count_estimate
        if eps_std_dev_estimate is not None:
            self.eps_std_dev_estimate = eps_std_dev_estimate

    @property
    def id(self):
        """Gets the id of this ZacksEPSSurpriseSummary.  # noqa: E501

        The Intrinio ID for the record  # noqa: E501

        :return: The id of this ZacksEPSSurpriseSummary.  # noqa: E501
        :rtype: str
        """
        return self._id
        
    @property
    def id_dict(self):
        """Gets the id of this ZacksEPSSurpriseSummary.  # noqa: E501

        The Intrinio ID for the record as a dictionary. Useful for Panda Dataframes.  # noqa: E501

        :return: The id of this ZacksEPSSurpriseSummary.  # noqa: E501
        :rtype: str
        """

        result = None

        value = self.id
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
            result = { 'id': value }

        
        return result
        

    @id.setter
    def id(self, id):
        """Sets the id of this ZacksEPSSurpriseSummary.

        The Intrinio ID for the record  # noqa: E501

        :param id: The id of this ZacksEPSSurpriseSummary.  # noqa: E501
        :type: str
        """

        self._id = id

    @property
    def fiscal_year(self):
        """Gets the fiscal_year of this ZacksEPSSurpriseSummary.  # noqa: E501

        The company’s fiscal year for the reported period  # noqa: E501

        :return: The fiscal_year of this ZacksEPSSurpriseSummary.  # noqa: E501
        :rtype: float
        """
        return self._fiscal_year
        
    @property
    def fiscal_year_dict(self):
        """Gets the fiscal_year of this ZacksEPSSurpriseSummary.  # noqa: E501

        The company’s fiscal year for the reported period as a dictionary. Useful for Panda Dataframes.  # noqa: E501

        :return: The fiscal_year of this ZacksEPSSurpriseSummary.  # noqa: E501
        :rtype: float
        """

        result = None

        value = self.fiscal_year
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
            result = { 'fiscal_year': value }

        
        return result
        

    @fiscal_year.setter
    def fiscal_year(self, fiscal_year):
        """Sets the fiscal_year of this ZacksEPSSurpriseSummary.

        The company’s fiscal year for the reported period  # noqa: E501

        :param fiscal_year: The fiscal_year of this ZacksEPSSurpriseSummary.  # noqa: E501
        :type: float
        """

        self._fiscal_year = fiscal_year

    @property
    def fiscal_quarter(self):
        """Gets the fiscal_quarter of this ZacksEPSSurpriseSummary.  # noqa: E501

        The company’s fiscal quarter for the reported period  # noqa: E501

        :return: The fiscal_quarter of this ZacksEPSSurpriseSummary.  # noqa: E501
        :rtype: str
        """
        return self._fiscal_quarter
        
    @property
    def fiscal_quarter_dict(self):
        """Gets the fiscal_quarter of this ZacksEPSSurpriseSummary.  # noqa: E501

        The company’s fiscal quarter for the reported period as a dictionary. Useful for Panda Dataframes.  # noqa: E501

        :return: The fiscal_quarter of this ZacksEPSSurpriseSummary.  # noqa: E501
        :rtype: str
        """

        result = None

        value = self.fiscal_quarter
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
            result = { 'fiscal_quarter': value }

        
        return result
        

    @fiscal_quarter.setter
    def fiscal_quarter(self, fiscal_quarter):
        """Sets the fiscal_quarter of this ZacksEPSSurpriseSummary.

        The company’s fiscal quarter for the reported period  # noqa: E501

        :param fiscal_quarter: The fiscal_quarter of this ZacksEPSSurpriseSummary.  # noqa: E501
        :type: str
        """

        self._fiscal_quarter = fiscal_quarter

    @property
    def calendar_year(self):
        """Gets the calendar_year of this ZacksEPSSurpriseSummary.  # noqa: E501

        The closest calendar year for the company’s fiscal year  # noqa: E501

        :return: The calendar_year of this ZacksEPSSurpriseSummary.  # noqa: E501
        :rtype: float
        """
        return self._calendar_year
        
    @property
    def calendar_year_dict(self):
        """Gets the calendar_year of this ZacksEPSSurpriseSummary.  # noqa: E501

        The closest calendar year for the company’s fiscal year as a dictionary. Useful for Panda Dataframes.  # noqa: E501

        :return: The calendar_year of this ZacksEPSSurpriseSummary.  # noqa: E501
        :rtype: float
        """

        result = None

        value = self.calendar_year
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
            result = { 'calendar_year': value }

        
        return result
        

    @calendar_year.setter
    def calendar_year(self, calendar_year):
        """Sets the calendar_year of this ZacksEPSSurpriseSummary.

        The closest calendar year for the company’s fiscal year  # noqa: E501

        :param calendar_year: The calendar_year of this ZacksEPSSurpriseSummary.  # noqa: E501
        :type: float
        """

        self._calendar_year = calendar_year

    @property
    def calendar_quarter(self):
        """Gets the calendar_quarter of this ZacksEPSSurpriseSummary.  # noqa: E501

        The closest calendar quarter for the company’s fiscal year  # noqa: E501

        :return: The calendar_quarter of this ZacksEPSSurpriseSummary.  # noqa: E501
        :rtype: str
        """
        return self._calendar_quarter
        
    @property
    def calendar_quarter_dict(self):
        """Gets the calendar_quarter of this ZacksEPSSurpriseSummary.  # noqa: E501

        The closest calendar quarter for the company’s fiscal year as a dictionary. Useful for Panda Dataframes.  # noqa: E501

        :return: The calendar_quarter of this ZacksEPSSurpriseSummary.  # noqa: E501
        :rtype: str
        """

        result = None

        value = self.calendar_quarter
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
            result = { 'calendar_quarter': value }

        
        return result
        

    @calendar_quarter.setter
    def calendar_quarter(self, calendar_quarter):
        """Sets the calendar_quarter of this ZacksEPSSurpriseSummary.

        The closest calendar quarter for the company’s fiscal year  # noqa: E501

        :param calendar_quarter: The calendar_quarter of this ZacksEPSSurpriseSummary.  # noqa: E501
        :type: str
        """

        self._calendar_quarter = calendar_quarter

    @property
    def actual_reported_date(self):
        """Gets the actual_reported_date of this ZacksEPSSurpriseSummary.  # noqa: E501

        The actual report date for the earnings release  # noqa: E501

        :return: The actual_reported_date of this ZacksEPSSurpriseSummary.  # noqa: E501
        :rtype: date
        """
        return self._actual_reported_date
        
    @property
    def actual_reported_date_dict(self):
        """Gets the actual_reported_date of this ZacksEPSSurpriseSummary.  # noqa: E501

        The actual report date for the earnings release as a dictionary. Useful for Panda Dataframes.  # noqa: E501

        :return: The actual_reported_date of this ZacksEPSSurpriseSummary.  # noqa: E501
        :rtype: date
        """

        result = None

        value = self.actual_reported_date
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
            result = { 'actual_reported_date': value }

        
        return result
        

    @actual_reported_date.setter
    def actual_reported_date(self, actual_reported_date):
        """Sets the actual_reported_date of this ZacksEPSSurpriseSummary.

        The actual report date for the earnings release  # noqa: E501

        :param actual_reported_date: The actual_reported_date of this ZacksEPSSurpriseSummary.  # noqa: E501
        :type: date
        """

        self._actual_reported_date = actual_reported_date

    @property
    def actual_reported_time(self):
        """Gets the actual_reported_time of this ZacksEPSSurpriseSummary.  # noqa: E501

        The actual report time for the earnings release  # noqa: E501

        :return: The actual_reported_time of this ZacksEPSSurpriseSummary.  # noqa: E501
        :rtype: str
        """
        return self._actual_reported_time
        
    @property
    def actual_reported_time_dict(self):
        """Gets the actual_reported_time of this ZacksEPSSurpriseSummary.  # noqa: E501

        The actual report time for the earnings release as a dictionary. Useful for Panda Dataframes.  # noqa: E501

        :return: The actual_reported_time of this ZacksEPSSurpriseSummary.  # noqa: E501
        :rtype: str
        """

        result = None

        value = self.actual_reported_time
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
            result = { 'actual_reported_time': value }

        
        return result
        

    @actual_reported_time.setter
    def actual_reported_time(self, actual_reported_time):
        """Sets the actual_reported_time of this ZacksEPSSurpriseSummary.

        The actual report time for the earnings release  # noqa: E501

        :param actual_reported_time: The actual_reported_time of this ZacksEPSSurpriseSummary.  # noqa: E501
        :type: str
        """

        self._actual_reported_time = actual_reported_time

    @property
    def actual_reported_code(self):
        """Gets the actual_reported_code of this ZacksEPSSurpriseSummary.  # noqa: E501

        The code cooresponding to the earnings release  BTO = BEFORE THE OPEN | DTM = DURING THE MARKET | AMC = AFTER MARKET CLOSE  # noqa: E501

        :return: The actual_reported_code of this ZacksEPSSurpriseSummary.  # noqa: E501
        :rtype: str
        """
        return self._actual_reported_code
        
    @property
    def actual_reported_code_dict(self):
        """Gets the actual_reported_code of this ZacksEPSSurpriseSummary.  # noqa: E501

        The code cooresponding to the earnings release  BTO = BEFORE THE OPEN | DTM = DURING THE MARKET | AMC = AFTER MARKET CLOSE as a dictionary. Useful for Panda Dataframes.  # noqa: E501

        :return: The actual_reported_code of this ZacksEPSSurpriseSummary.  # noqa: E501
        :rtype: str
        """

        result = None

        value = self.actual_reported_code
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
            result = { 'actual_reported_code': value }

        
        return result
        

    @actual_reported_code.setter
    def actual_reported_code(self, actual_reported_code):
        """Sets the actual_reported_code of this ZacksEPSSurpriseSummary.

        The code cooresponding to the earnings release  BTO = BEFORE THE OPEN | DTM = DURING THE MARKET | AMC = AFTER MARKET CLOSE  # noqa: E501

        :param actual_reported_code: The actual_reported_code of this ZacksEPSSurpriseSummary.  # noqa: E501
        :type: str
        """

        self._actual_reported_code = actual_reported_code

    @property
    def actual_reported_desc(self):
        """Gets the actual_reported_desc of this ZacksEPSSurpriseSummary.  # noqa: E501

        The description for the type of earnings release  # noqa: E501

        :return: The actual_reported_desc of this ZacksEPSSurpriseSummary.  # noqa: E501
        :rtype: str
        """
        return self._actual_reported_desc
        
    @property
    def actual_reported_desc_dict(self):
        """Gets the actual_reported_desc of this ZacksEPSSurpriseSummary.  # noqa: E501

        The description for the type of earnings release as a dictionary. Useful for Panda Dataframes.  # noqa: E501

        :return: The actual_reported_desc of this ZacksEPSSurpriseSummary.  # noqa: E501
        :rtype: str
        """

        result = None

        value = self.actual_reported_desc
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
            result = { 'actual_reported_desc': value }

        
        return result
        

    @actual_reported_desc.setter
    def actual_reported_desc(self, actual_reported_desc):
        """Sets the actual_reported_desc of this ZacksEPSSurpriseSummary.

        The description for the type of earnings release  # noqa: E501

        :param actual_reported_desc: The actual_reported_desc of this ZacksEPSSurpriseSummary.  # noqa: E501
        :type: str
        """

        self._actual_reported_desc = actual_reported_desc

    @property
    def eps_actual(self):
        """Gets the eps_actual of this ZacksEPSSurpriseSummary.  # noqa: E501

        The actual Non-GAAP EPS figure released by the company, interpreted by Zacks.  # noqa: E501

        :return: The eps_actual of this ZacksEPSSurpriseSummary.  # noqa: E501
        :rtype: float
        """
        return self._eps_actual
        
    @property
    def eps_actual_dict(self):
        """Gets the eps_actual of this ZacksEPSSurpriseSummary.  # noqa: E501

        The actual Non-GAAP EPS figure released by the company, interpreted by Zacks. as a dictionary. Useful for Panda Dataframes.  # noqa: E501

        :return: The eps_actual of this ZacksEPSSurpriseSummary.  # noqa: E501
        :rtype: float
        """

        result = None

        value = self.eps_actual
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
            result = { 'eps_actual': value }

        
        return result
        

    @eps_actual.setter
    def eps_actual(self, eps_actual):
        """Sets the eps_actual of this ZacksEPSSurpriseSummary.

        The actual Non-GAAP EPS figure released by the company, interpreted by Zacks.  # noqa: E501

        :param eps_actual: The eps_actual of this ZacksEPSSurpriseSummary.  # noqa: E501
        :type: float
        """

        self._eps_actual = eps_actual

    @property
    def eps_actual_zacks_adj(self):
        """Gets the eps_actual_zacks_adj of this ZacksEPSSurpriseSummary.  # noqa: E501

        The adjustments Zacks made to get to Non-GAAP EPS to reconcile with GAAP EPS.  # noqa: E501

        :return: The eps_actual_zacks_adj of this ZacksEPSSurpriseSummary.  # noqa: E501
        :rtype: float
        """
        return self._eps_actual_zacks_adj
        
    @property
    def eps_actual_zacks_adj_dict(self):
        """Gets the eps_actual_zacks_adj of this ZacksEPSSurpriseSummary.  # noqa: E501

        The adjustments Zacks made to get to Non-GAAP EPS to reconcile with GAAP EPS. as a dictionary. Useful for Panda Dataframes.  # noqa: E501

        :return: The eps_actual_zacks_adj of this ZacksEPSSurpriseSummary.  # noqa: E501
        :rtype: float
        """

        result = None

        value = self.eps_actual_zacks_adj
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
            result = { 'eps_actual_zacks_adj': value }

        
        return result
        

    @eps_actual_zacks_adj.setter
    def eps_actual_zacks_adj(self, eps_actual_zacks_adj):
        """Sets the eps_actual_zacks_adj of this ZacksEPSSurpriseSummary.

        The adjustments Zacks made to get to Non-GAAP EPS to reconcile with GAAP EPS.  # noqa: E501

        :param eps_actual_zacks_adj: The eps_actual_zacks_adj of this ZacksEPSSurpriseSummary.  # noqa: E501
        :type: float
        """

        self._eps_actual_zacks_adj = eps_actual_zacks_adj

    @property
    def eps_mean_estimate(self):
        """Gets the eps_mean_estimate of this ZacksEPSSurpriseSummary.  # noqa: E501

        The pre-earnings release mean EPS estimate for the company  # noqa: E501

        :return: The eps_mean_estimate of this ZacksEPSSurpriseSummary.  # noqa: E501
        :rtype: float
        """
        return self._eps_mean_estimate
        
    @property
    def eps_mean_estimate_dict(self):
        """Gets the eps_mean_estimate of this ZacksEPSSurpriseSummary.  # noqa: E501

        The pre-earnings release mean EPS estimate for the company as a dictionary. Useful for Panda Dataframes.  # noqa: E501

        :return: The eps_mean_estimate of this ZacksEPSSurpriseSummary.  # noqa: E501
        :rtype: float
        """

        result = None

        value = self.eps_mean_estimate
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
            result = { 'eps_mean_estimate': value }

        
        return result
        

    @eps_mean_estimate.setter
    def eps_mean_estimate(self, eps_mean_estimate):
        """Sets the eps_mean_estimate of this ZacksEPSSurpriseSummary.

        The pre-earnings release mean EPS estimate for the company  # noqa: E501

        :param eps_mean_estimate: The eps_mean_estimate of this ZacksEPSSurpriseSummary.  # noqa: E501
        :type: float
        """

        self._eps_mean_estimate = eps_mean_estimate

    @property
    def eps_amount_diff(self):
        """Gets the eps_amount_diff of this ZacksEPSSurpriseSummary.  # noqa: E501

        The EPS surprise amount difference  # noqa: E501

        :return: The eps_amount_diff of this ZacksEPSSurpriseSummary.  # noqa: E501
        :rtype: float
        """
        return self._eps_amount_diff
        
    @property
    def eps_amount_diff_dict(self):
        """Gets the eps_amount_diff of this ZacksEPSSurpriseSummary.  # noqa: E501

        The EPS surprise amount difference as a dictionary. Useful for Panda Dataframes.  # noqa: E501

        :return: The eps_amount_diff of this ZacksEPSSurpriseSummary.  # noqa: E501
        :rtype: float
        """

        result = None

        value = self.eps_amount_diff
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
            result = { 'eps_amount_diff': value }

        
        return result
        

    @eps_amount_diff.setter
    def eps_amount_diff(self, eps_amount_diff):
        """Sets the eps_amount_diff of this ZacksEPSSurpriseSummary.

        The EPS surprise amount difference  # noqa: E501

        :param eps_amount_diff: The eps_amount_diff of this ZacksEPSSurpriseSummary.  # noqa: E501
        :type: float
        """

        self._eps_amount_diff = eps_amount_diff

    @property
    def eps_percent_diff(self):
        """Gets the eps_percent_diff of this ZacksEPSSurpriseSummary.  # noqa: E501

        The EPS surprise percent difference  # noqa: E501

        :return: The eps_percent_diff of this ZacksEPSSurpriseSummary.  # noqa: E501
        :rtype: float
        """
        return self._eps_percent_diff
        
    @property
    def eps_percent_diff_dict(self):
        """Gets the eps_percent_diff of this ZacksEPSSurpriseSummary.  # noqa: E501

        The EPS surprise percent difference as a dictionary. Useful for Panda Dataframes.  # noqa: E501

        :return: The eps_percent_diff of this ZacksEPSSurpriseSummary.  # noqa: E501
        :rtype: float
        """

        result = None

        value = self.eps_percent_diff
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
            result = { 'eps_percent_diff': value }

        
        return result
        

    @eps_percent_diff.setter
    def eps_percent_diff(self, eps_percent_diff):
        """Sets the eps_percent_diff of this ZacksEPSSurpriseSummary.

        The EPS surprise percent difference  # noqa: E501

        :param eps_percent_diff: The eps_percent_diff of this ZacksEPSSurpriseSummary.  # noqa: E501
        :type: float
        """

        self._eps_percent_diff = eps_percent_diff

    @property
    def eps_count_estimate(self):
        """Gets the eps_count_estimate of this ZacksEPSSurpriseSummary.  # noqa: E501

        The pre-earnings release number of estimates by analysts  # noqa: E501

        :return: The eps_count_estimate of this ZacksEPSSurpriseSummary.  # noqa: E501
        :rtype: float
        """
        return self._eps_count_estimate
        
    @property
    def eps_count_estimate_dict(self):
        """Gets the eps_count_estimate of this ZacksEPSSurpriseSummary.  # noqa: E501

        The pre-earnings release number of estimates by analysts as a dictionary. Useful for Panda Dataframes.  # noqa: E501

        :return: The eps_count_estimate of this ZacksEPSSurpriseSummary.  # noqa: E501
        :rtype: float
        """

        result = None

        value = self.eps_count_estimate
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
            result = { 'eps_count_estimate': value }

        
        return result
        

    @eps_count_estimate.setter
    def eps_count_estimate(self, eps_count_estimate):
        """Sets the eps_count_estimate of this ZacksEPSSurpriseSummary.

        The pre-earnings release number of estimates by analysts  # noqa: E501

        :param eps_count_estimate: The eps_count_estimate of this ZacksEPSSurpriseSummary.  # noqa: E501
        :type: float
        """

        self._eps_count_estimate = eps_count_estimate

    @property
    def eps_std_dev_estimate(self):
        """Gets the eps_std_dev_estimate of this ZacksEPSSurpriseSummary.  # noqa: E501

        The pre-earnings release standard deviation of EPS estimates  # noqa: E501

        :return: The eps_std_dev_estimate of this ZacksEPSSurpriseSummary.  # noqa: E501
        :rtype: float
        """
        return self._eps_std_dev_estimate
        
    @property
    def eps_std_dev_estimate_dict(self):
        """Gets the eps_std_dev_estimate of this ZacksEPSSurpriseSummary.  # noqa: E501

        The pre-earnings release standard deviation of EPS estimates as a dictionary. Useful for Panda Dataframes.  # noqa: E501

        :return: The eps_std_dev_estimate of this ZacksEPSSurpriseSummary.  # noqa: E501
        :rtype: float
        """

        result = None

        value = self.eps_std_dev_estimate
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
            result = { 'eps_std_dev_estimate': value }

        
        return result
        

    @eps_std_dev_estimate.setter
    def eps_std_dev_estimate(self, eps_std_dev_estimate):
        """Sets the eps_std_dev_estimate of this ZacksEPSSurpriseSummary.

        The pre-earnings release standard deviation of EPS estimates  # noqa: E501

        :param eps_std_dev_estimate: The eps_std_dev_estimate of this ZacksEPSSurpriseSummary.  # noqa: E501
        :type: float
        """

        self._eps_std_dev_estimate = eps_std_dev_estimate

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
        if not isinstance(other, ZacksEPSSurpriseSummary):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
