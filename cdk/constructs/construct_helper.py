"""
Construct helper
"""

import os
import json

class ConstructHelper:
    """
    Construct Helper for constructs
    """

    def __init__(self, construct) -> None:
        self.construct = construct
        self.env = self.construct.node.try_get_context("env")

    def get_resource_name(self, resource_name: str) -> str:
        """
        Get Resource Name
        Args:
            resource_name (str): Resource Name
        Returns:
            str: Resource Name
        """
        suffix = self.get_parameter_value("SUFFIX")
        return f"{resource_name}-{suffix}"
    
    def get_parameter_value(self, param_name: str) -> str:
        """
        Get Parameter Value.
        Example: getting value of SUFFIX(param_name) from say int.json present under cdk/config
        Args:
            param_name (str): Parameter Name
        Returns:
            str: Parameter Value
        """
        root_config_path = os.path.join(os.getcwd(), "cdk", "config")
        config_data = self.read_config_data(f"{self.env}.json", root_config_path)
        param_value = config_data.get(param_name)
        
        if param_value is None:
            raise KeyError(f"Parameter {param_name} not found in {self.env}.json")
        
        return param_value


    def read_config_data(self, file_name: str, root_config_path: str = None) -> dict:
        """
        Read Stack Config Data to get lambda details
        Args:
            file_name (str): File Name
            root_config_path (str): Root Config Path
        Returns:
            dict: Config Data
        """
        if root_config_path is None:
            root_config_path = os.path.join(os.getcwd(), "cdk", "constructs", "config")
        
        config = os.path.join(root_config_path, file_name)
        with open(config, "r", encoding="utf-8") as file:
            data = file.read()
            config = json.loads(data)
        
        return config
