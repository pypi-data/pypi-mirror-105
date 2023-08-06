# -*- coding: utf-8 -*-

"""
Paclair exceptions
"""


class PaclairException(Exception):
    """
    Error base class
    """
    pass


class ConfigurationError(PaclairException):
    """
    Error reading configuration file
    """
    pass


class ClairConnectionError(PaclairException):
    """
    Error reaching Clair
    """
    pass


class ResourceNotFoundException(PaclairException):
    """
    Resource not found
    """
    pass


class PluginNotFoundException(PaclairException):
    """
    Unknown plugin
    """
    pass


class RegistryAccessError(PaclairException):
    """
    Error reaching registry
    """
    pass
