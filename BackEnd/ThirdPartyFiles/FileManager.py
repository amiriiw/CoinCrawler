"""Cpde by amiriiw"""

import json
import logging
from typing import List, Dict, Any


class JsonFile:
    
    @staticmethod
    def save_to_json(data: Any, file_name: str) -> None:
        """Saves the data to a JSON file."""
        
        try:
            file_name = f"{file_name}.json"
            
            with open(file_name, 'w') as json_file:
                json.dump(data, json_file, indent=2)
        
        except Exception as e: 
            logging.error(f"An error occurred while write data on json file: {str(e)}", exc_info=True)
            
