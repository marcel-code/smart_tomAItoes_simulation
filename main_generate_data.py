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
    #folder = '20240422_simulator_A_generated'
    #folder = '20240423_simulator_B_generated'
    #folder = '20240424_simulator_A_generated'

    # select whether to save files
    save_file = False

    # set of parameter values to test
    endDateList = ["20-09-2023", "30-09-2023", "10-10-2023", "20-10-2023", "30-10-2023", 
                   "10-11-2023", "20-11-2023", "30-11-2023", "10-12-2023", "20-12-2023", 
                   "31-12-2023"] # default is "20-11-2023", limit is "31-12-2023"
    
    pureCO2capList = [100, 200] # default is 100

    ## next 3 zipped in for-loop
    pipe1_maxTempList = [{"15-09": {"r-1": 60, "r+1": 70, "r+2": 70, "r+3": 60}, "15-10": {"0": 80}}] # default is {"15-09": {"r-1": 60, "r+1": 70, "r+2": 70, "r+3": 60}, "15-10": {"0": 80}}
    pipe1_minTempList = [{"15-09": {"0": 0}, "15-10": {"r-1": 40, "r+1": 50, "s-2": 50, "s": 40}}] # default is {"15-09": {"0": 0}, "15-10": {"r-1": 40, "r+1": 50, "s-2": 50, "s": 40}}
    pipe1_radiationInfluenceList = ["100 300"] # default is "100 300"

    ## next 3 zipped in for-loop
    src1_closeBelowList = ["5 255; 10 50; 15.0 5; 15.2 0"] # default is "5 255; 10 50; 15.0 5; 15.2 0"
    src1_closeAboveList = ["450 75"] # default is "450 75"
    src1_ToutMaxList = [18.0] # default is 18.0

    ## next 4 zipped in for-loop
    src2_closeBelowList = ["5 10"] # default is "5 10"
    src2_closeAboveList = ["1200 80"] # default is "1200 80"
    src2_ToutMaxList = [{"01-09": 25, "19-09": 18}] # default is {"01-09": 25, "19-09": 18}
    src2_gapOnTempExcList = ["1 0;4 20"] # default is "1 0;4 20"

    lmp1_intensityList = [150] # default is 150
    lmp1_hoursLightList = [{"05-09": 0, "07-09": 15}] # default is {"05-09": 0, "07-09": 15}
    lmp1_endTimeList = [18] # default is 18
    lmp1_maxIglobList = [200] # default is 200
    lmp1_maxPARsumList = [30] # default is 30

    temp_heatingTempList = [{"05-09": {"0": "17", "2": "19", "s-1": "19", "s+1": "16", "22": "16", "23": "17"}}] # default is {"05-09": {"0": "17", "2": "19", "s-1": "19", "s+1": "16", "22": "16", "23": "17"}}
    temp_radiationInfluenceList = ["100 400 2"] # default is "100 400 2"
    temp_ventOffsetList = [{"01-04": {"00:00": 2}}] # default is {"01-04": {"00:00": 2}}
    temp_PbandVentList = ["6 18;20 4"] # default is "6 18;20 4"

    CO2_setpointList = [{"01-01": {"r+0.5": 400, "r+1": 800, "s-1.5": 800, "s": 400}}] # default is {"01-01": {"r+0.5": 400, "r+1": 800, "s-1.5": 800, "s": 400}}
    CO2_setpIfLampsList = [{"15-09": "500", "25-09": "700"}] # default is {"15-09": "500", "25-09": "700"}
    CO2_doseCapacityList = [{"01-09": "100", "01-10": "20 100; 40 50; 70 25"}] # default is {"01-09": "100", "01-10": "20 100; 40 50; 70 25"}
    
    ## next 5 zipped in for-loop
    vent_winLeeMinList = [{"01-01": {"00:00": 0}}] # default is {"01-01": {"00:00": 0}}
    vent_winLeeMaxList = [{"01-01": {"00:00": 100}}] # default is {"01-01": {"00:00": 100}}
    vent_winWndMinList = [{"01-01": {"00:00": 0}}] # default is {"01-01": {"00:00": 0}}
    vent_winWndMaxList = [{"01-01": {"00:00": 100}}] # default is {"01-01": {"00:00": 100}}
    vent_startWndList = [{"01-01": {"00:00": 50}}] # default is {"01-01": {"00:00": 50}}

    plantDensityList = ["1 56; 14 42; 28 30; 35 20"] # default is "1 56; 14 42; 28 30; 35 20"

    # dictionary to save timestamp and net profit
    timestampNetProfitDict = {}

    # iterate over parameter values
    index = 0 # indexing the simulation number

    for endDate in endDateList:

        for pureCO2cap in pureCO2capList:

            for pipe1_maxTemp, pipe1_minTemp, pipe1_radiationInfluence in zip(pipe1_maxTempList, pipe1_minTempList, pipe1_radiationInfluenceList):

                for src1_closeBelow, src1_closeAbove, src1_ToutMax in zip(src1_closeBelowList, src1_closeAboveList, src1_ToutMaxList):
                                
                    for src2_closeBelow, src2_closeAbove, src2_ToutMax, src2_gapOnTempExc in zip(src2_closeBelowList, src2_closeAboveList, src2_ToutMaxList, src2_gapOnTempExcList):
                                                
                        for lmp1_intensity in lmp1_intensityList:
                            for lmp1_hoursLight in lmp1_hoursLightList:
                                for lmp1_endTime in lmp1_endTimeList:
                                    for lmp1_maxIglob in lmp1_maxIglobList:
                                        for lmp1_maxPARsum in lmp1_maxPARsumList:
                                            
                                            for temp_heatingTemp in temp_heatingTempList:
                                                for temp_radiationInfluence in temp_radiationInfluenceList:
                                                    for temp_ventOffset in temp_ventOffsetList:
                                                        
                                                        for temp_PbandVent in temp_PbandVentList:

                                                            for CO2_setpoint in CO2_setpointList:
                                                                for CO2_setpIfLamps in CO2_setpIfLampsList:
                                                                    for CO2_doseCapacity in CO2_doseCapacityList:

                                                                        for vent_winLeeMin, vent_winLeeMax, vent_winWndMin, vent_winWndMax, vent_startWnd in zip(vent_winLeeMinList, vent_winLeeMaxList, vent_winWndMinList, vent_winWndMaxList, vent_startWndList):

                                                                            for plantDensity in plantDensityList:

                                                                                # timestamp
                                                                                timestamp = time.strftime("%Y%m%d%H%M%S") # timestamp

                                                                                # set input data -> 39 variables
                                                                                NewInput = InputData._init()

                                                                                NewInput.data_dict['simset']['@startDate'] = "05-09-2023" # is fix
                                                                                NewInput.data_dict['simset']['@endDate'] = endDate

                                                                                NewInput.data_dict['common']['CO2dosing']['@pureCO2cap'] = pureCO2cap

                                                                                NewInput.data_dict['comp1']['heatingpipes']['pipe1']['@maxTemp'] = pipe1_maxTemp
                                                                                NewInput.data_dict['comp1']['heatingpipes']['pipe1']['@minTemp'] = pipe1_minTemp
                                                                                NewInput.data_dict['comp1']['heatingpipes']['pipe1']['@radiationInfluence'] = pipe1_radiationInfluence
                                                                                
                                                                                NewInput.data_dict['comp1']['screens']['scr1']['@enabled'] = True # set fix
                                                                                NewInput.data_dict['comp1']['screens']['scr1']['@material'] = "scr_Transparent" # is fix
                                                                                NewInput.data_dict['comp1']['screens']['scr1']['@closeBelow'] = src1_closeBelow
                                                                                NewInput.data_dict['comp1']['screens']['scr1']['@closeAbove'] = src1_closeAbove
                                                                                NewInput.data_dict['comp1']['screens']['scr1']['@ToutMax'] = src1_ToutMax
                                                                                NewInput.data_dict['comp1']['screens']['scr1']['@lightPollutionPrevention'] = False # set fix

                                                                                NewInput.data_dict['comp1']['screens']['scr2']['@enabled'] = True # set fix
                                                                                NewInput.data_dict['comp1']['screens']['scr2']['@material'] = "scr_Blackout" # is fix
                                                                                NewInput.data_dict['comp1']['screens']['scr2']['@closeBelow'] = src2_closeBelow
                                                                                NewInput.data_dict['comp1']['screens']['scr2']['@closeAbove'] = src2_closeAbove
                                                                                NewInput.data_dict['comp1']['screens']['scr2']['@ToutMax'] = src2_ToutMax
                                                                                NewInput.data_dict['comp1']['screens']['scr2']['@lightPollutionPrevention'] = True # set fix
                                                                                NewInput.data_dict['comp1']['screens']['scr2']['@gapOnTempExc'] = src2_gapOnTempExc

                                                                                NewInput.data_dict['comp1']['illumination']['lmp1']['@enabled'] = True # set fix
                                                                                NewInput.data_dict['comp1']['illumination']['lmp1']['@type'] = "lmp_LED27" # is fix
                                                                                NewInput.data_dict['comp1']['illumination']['lmp1']['@intensity'] = lmp1_intensity
                                                                                NewInput.data_dict['comp1']['illumination']['lmp1']['@hoursLight'] = lmp1_hoursLight
                                                                                NewInput.data_dict['comp1']['illumination']['lmp1']['@endTime'] = lmp1_endTime
                                                                                NewInput.data_dict['comp1']['illumination']['lmp1']['@maxIglob'] = lmp1_maxIglob
                                                                                NewInput.data_dict['comp1']['illumination']['lmp1']['@maxPARsum'] = lmp1_maxPARsum

                                                                                NewInput.data_dict['comp1']['setpoints']['temp']['@heatingTemp'] = temp_heatingTemp
                                                                                NewInput.data_dict['comp1']['setpoints']['temp']['@radiationInfluence'] = temp_radiationInfluence
                                                                                NewInput.data_dict['comp1']['setpoints']['temp']['@ventOffset'] = temp_ventOffset
                                                                                NewInput.data_dict['comp1']['setpoints']['temp']['@PbandVent'] = temp_PbandVent

                                                                                NewInput.data_dict['comp1']['setpoints']['CO2']['@setpoint'] = CO2_setpoint
                                                                                NewInput.data_dict['comp1']['setpoints']['CO2']['@setpIfLamps'] = CO2_setpIfLamps
                                                                                NewInput.data_dict['comp1']['setpoints']['CO2']['@doseCapacity'] = CO2_doseCapacity

                                                                                NewInput.data_dict['comp1']['setpoints']['ventilation']['@winLeeMin'] = vent_winLeeMin
                                                                                NewInput.data_dict['comp1']['setpoints']['ventilation']['@winLeeMax'] = vent_winLeeMax
                                                                                NewInput.data_dict['comp1']['setpoints']['ventilation']['@winWndMin'] = vent_winWndMin
                                                                                NewInput.data_dict['comp1']['setpoints']['ventilation']['@winWndMax'] = vent_winWndMax
                                                                                NewInput.data_dict['comp1']['setpoints']['ventilation']['@startWnd'] = vent_startWnd

                                                                                NewInput.data_dict['crp_dwarftomato']['cropModel']['@plantDensity'] = plantDensity

                                                                                """
                                                                                # simulate
                                                                                url = 'https://www.digigreenhouse.wur.nl/AGC2024/model/kaspro'
                                                                                response = requests.post(url, data={'key': key, 'parameters': NewInput.get_data_str()})
                                                                                NewOutput = OutputData.from_response(response)

                                                                                # save net profit in dictionary
                                                                                timestampNetProfitDict[timestamp+'_'+str(index)] = NewOutput.data_dict['stats']['economics']['balance']

                                                                                # save input and output as JSON files
                                                                                if save_file:

                                                                                    # save input
                                                                                    filename_input = os.path.join(DATA_PATH, folder, timestamp+'_'+str(index)+'_simulator_'+keystr+'_input.json')
                                                                                    NewInput.write_json(filename_input)

                                                                                    # save output
                                                                                    filename_output = os.path.join(DATA_PATH, folder, timestamp+'_'+str(index)+'_simulator_'+keystr+'_output.json')
                                                                                    NewOutput.write_json(filename_output)
                                                                                """

                                                                                # update index
                                                                                index += 1
    
    print("Number of simulations:", index)
    
    # save dictionary with timestamps and corresponding net profit
    if save_file:
        # save with lastly used timestamp as prefix
        filename = os.path.join(DATA_PATH, folder, timestamp+'_timestamp_and_netProfit.json')
        with open(filename, 'w') as file:
            json.dump(timestampNetProfitDict, file, indent=4)
