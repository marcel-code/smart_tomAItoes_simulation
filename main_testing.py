import json
import os
import yaml
import xlrd
import time
from datetime import datetime, timedelta
from pathlib import Path

import matplotlib.pyplot as plt
import requests

from src.settings import root, TESTING_PATH, DATA_PATH
from src.data.input_dataloader import InputData
from src.data.output_dataloader import OutputData

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

    # select task
    initial_example_and_data_handling = False
    extract_net_profits_to_dictionary = False
    extract_simulation_duration_to_dictionary = False
    plot_net_profits_over_simulation_duration = False
    build_datetime_strings_list = False

    if initial_example_and_data_handling:

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

        #NewResponse = OutputData.from_response(response)
        #filename = os.path.join(TESTING_PATH, 'initial_example', 'example_response.json')
        #NewResponse = OutputData.from_json(filename)
        #filename = os.path.join(TESTING_PATH, 'initial_example', 'example_response.yaml')
        #NewResponse = OutputData.from_yaml(filename)
        #print(11,filename)
        #print(NewResponse.data_dict)
        

        #filename = os.path.join(TESTING_PATH, 'initial_example', 'example_response_write.json')
        #NewResponse.write_json(filename)
        #filename = os.path.join(TESTING_PATH, 'initial_example', 'example_response_write.yaml')
        #NewResponse.write_yaml(filename)
        
        ##############################################

        # Test input_dataloader

        #filename = os.path.join(TESTING_PATH, 'initial_example', 'example_input.json')
        #NewInput = InputData.from_json(filename)
        #filename = os.path.join(TESTING_PATH, 'initial_example', 'example_input.yaml')
        #NewInput = InputData.from_yaml(filename)
        #print(NewInput.data_dict)
        #print(type(NewInput.data_dict["comp1"]["screens"]["scr1"]["@enabled"]))

        #filename = os.path.join(TESTING_PATH, 'initial_example', 'example_input_write.json')
        #NewInput.write_json(filename)
        #filename = os.path.join(TESTING_PATH, 'initial_example', 'example_input_write.yaml')
        #NewInput.write_yaml(filename)

        ##############################################
    
    if extract_net_profits_to_dictionary:
        
        # define used folder
        #folder = '20240422_simulator_A_generated'
        #folder = '20240423_simulator_B_generated'
        #folder = '20240424_simulator_A_generated'
        folder = '20240426_simulator_A_generated'

        # select replace string
        if '_A_' in folder:
            replace_str = '_simulator_A_output'      
        elif '_B_' in folder:
            replace_str = '_simulator_B_output'

        # initialize dictionary place holder
        timestampNetProfitDict = {}

        # list of all filenames in folder
        folder_path = os.path.join(DATA_PATH, folder)
        filenames = os.listdir(folder_path)

        # list of all filenames of output files in folder
        output_files = [filename for filename in filenames if 'output' in filename]

        for output_file in output_files:
            
            # extray dictionary key from filename
            output_file_key = output_file.replace(replace_str, '')
            output_file_key_final = output_file_key.replace('.json', '')

            # read output json
            output_filename = os.path.join(DATA_PATH, folder, output_file)
            NewOutput = OutputData.from_json(output_filename)

            # save net profit to dictionary
            timestampNetProfitDict[output_file_key_final] = NewOutput.data_dict['stats']['economics']['balance']

        # finalize filename
        output_file_key_final = output_file_key_final.split('_')[0]

        # save dictionary as json
        filename = os.path.join(DATA_PATH, folder, output_file_key_final+'_timestamp_and_netProfit.json')
        with open(filename, 'w') as file:
            json.dump(timestampNetProfitDict, file, indent=4)
            
    if extract_simulation_duration_to_dictionary:
        
        # define used folder
        #folder = '20240422_simulator_A_generated'
        #folder = '20240423_simulator_B_generated'
        #folder = '20240424_simulator_A_generated'
        folder = '20240426_simulator_A_generated'

        # select replace string
        if '_A_' in folder:
            replace_str = '_simulator_A_output'      
        elif '_B_' in folder:
            replace_str = '_simulator_B_output'

        # initialize dictionary place holder
        timestampSimulationDurationDict = {}

        # list of all filenames in folder
        folder_path = os.path.join(DATA_PATH, folder)
        filenames = os.listdir(folder_path)

        # list of all filenames of output files in folder
        output_files = [filename for filename in filenames if 'output' in filename]

        for output_file in output_files:
            
            # extray dictionary key from filename
            output_file_key = output_file.replace(replace_str, '')
            output_file_key_final = output_file_key.replace('.json', '')

            # read output json
            output_filename = os.path.join(DATA_PATH, folder, output_file)
            NewOutput = OutputData.from_json(output_filename)

            # extract start and end date from output            
            start_excel_datestamp = NewOutput.data_dict['data']['DateTime']['data'][0]
            end_excel_datestamp = NewOutput.data_dict['data']['DateTime']['data'][-1]

            # convert excel datestamp to datetime
            start_datetime = xlrd.xldate.xldate_as_datetime(start_excel_datestamp, 0)
            end_datetime = xlrd.xldate.xldate_as_datetime(end_excel_datestamp, 0)

            # calculate simulation duration in days
            simulation_duration = (end_datetime-start_datetime).days

            # save net profit to dictionary
            timestampSimulationDurationDict[output_file_key_final] = simulation_duration

        # finalize filename
        output_file_key_final = output_file_key_final.split('_')[0]

        # save dictionary as json
        filename = os.path.join(DATA_PATH, folder, output_file_key_final+'_timestamp_and_simulationDuration.json')
        with open(filename, 'w') as file:
            json.dump(timestampSimulationDurationDict, file, indent=4)
            
    if plot_net_profits_over_simulation_duration:
        
        # all investigated folders
        folders = ['20240422_simulator_A_generated', 
                   '20240423_simulator_B_generated', 
                   '20240424_simulator_A_generated',
                   '20240426_simulator_A_generated']
        
        # initialize data dictionary
        dataDict = {}

        # for all folders
        for folder in folders:

            # list of all filenames in folder
            folder_path = os.path.join(DATA_PATH, folder)
            filenames = os.listdir(folder_path)

            # filename of json file with net profits and simulation durations
            timestamp_and_netProfit_filename = [filename for filename in filenames if 'timestamp_and_netProfit' in filename][0]
            timestamp_and_simulationDuration_filename = [filename for filename in filenames if 'timestamp_and_simulationDuration' in filename][0]

            # read dictionary from json with net profits
            filename = os.path.join(DATA_PATH, folder, timestamp_and_netProfit_filename)
            with open(filename, 'r') as file:
                timestampNetProfitDict = json.load(file)
            # read dictionary from json with simulation durations
            filename = os.path.join(DATA_PATH, folder, timestamp_and_simulationDuration_filename)
            with open(filename, 'r') as file:
                timestampSimulationDurationDict = json.load(file)

            # save data in dictionary
            dataDict[folder] = [timestampSimulationDurationDict.values(), timestampNetProfitDict.values()]

        # plot net profits over simulation duration
        shape = ['o', '+', '.', 'x']
        idx = 0
        for folder in folders:
            # plot net profits over simulation duration
            plt.plot(dataDict[folder][0], dataDict[folder][1], shape[idx], label=folder)
            idx += 1
        plt.legend()
        plt.xlabel('Simulation duration [days]')
        plt.ylabel('Net profit [€]')
        plt.show()

    if build_datetime_strings_list:

        # Startdatum
        start_date = datetime(2023, 10, 25)

        # Enddatum
        end_date = datetime(2023, 12, 14)

        # Liste für die Datums-Strings
        date_list = []

        # Schleife durch alle Tage zwischen Start- und Enddatum
        current_date = start_date
        while current_date <= end_date:
            # Formatieren des Datums im gewünschten Format und Hinzufügen zur Liste
            date_str = current_date.strftime("%d-%m-%Y")
            date_list.append(date_str)
            
            # Nächster Tag
            current_date += timedelta(days=1)

        # Ausgabe der Liste
        print(date_list)

        start_date = "05-09-2023"
        end_date = (datetime.strptime(start_date, "%d-%m-%Y") + timedelta(days=70)).strftime("%d-%m-%Y")

        print(end_date)
