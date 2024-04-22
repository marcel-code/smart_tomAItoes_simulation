import os
import time
import json
import yaml

import requests

from src.settings import DATA_PATH
from src.data.input_dataloader import InputData
from src.data.output_dataloader import OutputData

## TODO SECTION

# TODO set of parameter values to test; TODO: do more; or maybe: do dictionaries, and then access with keys
# TODO baue timestamp-net profit dictionary (and vice versa) and save both in json files
# TODO check for all input parameters whether important or not
# TODO check for all input parameters how they can be expressed. Which ways are easiest to implement?!

## MAIN SECTION

if __name__ == "__main__":
    
    # select key
    key_A = 'SmartToms-A-gl4d-1cam' # key to simulator A
    key_B = 'SmartToms-B-gl4d-1cam' # key to simulator B
    key = key_A
    if key == key_A:
        keystr = 'A'
    elif key == key_B:
        keystr = 'B'

    # select folder
    folder = 'generated_test'
    #folder = '20240423_simulator_B_generated'

    # select whether to save files
    save_file = True

    # set of parameter values to test
    endDateList = ["10-09-2023", "20-09-2023", "30-09-2023", "10-10-2023", "20-10-2023",
                   "30-10-2023", "10-11-2023", "20-11-2023", "30-11-2023", "10-12-2023"]

    # dictionary to save timestamp and net profit
    timestampNetProfitDict = {}

    # iterate over parameter values
    for i in range(len(endDateList)):

        # timestamp
        timestamp = time.strftime("%Y%m%d%H%M%S") # timestamp

        # set input data -> 39 variables
        NewInput = InputData._init()

        NewInput.data_dict['simset']['@startDate'] = "05-09-2023" # fix
        NewInput.data_dict['simset']['@endDate'] = endDateList[i]

        NewInput.data_dict['common']['CO2dosing']['@pureCO2cap'] = 100

        NewInput.data_dict['comp1']['heatingpipes']['pipe1']['@maxTemp'] = {"15-09": {"r-1": 60, "r+1": 70, "r+2": 70, "r+3": 60}, 
                                                                            "15-10": {"0": 80}}
        NewInput.data_dict['comp1']['heatingpipes']['pipe1']['@minTemp'] = {"15-09": {"0": 0}, 
                                                                            "15-10": {"r-1": 40, "r+1": 50, "s-2": 50, "s": 40}}
        NewInput.data_dict['comp1']['heatingpipes']['pipe1']['@radiationInfluence'] = "100 300"
        
        NewInput.data_dict['comp1']['screens']['scr1']['@enabled'] = True
        NewInput.data_dict['comp1']['screens']['scr1']['@material'] = "scr_Transparent"
        NewInput.data_dict['comp1']['screens']['scr1']['@closeBelow'] = "5 255; 10 50; 15.0 5; 15.2 0"
        NewInput.data_dict['comp1']['screens']['scr1']['@closeAbove'] = "450 75"
        NewInput.data_dict['comp1']['screens']['scr1']['@ToutMax'] = 18.0
        NewInput.data_dict['comp1']['screens']['scr1']['@lightPollutionPrevention'] = False

        NewInput.data_dict['comp1']['screens']['scr2']['@enabled'] = True
        NewInput.data_dict['comp1']['screens']['scr2']['@material'] = "scr_Blackout"
        NewInput.data_dict['comp1']['screens']['scr2']['@closeBelow'] = "5 10"
        NewInput.data_dict['comp1']['screens']['scr2']['@closeAbove'] = "1200 80"
        NewInput.data_dict['comp1']['screens']['scr2']['@ToutMax'] = {"01-09": 25, "19-09": 18}
        NewInput.data_dict['comp1']['screens']['scr2']['@lightPollutionPrevention'] = True
        NewInput.data_dict['comp1']['screens']['scr2']['@gapOnTempExc'] = "1 0;4 20"

        NewInput.data_dict['comp1']['illumination']['lmp1']['@enabled'] = True
        NewInput.data_dict['comp1']['illumination']['lmp1']['@type'] = "lmp_LED27" # not important
        NewInput.data_dict['comp1']['illumination']['lmp1']['@intensity'] = 150
        NewInput.data_dict['comp1']['illumination']['lmp1']['@hoursLight'] = {"05-09": 0, "07-09": 15}
        NewInput.data_dict['comp1']['illumination']['lmp1']['@endTime'] = 18
        NewInput.data_dict['comp1']['illumination']['lmp1']['@maxIglob'] = 200
        NewInput.data_dict['comp1']['illumination']['lmp1']['@maxPARsum'] = 30

        NewInput.data_dict['comp1']['setpoints']['temp']['@heatingTemp'] = {"0": "17", "2": "19", "s-1": "19", 
                                                                            "s+1": "16", "22": "16", "23": "17"}
        NewInput.data_dict['comp1']['setpoints']['temp']['@radiationInfluence'] = "100 400 2"
        NewInput.data_dict['comp1']['setpoints']['temp']['@ventOffset'] = {"01-04": {"00:00": 2}}
        NewInput.data_dict['comp1']['setpoints']['temp']['@PbandVent'] = "6 18;20 4"

        NewInput.data_dict['comp1']['setpoints']['CO2']['@setpoint'] = {"01-01": {"r+0.5": 400, "r+1": 800, "s-1.5": 800, "s": 400}}
        NewInput.data_dict['comp1']['setpoints']['CO2']['@setpIfLamps'] = {"15-09": "500",
                                                                           "25-09": "700"}
        NewInput.data_dict['comp1']['setpoints']['CO2']['@doseCapacity'] = {"01-09": "100",
                                                                            "01-10": "20 100; 40 50; 70 25"}

        NewInput.data_dict['comp1']['setpoints']['ventilation']['@winLeeMin'] = {"01-01": {"00:00": 0}}
        NewInput.data_dict['comp1']['setpoints']['ventilation']['@winLeeMax'] = {"01-01": {"00:00": 100}}
        NewInput.data_dict['comp1']['setpoints']['ventilation']['@winWndMin'] = {"01-01": {"00:00": 0}}
        NewInput.data_dict['comp1']['setpoints']['ventilation']['@winWndMax'] = {"01-01": {"00:00": 100}}
        NewInput.data_dict['comp1']['setpoints']['ventilation']['@startWnd'] = {"01-01": {"00:00": 50}}

        NewInput.data_dict['crp_dwarftomato']['cropModel']['@plantDensity'] = "1 56; 14 42; 28 30; 35 20"

        # simulate
        url = 'https://www.digigreenhouse.wur.nl/AGC2024/model/kaspro'
        response = requests.post(url, data={'key': key, 'parameters': NewInput.data_str})
        NewOutput = OutputData.from_response(response)

        # save net profit in dictionary
        timestampNetProfitDict[timestamp+'_'+str(i)] = NewOutput.data_dict['stats']['economics']['balance']

        # save input and output as JSON files
        if save_file:

            # save input
            filename_input = os.path.join(DATA_PATH, folder, timestamp+'_'+str(i)+'_simulator_'+keystr+'_input.json')
            NewInput.write_json(filename_input)

            # save output
            filename_output = os.path.join(DATA_PATH, folder, timestamp+'_'+str(i)+'_simulator_'+keystr+'_output.json')
            NewOutput.write_json(filename_output)
    
    # save dictionary with timestamps and corresponding net profit
    if save_file:
        # save with lastly used timestamp as prefix
        filename = os.path.join(DATA_PATH, folder, timestamp+'_timestamp_and_netProfit.json')
        with open(filename, 'w') as file:
            json.dump(timestampNetProfitDict, file, indent=4)
