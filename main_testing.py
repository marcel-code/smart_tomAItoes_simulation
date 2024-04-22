import json
import os
import yaml
import time
from pathlib import Path

import requests

from src.settings import root, TESTING_PATH, DATA_PATH
from src.data.input_dataloader import InputData
from src.data.output_dataloader import OutputData

## TODO SECTION

# TODO find a good simulaiton duration / end date

## MAIN SECTION

def print_all_keys(dictionary, parent_keys=[]):
    for key, value in dictionary.items():
        current_keys = parent_keys + [key]
        if isinstance(value, dict):
            print_all_keys(value, current_keys)
        else:
            print(".".join(current_keys))

if __name__ == "__main__":

    # Test interaction with simulator

    # select key
    key_A = 'SmartToms-A-gl4d-1cam' # key to simulator A
    key_B = 'SmartToms-B-gl4d-1cam' # key to simulator B
    key = key_A

    # select example
    initial_example = True

    if initial_example:

        # read input json
        # param string = input string
        param_path = os.path.join(TESTING_PATH, 'initial_example', 'example_input.json')
        #print(type(param_path))
        with open(param_path, 'r') as file:
            param_string = file.read()     # read as string
            param_dict = json.loads(param_string) # read as dictionary

        # simulator
        url = 'https://www.digigreenhouse.wur.nl/AGC2024/model/kaspro'
        response = requests.post(url, data={'key': key, 'parameters': param_string})
        # extract data
        response_text = response.text
        response_dict = response.json()
        
        #print(json.loads(response.text))

        # print out the response
        #print("Response:", response)
        #print("Response json:", response.json())
        
        # Write the response json to a file
        response_path = os.path.join(TESTING_PATH, 'initial_example', 'example_response.json')
        with open(response_path, 'w') as file:
            json.dump(response.json(), file)
        
        # PRINTS

        # input
        #print_all_keys(param_dict)

        # output
        response_dict = response.json()
        #print(response_dict.keys())
        #print_all_keys(response_dict)
        #print(type(response_dict['stats']['economics']['balance']))
        
        ##############################################

        # Test output_dataloader

        NewResponse = OutputData.from_response(response)
        filename = os.path.join(TESTING_PATH, 'initial_example', 'example_response.json')
        NewResponse = OutputData.from_json(filename)
        filename = os.path.join(TESTING_PATH, 'initial_example', 'example_response.yaml')
        NewResponse = OutputData.from_yaml(filename)
        print(11,filename)
        print(NewResponse.data_dict)
        

        filename = os.path.join(TESTING_PATH, 'initial_example', 'example_response_write.json')
        NewResponse.write_json(filename)
        filename = os.path.join(TESTING_PATH, 'initial_example', 'example_response_write.yaml')
        NewResponse.write_yaml(filename)
        
        ##############################################

        # Test input_dataloader

        filename = os.path.join(TESTING_PATH, 'initial_example', 'example_input.json')
        NewInput = InputData.from_json(filename)
        filename = os.path.join(TESTING_PATH, 'initial_example', 'example_input.yaml')
        NewInput = InputData.from_yaml(filename)
        print(NewInput.data_dict)
        #print(type(NewInput.data_dict["comp1"]["screens"]["scr1"]["@enabled"]))

        filename = os.path.join(TESTING_PATH, 'initial_example', 'example_input_write.json')
        NewInput.write_json(filename)
        filename = os.path.join(TESTING_PATH, 'initial_example', 'example_input_write.yaml')
        NewInput.write_yaml(filename)

        ##############################################
