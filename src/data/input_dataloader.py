import json
import yaml

from .base_dataset import BaseDataset

class InputData(BaseDataset):
    """
    Class for input data
    """

    data_dict = {
        "simset": {
            "@startDate": "05-09-2023",
            "@endDate": "06-09-2023"
        },
        "common": {
            "CO2dosing": {
                "@pureCO2cap": 100
            }
        },
        "comp1": {
            "heatingpipes": {
                "pipe1": {
                    "@maxTemp": {
                        "15-09": {"r-1": 60, "r+1": 70, "r+2": 70, "r+3": 60},
                        "15-10": {"0": 80}
                    },
                    "@minTemp": {
                        "15-09": {"0": 0}, 
                        "15-10": {"r-1": 40, "r+1": 50, "s-2": 50, "s": 40}
                    },
                    "@radiationInfluence": "100 300"
                }
            },
            "screens": {
                "scr1": {
                    "@enabled": True,
                    "@material": "scr_Transparent",
                    "@closeBelow": "5 255; 10 50; 15.0 5; 15.2 0",
                    "@closeAbove": "450 75",
                    "@ToutMax": 18.0,
                    "@lightPollutionPrevention": False
                },
                "scr2": {
                    "@enabled": True,
                    "@material": "scr_Blackout",
                    "@closeBelow": "5 10",
                    "@closeAbove": "1200 80",
                    "@ToutMax": {"01-09": 25,"19-09": 18},
                    "@lightPollutionPrevention": True,
                    "@gapOnTempExc": "1 0;4 20"
                }
            },
            "illumination": {
                "lmp1": {
                    "@enabled": True,
                    "@type": "lmp_LED27",
                    "@intensity": 150,
                    "@hoursLight": {"05-09": 0, "07-09": 15},
                    "@endTime": 18,
                    "@maxIglob": 200,
                    "@maxPARsum": 30
                }
            },
            "setpoints": {
                "temp": {
                "@heatingTemp": {
                "05-09": {
                    "0": "17", "2": "19", "s-1": "19", 
                    "s+1": "16", "22": "16", "23": "17"}
                    },
                    "@radiationInfluence": "100 400 2",
                    "@ventOffset": {
                    "01-04": {"00:00": 2}
                    },
                    "@PbandVent": "6 18;20 4"
                },
                "CO2": {
                    "@setpoint": {
                    "01-01": {"r+0.5": 400, "r+1": 800, "s-1.5": 800, "s": 400}
                    },
                    "@setpIfLamps": {
                    "15-09": "500",
                    "25-09": "700"
                    },
                    "@doseCapacity": {
                    "01-09": "100",
                    "01-10": "20 100; 40 50; 70 25"
                    }
                },
                "ventilation": {
                    "@winLeeMin": {
                    "01-01": {"00:00": 0}
                    },
                    "@winLeeMax": {
                    "01-01": {"00:00": 100}
                    },
                    "@winWndMin": {
                    "01-01": {"00:00": 0}
                    },
                    "@winWndMax": {
                    "01-01": {"00:00": 100}
                    },
                    "@startWnd": {
                    "01-01": {"00:00": 50}
                    }
                }
            }
        },
        "crp_dwarftomato": {
            "cropModel": {
                "@plantDensity": "1 56; 14 42; 28 30; 35 20"
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
