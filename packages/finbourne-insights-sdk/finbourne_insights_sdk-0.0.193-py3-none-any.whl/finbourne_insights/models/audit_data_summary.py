# coding: utf-8

"""
    FINBOURNE Insights API

    FINBOURNE Technology  # noqa: E501

    The version of the OpenAPI document: 0.0.193
    Contact: info@finbourne.com
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

class AuditDataSummary(object):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
      required_map (dict): The key is attribute name
                           and the value is whether it is 'required' or 'optional'.
    """
    openapi_types = {
        'count': 'int',
        'categories': 'dict(str, int)'
    }

    attribute_map = {
        'count': 'count',
        'categories': 'categories'
    }

    required_map = {
        'count': 'optional',
        'categories': 'optional'
    }

    def __init__(self, count=None, categories=None):  # noqa: E501
        """
        AuditDataSummary - a model defined in OpenAPI

        :param count: 
        :type count: int
        :param categories: 
        :type categories: dict(str, int)

        """  # noqa: E501

        self._count = None
        self._categories = None
        self.discriminator = None

        if count is not None:
            self.count = count
        self.categories = categories

    @property
    def count(self):
        """Gets the count of this AuditDataSummary.  # noqa: E501


        :return: The count of this AuditDataSummary.  # noqa: E501
        :rtype: int
        """
        return self._count

    @count.setter
    def count(self, count):
        """Sets the count of this AuditDataSummary.


        :param count: The count of this AuditDataSummary.  # noqa: E501
        :type: int
        """

        self._count = count

    @property
    def categories(self):
        """Gets the categories of this AuditDataSummary.  # noqa: E501


        :return: The categories of this AuditDataSummary.  # noqa: E501
        :rtype: dict(str, int)
        """
        return self._categories

    @categories.setter
    def categories(self, categories):
        """Sets the categories of this AuditDataSummary.


        :param categories: The categories of this AuditDataSummary.  # noqa: E501
        :type: dict(str, int)
        """

        self._categories = categories

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.openapi_types):
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
        if not isinstance(other, AuditDataSummary):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
