import abc

class IGeocode(object):
    __metaclass__  = abc.ABCMeta

    @abc.abstractmethod
    def coder(self, location):
        """Method that should do something."""

class IGeocodeReverse(object):
    __metaclass__  = abc.ABCMeta

    @abc.abstractmethod
    def coder_reverse(self, location):
        """Method that should do something."""
