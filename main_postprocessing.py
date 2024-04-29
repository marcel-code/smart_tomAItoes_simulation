import argparse
import copy
import json
import os
import yaml
import time
from datetime import datetime
from pathlib import Path

import matplotlib.pyplot as plt
import requests

from src.settings import root, TESTING_PATH, DATA_PATH
from src.data.input_dataloader import InputData
from src.data.output_dataloader import OutputData

## METHODS SECTION

def method_1():
    pass

## MAIN SECTION

if __name__ == "__main__":

    # define used folder
    #folder = '20240422_simulator_A_generated'
    #folder = '20240423_simulator_B_generated'
    #folder = '20240424_simulator_A_generated'
    folder = '20240426_simulator_A_generated'

    # list of all filenames in folder
    folder_path = os.path.join(DATA_PATH, folder)
    filenames = os.listdir(folder_path)

    # list of all filenames of output files in folder
    output_files = [filename for filename in filenames if 'output' in filename]

    for output_file in output_files:

        # read output json
        output_filename = os.path.join(DATA_PATH, folder, output_file)
        NewOutput = OutputData.from_json(output_filename)

        startDate = NewOutput.data_dict['data']['DateTime']['data'][0] # in excel format
        endDate = NewOutput.data_dict['data']['DateTime']['data'][-1] # in excel format

        greenhouse_air_temperature = NewOutput.data_dict['data']['comp1.Air.T']['data'] # in °C
        greenhouse_air_humidity = NewOutput.data_dict['data']['comp1.Air.RH']['data'] # in %
        greenhouse_CO2_conc = NewOutput.data_dict['data']['comp1.Air.ppm']['data'] # in ppm

        outside_solar_radiation = NewOutput.data_dict['data']['common.Iglob.Value']['data'] # in W/m^2
        outside_temperature = NewOutput.data_dict['data']['common.Tout.Value']['data'] # in °C
        outside_humidity = NewOutput.data_dict['data']['common.RHout.Value']['data'] # in %
        outside_wind_speed = NewOutput.data_dict['data']['common.Windsp.Value']['data'] # in m/s

        light_intensity_above_crop = NewOutput.data_dict['data']['comp1.PARsensor.Above']['data'] # in µmol/m^2/s
        avg_heat_pipe_temperature = NewOutput.data_dict['data']['comp1.TPipe1.Value']['data'] # in °C
        supply_heat_pipe_temperature = NewOutput.data_dict['data']['comp1.ConPipes.TSupPipe1']['data'] # in °C
        heating_power = NewOutput.data_dict['data']['comp1.PConPipe1.Value']['data'] # in W/m^2
        lee_side_window_opening = NewOutput.data_dict['data']['comp1.ConWin.WinLee']['data'] # in %
        wind_side_window_opening = NewOutput.data_dict['data']['comp1.ConWin.WinWnd']['data'] # in %
        heating_setpoint = NewOutput.data_dict['data']['comp1.Setpoints.SpHeat']['data'] # in °C
        ventilation_setpoint = NewOutput.data_dict['data']['comp1.Setpoints.SpVent']['data'] # in °C
        screen_1_position = NewOutput.data_dict['data']['comp1.Scr1.Pos']['data']  # in 0-1
        screen_2_position = NewOutput.data_dict['data']['comp1.Scr2.Pos']['data'] # in 0-1
        lamp_electricity_consumption = NewOutput.data_dict['data']['comp1.Lmp1.ElecUse']['data'] # in W/m^2
        co2_dosing_rate = NewOutput.data_dict['data']['comp1.McPureAir.Value']['data'] # in kg/(m² s)
        co2_dosing_setpoint = NewOutput.data_dict['data']['comp1.Setpoints.SpCO2']['data'] # in ppm

        fruit_freshweight = NewOutput.data_dict['data']['comp1.Growth.FruitFreshweight']['data'] # in gram/plant
        dvs_fruit = NewOutput.data_dict['data']['comp1.Growth.DVSfruit']['data'] # in 0-1
        dry_matter_fraction = NewOutput.data_dict['data']['comp1.Growth.DryMatterFract']['data'] # in 0-1
        crop_absorption = NewOutput.data_dict['data']['comp1.Growth.CropAbs']['data'] # in 0-1
        plant_density = NewOutput.data_dict['data']['comp1.Growth.PlantDensity']['data'] # in plants/m^2

        peak_hour = NewOutput.data_dict['data']['common.ElecPrice.PeakHour']['data'] # boolean

        fractionOfYear = NewOutput.data_dict['stats']['economics']['info']['fractionOfYear'] # in 0-1
        averageDensity = NewOutput.data_dict['stats']['economics']['info']['averageDensity'] # in plants/m^2

        fixedCosts_greenhouse = NewOutput.data_dict['stats']['economics']['fixedCosts']['objects']['comp1.Greenhouse'] # in €/m^2
        fixedCosts_lamp_1 = NewOutput.data_dict['stats']['economics']['fixedCosts']['objects']['comp1.Lmp1'] # in €/m^2
        fixedCosts_screen_1 = NewOutput.data_dict['stats']['economics']['fixedCosts']['objects']['comp1.Scr1'] # in €/m^2
        fixedCosts_screen_2 = NewOutput.data_dict['stats']['economics']['fixedCosts']['objects']['comp1.Scr2'] # in €/m^2
        fixedCosts_ConCO2 = NewOutput.data_dict['stats']['economics']['fixedCosts']['objects']['comp1.ConCO2'] # in €/m^2
        fixedCosts_spacingSystem = NewOutput.data_dict['stats']['economics']['fixedCosts']['objects']['spacingSystem'] # in €/m^2
        fixedCosts_total = NewOutput.data_dict['stats']['economics']['fixedCosts']['total'] # in €/m^2

        variableCosts_gas = NewOutput.data_dict['stats']['economics']['variableCosts']['objects']['gas'] # in €/m^2
        variableCosts_elec = NewOutput.data_dict['stats']['economics']['variableCosts']['objects']['elec'] # in €/m^2
        variableCosts_CO2 = NewOutput.data_dict['stats']['economics']['variableCosts']['objects']['CO2'] # in €/m^2
        variableCosts_plants = NewOutput.data_dict['stats']['economics']['variableCosts']['objects']['plants'] # in €/m^2
        variableCosts_total = NewOutput.data_dict['stats']['economics']['variableCosts']['total'] # in €/m^2

        gains_product = NewOutput.data_dict['stats']['economics']['gains']['objects']['product'] # in €/m^2
        gains_total = NewOutput.data_dict['stats']['economics']['gains']['total'] # in €/m^2

        net_profit = NewOutput.data_dict['stats']['economics']['balance'] # in €/m^2
