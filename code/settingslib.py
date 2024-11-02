# region import
import json
import re
import os
from colorama import Fore, Back, Style
# endregion

# settings class
class Settings:
    # region init
    def __init__(self, path:str, warnings:bool=True):
        # initialize variables
        self.__path_set     = False
        self.__alt_path_set = False
        self.path           = ''
        self.alt_path       = ''
        self.raw_settings   = ''
        
        self.warnings = warnings
        
        # load settings
        self.set_path(path)
        self.load_settings()
    # endregion init
    
    # region depen
    def __col(self, color:str|list):
        if isinstance(color, str):
            print(f'{color}', end='')
        elif isinstance(color, list):
            for c in color:
                self.__col(c)
        
    def __print_col(self, color:str|list, text:str, is_warning:bool=False):
        if is_warning:
            self.__col([Fore.BLACK, Back.BLACK])
            print(f'TO DISABLE WARNINGS INITIALIZE SETTINGS WITH "warnings=True"')
            
        self.__col(color)
        print(text, end='')
        print('')
        self.__col(Style.RESET_ALL)
    
    # endregion depen

    # region reloading functions
    # function to set the global path
    def set_path(self, path:str):
        # checks
        assert os.path.isfile(path) # check if file exists
        assert path.endswith('.json') # check if file is .json
        
        # try to find alt settings file
        alt_path = re.split(r'[\\/(//)]', path)
        alt_path[-1] = alt_path[-1]
        alt_path[-1] = 'alt__' + alt_path[-1]
        alt_path = '/'.join(alt_path)
        
        if os.path.isfile(alt_path): # check if the alt_path is valid
            self.alt_path = alt_path
            self.__alt_path_set = True
        elif self.warnings:
            self.__print_col(Fore.YELLOW, "Alternative Path for Type hints not found. Continuing anyway.", True)
                
        # set variables
        self.path = path
        self.__path_set = True
    
    # function to load settings
    def load_settings(self, path:str=None):
        if not path: # check if a custom path was defined
            path = self.path
        raw_settings = json.load(open(path, 'r', encoding='utf-8')) # load raw data into variable
        assert isinstance(raw_settings, dict)
        self.raw_settings = raw_settings
        
    def save_settings(self, path:str=None):
        if not path:
            path = self.path
            
        json.dump(self.__dir__(), open(path, 'w'))
        
    # endregion reloading functions
        
    # region settings functions
    # function to easily get settings via ['x']
    def __dir__(self):
        # returns the setting
        return self.raw_settings
    
    def __call__(self, keys:str):
        return self.get(keys)
    
    def get(self, keys:str) -> any:
        keys = keys.split('.')
        nested = self.__dir__()
        
        for key in keys:
            try:
                if key.isnumeric():
                    nested = nested[int(key)]
                else:
                    nested = nested[key]
            except KeyError as error:
                print(f'Error finding {key} for {'.'.join(keys)}')
                print({error})
                raise error
            except IndexError as error:
                print(f'Error finding {key} for {'.'.join(keys)}')
                print({error})
                raise error
                
        return nested
    
    # endregion settings functions
