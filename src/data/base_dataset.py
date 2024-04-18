"""
Base class for input and output data
"""

from abc import ABCMeta, abstractmethod

class BaseDataset(metaclass=ABCMeta):
    """
    What the dataset model is expect to declare:
        from_json(self, filepath): load the data from a json file as constructor

        from_yaml(self, filepath): load the data from a yaml file as constructor

        write_json(self, filepath): write the data in a json file
        
        write_yaml(self, filepath): write the data in a yaml file
    """

    def __init__(self, data_dict, data_str):
        self.data_dict = data_dict
        self.data_str  = data_str
    
    @classmethod
    @abstractmethod
    def from_json(self, filepath):
        """To be implemented by the child class."""
        raise NotImplementedError
    
    @classmethod
    @abstractmethod
    def from_yaml(self, filepath):
        """To be implemented by the child class."""
        raise NotImplementedError

    @abstractmethod
    def write_json(self, filepath):
        """To be implemented by the child class."""
        raise NotImplementedError
    
    @abstractmethod
    def write_yaml(self, filepath):
        """To be implemented by the child class."""
        raise NotImplementedError
    