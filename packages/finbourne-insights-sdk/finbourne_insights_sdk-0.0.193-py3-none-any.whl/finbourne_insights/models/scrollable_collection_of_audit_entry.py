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

class ScrollableCollectionOfAuditEntry(object):
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
        'data': 'list[AuditEntry]',
        'state': 'str'
    }

    attribute_map = {
        'data': 'data',
        'state': 'state'
    }

    required_map = {
        'data': 'optional',
        'state': 'optional'
    }

    def __init__(self, data=None, state=None):  # noqa: E501
        """
        ScrollableCollectionOfAuditEntry - a model defined in OpenAPI

        :param data: 
        :type data: list[finbourne_insights.AuditEntry]
        :param state: 
        :type state: str

        """  # noqa: E501

        self._data = None
        self._state = None
        self.discriminator = None

        self.data = data
        self.state = state

    @property
    def data(self):
        """Gets the data of this ScrollableCollectionOfAuditEntry.  # noqa: E501


        :return: The data of this ScrollableCollectionOfAuditEntry.  # noqa: E501
        :rtype: list[AuditEntry]
        """
        return self._data

    @data.setter
    def data(self, data):
        """Sets the data of this ScrollableCollectionOfAuditEntry.


        :param data: The data of this ScrollableCollectionOfAuditEntry.  # noqa: E501
        :type: list[AuditEntry]
        """

        self._data = data

    @property
    def state(self):
        """Gets the state of this ScrollableCollectionOfAuditEntry.  # noqa: E501


        :return: The state of this ScrollableCollectionOfAuditEntry.  # noqa: E501
        :rtype: str
        """
        return self._state

    @state.setter
    def state(self, state):
        """Sets the state of this ScrollableCollectionOfAuditEntry.


        :param state: The state of this ScrollableCollectionOfAuditEntry.  # noqa: E501
        :type: str
        """

        self._state = state

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
        if not isinstance(other, ScrollableCollectionOfAuditEntry):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
