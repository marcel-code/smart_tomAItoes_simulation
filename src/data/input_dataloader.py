import json
import yaml

from .base_dataset import BaseDataset

class InputData(BaseDataset):
    """
    Class for input data
    """

    data_dict = {
        "simset": {
            "@startDate": "05-09-2023",     # simulation start date
            "@endDate": "06-09-2023"        # simulation end date
        },
        "common": {
            "CO2dosing": {
                "@pureCO2cap": 100          # maximum CO2-capacity in kg/(ha h)
            }
        },
        "comp1": {
            "heatingpipes": {
                "pipe1": {
                    "@maxTemp": {   # maximum applied heating pipe temperature (can also be changed during the year and over the day)
                        "15-09": {"r-1": 60, "r+1": 70, "r+2": 70, "r+3": 60},
                        "15-10": {"0": 80}
                    },
                    "@minTemp": {   # minimum applied heating pipe temperature (can also be changed during the year and over the day)
                        "15-09": {"0": 0}, 
                        "15-10": {"r-1": 40, "r+1": 50, "s-2": 50, "s": 40}
                    },
                    "@radiationInfluence": "100 300"    # parameters to define the table-like influence of solar radiation on the (minimum pipe) temperature (deactivated with "0")
                }
            },
            "screens": {
                "scr1": {
                    "@enabled": True,                   # enable/disable screen
                    "@material": "scr_Transparent",     # screen type
                    "@closeBelow": "5 255; 10 50; 15.0 5; 15.2 0",  # deploys the screen when the outside radiation is below a certain level, so controls the behaviour at dawn, early morning, and night
                    "@closeAbove": "450 75",            # controls the screen when the radiation exceeds a certain value, so is meant to be used when using screens for shading
                    "@ToutMax": 18.0,                   # tells above what outside temperature the screen is not used
                    "@lightPollutionPrevention": False  # tells that the controller should always close this screen when lights are on during night-time
                },
                "scr2": {
                    "@enabled": True,                   # enable/disable screen
                    "@material": "scr_Blackout",        # screen type
                    "@closeBelow": "5 10",              # deploys the screen when the outside radiation is below a certain level, so controls the behaviour at dawn, early morning, and night
                    "@closeAbove": "1200 80",           # controls the screen when the radiation exceeds a certain value, so is meant to be used when using screens for shading
                    "@ToutMax": {"01-09": 25,"19-09": 18},  # tells above what outside temperature the screen is not used
                    "@lightPollutionPrevention": True,  # tells that the controller should always close this screen when lights are on during night-time
                    "@gapOnTempExc": "1 0;4 20"         # screen gap as a function of air temperature excess compared to heating setpoint
                }
            },
            "illumination": {
                "lmp1": {
                    "@enabled": True,       # enable/disable lamps
                    "@type": "lmp_LED27",   # lamp type
                    "@intensity": 150,      # define the amount of PAR light provided by the lamps in µmol/(m² s)
                    "@hoursLight": {        # defines the maximum number of daily running hours of the lamps
                        "05-09": 0, 
                        "07-09": 15
                    }, 
                    "@endTime": 18,         # defines at which time the lamps are switched off every day
                    "@maxIglob": 200,       # criterion for the outside radiation above which the lamps are switched off
                    "@maxPARsum": 30        # criterion for the light intensity just above crop above which the lamps are switched off (this can prevent lamps switching on in the afternoon after a sunny day; this can be switched off by providing a high value)
                }
            },
            "setpoints": {
                "temp": {
                    "@heatingTemp": {       # heating setpoints given as structure that represents a time-value combination
                        "05-09": {
                            "0": "17", "2": "19", "s-1": "19", 
                            "s+1": "16", "22": "16", "23": "17"
                        }
                    },
                    "@radiationInfluence": "100 400 2",     # parameters to define the table-like influence of solar radiation on the (minimum pipe) temperature (deactivated with "0")
                    "@ventOffset": {        # ventilation line is defined as an offset relative to the heating setpoint (limited by 2 °C/h)
                        "01-04": {"00:00": 2}
                    },
                    "@PbandVent": "6 18;20 4"   # P-band for the ventilation control of the leeward vent opening (often: set proportional band depending on outside temperature)
                },
                "CO2": {
                    "@setpoint": {          # CO2 dosing setpoints (expressed in ppm)
                        "01-01": {"r+0.5": 400, "r+1": 800, "s-1.5": 800, "s": 400}
                    },
                    "@setpIfLamps": {       # setpoint for CO2 can be overruled by a setpoint when the lamps are on (expressed in ppm)
                        "15-09": "500",
                        "25-09": "700"
                    },
                    "@doseCapacity": {      # adjust the maximum CO2 dosing rate
                        "01-09": "100",
                        "01-10": "20 100; 40 50; 70 25"
                    }
                },
                "ventilation": {
                    "@winLeeMin": {     # limitation for minimum vent/window-opening on lee side (can also be "abused" with direct passing of setpoints)
                        "01-01": {"00:00": 0}
                    },
                    "@winLeeMax": {     # limitation for maximal vent/window-opening on lee side (can also be "abused" with direct passing of setpoints)
                        "01-01": {"00:00": 100}
                    },
                    "@winWndMin": {     # limitation for minimum vent/window-opening on wind side (can also be "abused" with direct passing of setpoints)
                        "01-01": {"00:00": 0}
                    },
                    "@winWndMax": {     # limitation for maximum vent/window-opening on wind side (can also be "abused" with direct passing of setpoints)
                        "01-01": {"00:00": 100}
                    },
                    "@startWnd": {      # starting also opening the windward vent opening (use the windward side vents only after the vents on the leeward side are opened above a certain extent)
                        "01-01": {"00:00": 50}
                    }
                }
            }
        },
        "crp_dwarftomato": {
            "cropModel": {
                "@plantDensity": "1 56; 14 42; 28 30; 35 20"    # set plant-density information to the crop-simulation-model
            }
        }
    }

    data_str = json.dumps(data_dict)
    
    @classmethod
    def from_json(cls, filepath):
        """
            Load data from a JSON file.
        """
        with open(filepath, 'r') as file:
            data_str = file.read()
        return cls(json.loads(data_str), 
                   data_str)

    @classmethod
    def from_yaml(cls, filepath):
        """
            Load data from a yaml file.
        """
        data_dict = yaml.safe_load(filepath)
        return cls(data_dict, 
                   json.dumps(data_dict))
    
    def write_json(self, filepath):
        """
            Write data in a JSON file.
        """
        with open(filepath, 'w') as file:
            json.dump(self.data_dict, file)
    
    def write_yaml(self, filepath):
        """
            Write data in a yaml file.
        """
        with open(filepath, 'w') as file:
            yaml.dump(self.data_dict, file, default_flow_style=False)
