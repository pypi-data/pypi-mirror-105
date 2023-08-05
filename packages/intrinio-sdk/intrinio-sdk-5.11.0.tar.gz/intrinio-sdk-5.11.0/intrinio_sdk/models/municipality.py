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


class Municipality(object):
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
        'census_id': 'float',
        'government_name': 'str',
        'government_type': 'str',
        'primary_contact_type': 'str',
        'address1': 'str',
        'address2': 'str',
        'city': 'str',
        'state': 'str',
        'zip': 'str',
        'web_site': 'str',
        'population': 'float',
        'population_as_of_year': 'float',
        'enrollment': 'float',
        'enrollment_as_of_year': 'float',
        'area_name': 'str',
        'area_type': 'str',
        'latitude': 'float',
        'longitude': 'float'
    }

    attribute_map = {
        'id': 'id',
        'census_id': 'census_id',
        'government_name': 'government_name',
        'government_type': 'government_type',
        'primary_contact_type': 'primary_contact_type',
        'address1': 'address1',
        'address2': 'address2',
        'city': 'city',
        'state': 'state',
        'zip': 'zip',
        'web_site': 'web_site',
        'population': 'population',
        'population_as_of_year': 'population_as_of_year',
        'enrollment': 'enrollment',
        'enrollment_as_of_year': 'enrollment_as_of_year',
        'area_name': 'area_name',
        'area_type': 'area_type',
        'latitude': 'latitude',
        'longitude': 'longitude'
    }

    def __init__(self, id=None, census_id=None, government_name=None, government_type=None, primary_contact_type=None, address1=None, address2=None, city=None, state=None, zip=None, web_site=None, population=None, population_as_of_year=None, enrollment=None, enrollment_as_of_year=None, area_name=None, area_type=None, latitude=None, longitude=None):  # noqa: E501
        """Municipality - a model defined in Swagger"""  # noqa: E501

        self._id = None
        self._census_id = None
        self._government_name = None
        self._government_type = None
        self._primary_contact_type = None
        self._address1 = None
        self._address2 = None
        self._city = None
        self._state = None
        self._zip = None
        self._web_site = None
        self._population = None
        self._population_as_of_year = None
        self._enrollment = None
        self._enrollment_as_of_year = None
        self._area_name = None
        self._area_type = None
        self._latitude = None
        self._longitude = None
        self.discriminator = None

        if id is not None:
            self.id = id
        if census_id is not None:
            self.census_id = census_id
        if government_name is not None:
            self.government_name = government_name
        if government_type is not None:
            self.government_type = government_type
        if primary_contact_type is not None:
            self.primary_contact_type = primary_contact_type
        if address1 is not None:
            self.address1 = address1
        if address2 is not None:
            self.address2 = address2
        if city is not None:
            self.city = city
        if state is not None:
            self.state = state
        if zip is not None:
            self.zip = zip
        if web_site is not None:
            self.web_site = web_site
        if population is not None:
            self.population = population
        if population_as_of_year is not None:
            self.population_as_of_year = population_as_of_year
        if enrollment is not None:
            self.enrollment = enrollment
        if enrollment_as_of_year is not None:
            self.enrollment_as_of_year = enrollment_as_of_year
        if area_name is not None:
            self.area_name = area_name
        if area_type is not None:
            self.area_type = area_type
        if latitude is not None:
            self.latitude = latitude
        if longitude is not None:
            self.longitude = longitude

    @property
    def id(self):
        """Gets the id of this Municipality.  # noqa: E501

        The Intrinio ID for Municipality  # noqa: E501

        :return: The id of this Municipality.  # noqa: E501
        :rtype: str
        """
        return self._id
        
    @property
    def id_dict(self):
        """Gets the id of this Municipality.  # noqa: E501

        The Intrinio ID for Municipality as a dictionary. Useful for Panda Dataframes.  # noqa: E501

        :return: The id of this Municipality.  # noqa: E501
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
        """Sets the id of this Municipality.

        The Intrinio ID for Municipality  # noqa: E501

        :param id: The id of this Municipality.  # noqa: E501
        :type: str
        """

        self._id = id

    @property
    def census_id(self):
        """Gets the census_id of this Municipality.  # noqa: E501

        The ID for the census  # noqa: E501

        :return: The census_id of this Municipality.  # noqa: E501
        :rtype: float
        """
        return self._census_id
        
    @property
    def census_id_dict(self):
        """Gets the census_id of this Municipality.  # noqa: E501

        The ID for the census as a dictionary. Useful for Panda Dataframes.  # noqa: E501

        :return: The census_id of this Municipality.  # noqa: E501
        :rtype: float
        """

        result = None

        value = self.census_id
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
            result = { 'census_id': value }

        
        return result
        

    @census_id.setter
    def census_id(self, census_id):
        """Sets the census_id of this Municipality.

        The ID for the census  # noqa: E501

        :param census_id: The census_id of this Municipality.  # noqa: E501
        :type: float
        """

        self._census_id = census_id

    @property
    def government_name(self):
        """Gets the government_name of this Municipality.  # noqa: E501

        The government name of the Municipality  # noqa: E501

        :return: The government_name of this Municipality.  # noqa: E501
        :rtype: str
        """
        return self._government_name
        
    @property
    def government_name_dict(self):
        """Gets the government_name of this Municipality.  # noqa: E501

        The government name of the Municipality as a dictionary. Useful for Panda Dataframes.  # noqa: E501

        :return: The government_name of this Municipality.  # noqa: E501
        :rtype: str
        """

        result = None

        value = self.government_name
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
            result = { 'government_name': value }

        
        return result
        

    @government_name.setter
    def government_name(self, government_name):
        """Sets the government_name of this Municipality.

        The government name of the Municipality  # noqa: E501

        :param government_name: The government_name of this Municipality.  # noqa: E501
        :type: str
        """

        self._government_name = government_name

    @property
    def government_type(self):
        """Gets the government_type of this Municipality.  # noqa: E501

        The type of government of the Municipality  # noqa: E501

        :return: The government_type of this Municipality.  # noqa: E501
        :rtype: str
        """
        return self._government_type
        
    @property
    def government_type_dict(self):
        """Gets the government_type of this Municipality.  # noqa: E501

        The type of government of the Municipality as a dictionary. Useful for Panda Dataframes.  # noqa: E501

        :return: The government_type of this Municipality.  # noqa: E501
        :rtype: str
        """

        result = None

        value = self.government_type
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
            result = { 'government_type': value }

        
        return result
        

    @government_type.setter
    def government_type(self, government_type):
        """Sets the government_type of this Municipality.

        The type of government of the Municipality  # noqa: E501

        :param government_type: The government_type of this Municipality.  # noqa: E501
        :type: str
        """

        self._government_type = government_type

    @property
    def primary_contact_type(self):
        """Gets the primary_contact_type of this Municipality.  # noqa: E501

        The primary contact type of the Municipality  # noqa: E501

        :return: The primary_contact_type of this Municipality.  # noqa: E501
        :rtype: str
        """
        return self._primary_contact_type
        
    @property
    def primary_contact_type_dict(self):
        """Gets the primary_contact_type of this Municipality.  # noqa: E501

        The primary contact type of the Municipality as a dictionary. Useful for Panda Dataframes.  # noqa: E501

        :return: The primary_contact_type of this Municipality.  # noqa: E501
        :rtype: str
        """

        result = None

        value = self.primary_contact_type
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
            result = { 'primary_contact_type': value }

        
        return result
        

    @primary_contact_type.setter
    def primary_contact_type(self, primary_contact_type):
        """Sets the primary_contact_type of this Municipality.

        The primary contact type of the Municipality  # noqa: E501

        :param primary_contact_type: The primary_contact_type of this Municipality.  # noqa: E501
        :type: str
        """

        self._primary_contact_type = primary_contact_type

    @property
    def address1(self):
        """Gets the address1 of this Municipality.  # noqa: E501

        The first line of the address  # noqa: E501

        :return: The address1 of this Municipality.  # noqa: E501
        :rtype: str
        """
        return self._address1
        
    @property
    def address1_dict(self):
        """Gets the address1 of this Municipality.  # noqa: E501

        The first line of the address as a dictionary. Useful for Panda Dataframes.  # noqa: E501

        :return: The address1 of this Municipality.  # noqa: E501
        :rtype: str
        """

        result = None

        value = self.address1
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
            result = { 'address1': value }

        
        return result
        

    @address1.setter
    def address1(self, address1):
        """Sets the address1 of this Municipality.

        The first line of the address  # noqa: E501

        :param address1: The address1 of this Municipality.  # noqa: E501
        :type: str
        """

        self._address1 = address1

    @property
    def address2(self):
        """Gets the address2 of this Municipality.  # noqa: E501

        The second line of the address (i.e. suite number)  # noqa: E501

        :return: The address2 of this Municipality.  # noqa: E501
        :rtype: str
        """
        return self._address2
        
    @property
    def address2_dict(self):
        """Gets the address2 of this Municipality.  # noqa: E501

        The second line of the address (i.e. suite number) as a dictionary. Useful for Panda Dataframes.  # noqa: E501

        :return: The address2 of this Municipality.  # noqa: E501
        :rtype: str
        """

        result = None

        value = self.address2
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
            result = { 'address2': value }

        
        return result
        

    @address2.setter
    def address2(self, address2):
        """Sets the address2 of this Municipality.

        The second line of the address (i.e. suite number)  # noqa: E501

        :param address2: The address2 of this Municipality.  # noqa: E501
        :type: str
        """

        self._address2 = address2

    @property
    def city(self):
        """Gets the city of this Municipality.  # noqa: E501

        The city in which the Municipality is located in  # noqa: E501

        :return: The city of this Municipality.  # noqa: E501
        :rtype: str
        """
        return self._city
        
    @property
    def city_dict(self):
        """Gets the city of this Municipality.  # noqa: E501

        The city in which the Municipality is located in as a dictionary. Useful for Panda Dataframes.  # noqa: E501

        :return: The city of this Municipality.  # noqa: E501
        :rtype: str
        """

        result = None

        value = self.city
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
            result = { 'city': value }

        
        return result
        

    @city.setter
    def city(self, city):
        """Sets the city of this Municipality.

        The city in which the Municipality is located in  # noqa: E501

        :param city: The city of this Municipality.  # noqa: E501
        :type: str
        """

        self._city = city

    @property
    def state(self):
        """Gets the state of this Municipality.  # noqa: E501

        The state in which the Municipality is located in  # noqa: E501

        :return: The state of this Municipality.  # noqa: E501
        :rtype: str
        """
        return self._state
        
    @property
    def state_dict(self):
        """Gets the state of this Municipality.  # noqa: E501

        The state in which the Municipality is located in as a dictionary. Useful for Panda Dataframes.  # noqa: E501

        :return: The state of this Municipality.  # noqa: E501
        :rtype: str
        """

        result = None

        value = self.state
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
            result = { 'state': value }

        
        return result
        

    @state.setter
    def state(self, state):
        """Sets the state of this Municipality.

        The state in which the Municipality is located in  # noqa: E501

        :param state: The state of this Municipality.  # noqa: E501
        :type: str
        """

        self._state = state

    @property
    def zip(self):
        """Gets the zip of this Municipality.  # noqa: E501

        The zip code in which the Municipality is located in  # noqa: E501

        :return: The zip of this Municipality.  # noqa: E501
        :rtype: str
        """
        return self._zip
        
    @property
    def zip_dict(self):
        """Gets the zip of this Municipality.  # noqa: E501

        The zip code in which the Municipality is located in as a dictionary. Useful for Panda Dataframes.  # noqa: E501

        :return: The zip of this Municipality.  # noqa: E501
        :rtype: str
        """

        result = None

        value = self.zip
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
            result = { 'zip': value }

        
        return result
        

    @zip.setter
    def zip(self, zip):
        """Sets the zip of this Municipality.

        The zip code in which the Municipality is located in  # noqa: E501

        :param zip: The zip of this Municipality.  # noqa: E501
        :type: str
        """

        self._zip = zip

    @property
    def web_site(self):
        """Gets the web_site of this Municipality.  # noqa: E501

        The web site of the Municipality  # noqa: E501

        :return: The web_site of this Municipality.  # noqa: E501
        :rtype: str
        """
        return self._web_site
        
    @property
    def web_site_dict(self):
        """Gets the web_site of this Municipality.  # noqa: E501

        The web site of the Municipality as a dictionary. Useful for Panda Dataframes.  # noqa: E501

        :return: The web_site of this Municipality.  # noqa: E501
        :rtype: str
        """

        result = None

        value = self.web_site
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
            result = { 'web_site': value }

        
        return result
        

    @web_site.setter
    def web_site(self, web_site):
        """Sets the web_site of this Municipality.

        The web site of the Municipality  # noqa: E501

        :param web_site: The web_site of this Municipality.  # noqa: E501
        :type: str
        """

        self._web_site = web_site

    @property
    def population(self):
        """Gets the population of this Municipality.  # noqa: E501

        The population of the Municipality  # noqa: E501

        :return: The population of this Municipality.  # noqa: E501
        :rtype: float
        """
        return self._population
        
    @property
    def population_dict(self):
        """Gets the population of this Municipality.  # noqa: E501

        The population of the Municipality as a dictionary. Useful for Panda Dataframes.  # noqa: E501

        :return: The population of this Municipality.  # noqa: E501
        :rtype: float
        """

        result = None

        value = self.population
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
            result = { 'population': value }

        
        return result
        

    @population.setter
    def population(self, population):
        """Sets the population of this Municipality.

        The population of the Municipality  # noqa: E501

        :param population: The population of this Municipality.  # noqa: E501
        :type: float
        """

        self._population = population

    @property
    def population_as_of_year(self):
        """Gets the population_as_of_year of this Municipality.  # noqa: E501

        The year from which the population of the Municipality was measured  # noqa: E501

        :return: The population_as_of_year of this Municipality.  # noqa: E501
        :rtype: float
        """
        return self._population_as_of_year
        
    @property
    def population_as_of_year_dict(self):
        """Gets the population_as_of_year of this Municipality.  # noqa: E501

        The year from which the population of the Municipality was measured as a dictionary. Useful for Panda Dataframes.  # noqa: E501

        :return: The population_as_of_year of this Municipality.  # noqa: E501
        :rtype: float
        """

        result = None

        value = self.population_as_of_year
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
            result = { 'population_as_of_year': value }

        
        return result
        

    @population_as_of_year.setter
    def population_as_of_year(self, population_as_of_year):
        """Sets the population_as_of_year of this Municipality.

        The year from which the population of the Municipality was measured  # noqa: E501

        :param population_as_of_year: The population_as_of_year of this Municipality.  # noqa: E501
        :type: float
        """

        self._population_as_of_year = population_as_of_year

    @property
    def enrollment(self):
        """Gets the enrollment of this Municipality.  # noqa: E501

        The enrollment of the Municipality  # noqa: E501

        :return: The enrollment of this Municipality.  # noqa: E501
        :rtype: float
        """
        return self._enrollment
        
    @property
    def enrollment_dict(self):
        """Gets the enrollment of this Municipality.  # noqa: E501

        The enrollment of the Municipality as a dictionary. Useful for Panda Dataframes.  # noqa: E501

        :return: The enrollment of this Municipality.  # noqa: E501
        :rtype: float
        """

        result = None

        value = self.enrollment
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
            result = { 'enrollment': value }

        
        return result
        

    @enrollment.setter
    def enrollment(self, enrollment):
        """Sets the enrollment of this Municipality.

        The enrollment of the Municipality  # noqa: E501

        :param enrollment: The enrollment of this Municipality.  # noqa: E501
        :type: float
        """

        self._enrollment = enrollment

    @property
    def enrollment_as_of_year(self):
        """Gets the enrollment_as_of_year of this Municipality.  # noqa: E501

        The year from which the enrollment of the Municipality was measured  # noqa: E501

        :return: The enrollment_as_of_year of this Municipality.  # noqa: E501
        :rtype: float
        """
        return self._enrollment_as_of_year
        
    @property
    def enrollment_as_of_year_dict(self):
        """Gets the enrollment_as_of_year of this Municipality.  # noqa: E501

        The year from which the enrollment of the Municipality was measured as a dictionary. Useful for Panda Dataframes.  # noqa: E501

        :return: The enrollment_as_of_year of this Municipality.  # noqa: E501
        :rtype: float
        """

        result = None

        value = self.enrollment_as_of_year
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
            result = { 'enrollment_as_of_year': value }

        
        return result
        

    @enrollment_as_of_year.setter
    def enrollment_as_of_year(self, enrollment_as_of_year):
        """Sets the enrollment_as_of_year of this Municipality.

        The year from which the enrollment of the Municipality was measured  # noqa: E501

        :param enrollment_as_of_year: The enrollment_as_of_year of this Municipality.  # noqa: E501
        :type: float
        """

        self._enrollment_as_of_year = enrollment_as_of_year

    @property
    def area_name(self):
        """Gets the area_name of this Municipality.  # noqa: E501

        The name of the area of the Municipality  # noqa: E501

        :return: The area_name of this Municipality.  # noqa: E501
        :rtype: str
        """
        return self._area_name
        
    @property
    def area_name_dict(self):
        """Gets the area_name of this Municipality.  # noqa: E501

        The name of the area of the Municipality as a dictionary. Useful for Panda Dataframes.  # noqa: E501

        :return: The area_name of this Municipality.  # noqa: E501
        :rtype: str
        """

        result = None

        value = self.area_name
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
            result = { 'area_name': value }

        
        return result
        

    @area_name.setter
    def area_name(self, area_name):
        """Sets the area_name of this Municipality.

        The name of the area of the Municipality  # noqa: E501

        :param area_name: The area_name of this Municipality.  # noqa: E501
        :type: str
        """

        self._area_name = area_name

    @property
    def area_type(self):
        """Gets the area_type of this Municipality.  # noqa: E501

        The type of area of the Municipality  # noqa: E501

        :return: The area_type of this Municipality.  # noqa: E501
        :rtype: str
        """
        return self._area_type
        
    @property
    def area_type_dict(self):
        """Gets the area_type of this Municipality.  # noqa: E501

        The type of area of the Municipality as a dictionary. Useful for Panda Dataframes.  # noqa: E501

        :return: The area_type of this Municipality.  # noqa: E501
        :rtype: str
        """

        result = None

        value = self.area_type
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
            result = { 'area_type': value }

        
        return result
        

    @area_type.setter
    def area_type(self, area_type):
        """Sets the area_type of this Municipality.

        The type of area of the Municipality  # noqa: E501

        :param area_type: The area_type of this Municipality.  # noqa: E501
        :type: str
        """

        self._area_type = area_type

    @property
    def latitude(self):
        """Gets the latitude of this Municipality.  # noqa: E501

        The latitude of the location of the Municipality  # noqa: E501

        :return: The latitude of this Municipality.  # noqa: E501
        :rtype: float
        """
        return self._latitude
        
    @property
    def latitude_dict(self):
        """Gets the latitude of this Municipality.  # noqa: E501

        The latitude of the location of the Municipality as a dictionary. Useful for Panda Dataframes.  # noqa: E501

        :return: The latitude of this Municipality.  # noqa: E501
        :rtype: float
        """

        result = None

        value = self.latitude
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
            result = { 'latitude': value }

        
        return result
        

    @latitude.setter
    def latitude(self, latitude):
        """Sets the latitude of this Municipality.

        The latitude of the location of the Municipality  # noqa: E501

        :param latitude: The latitude of this Municipality.  # noqa: E501
        :type: float
        """

        self._latitude = latitude

    @property
    def longitude(self):
        """Gets the longitude of this Municipality.  # noqa: E501

        The longitude of the location of the Municipality  # noqa: E501

        :return: The longitude of this Municipality.  # noqa: E501
        :rtype: float
        """
        return self._longitude
        
    @property
    def longitude_dict(self):
        """Gets the longitude of this Municipality.  # noqa: E501

        The longitude of the location of the Municipality as a dictionary. Useful for Panda Dataframes.  # noqa: E501

        :return: The longitude of this Municipality.  # noqa: E501
        :rtype: float
        """

        result = None

        value = self.longitude
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
            result = { 'longitude': value }

        
        return result
        

    @longitude.setter
    def longitude(self, longitude):
        """Sets the longitude of this Municipality.

        The longitude of the location of the Municipality  # noqa: E501

        :param longitude: The longitude of this Municipality.  # noqa: E501
        :type: float
        """

        self._longitude = longitude

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
        if not isinstance(other, Municipality):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
