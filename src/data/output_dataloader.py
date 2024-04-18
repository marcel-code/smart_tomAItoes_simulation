import json
import yaml

from .base_dataset import BaseDataset

class OutputData(BaseDataset):
    """
    Class for output data
    """

    data_dict = {
        "responsecode": 0,
        "responsemsg": "ok",
        "data": {
            "DateTime": {
                "unit": "OLE Automation date",
                "data": [45174.041667, 45174.083333]
            }, 
            "comp1.Air.T": {
                "unit": "oC", "data": [18.0, 19.28 ]
            }, 
            "comp1.Air.RH": {
                "unit": "%", 
                "data": [72.1, 68.7]
            }, 
            "comp1.Air.ppm": {
                "unit": "ppm", 
                "data": [400.0, 400.0]
            }, 
            "common.Iglob.Value": {
                "unit": "W/m2", 
                "data": [0.0, 0.0]
            }, 
            "common.Tout.Value": {
                "unit": "oC", 
                "data": [16.8, 16.4]
            }, 
            "common.RHout.Value": {
                "unit": "%", 
                "data": [86.4, 87.3]
            }, 
            "common.Windsp.Value": {
                "unit": "m/s", 
                "data": [0.8, 1.3]
            }, 
            "comp1.PARsensor.Above": {
                "unit": "umol/m2/s", 
                "data": [0.0, 0.0]
            }, 
            "comp1.TPipe1.Value": {
                "unit": "oC", 
                "data": [43.393038625547376, 37.263411730190654,]
            }, 
            "comp1.ConPipes.TSupPipe1": {
                "unit": "oC", 
                "data": [47.5, 38.5]
            }, 
            "comp1.PConPipe1.Value": {
                "unit": "W/m2", 
                "data": [108.3, 27.2]
            }, 
            "comp1.ConWin.WinLee": {
                "unit": "%", 
                "data": [0.0, 0.0]
            }, 
            "comp1.ConWin.WinWnd": {
                "unit": "%", 
                "data": [0.0, 0.0]
            }, 
            "comp1.Setpoints.SpHeat": {
                "unit": "oC", 
                "data": [17.5, 18.5]
            }, 
            "comp1.Setpoints.SpVent": {
                "unit": "oC", 
                "data": [19.5, 20.5]
            }, 
            "comp1.Scr1.Pos": {
                "unit": "0-1", 
                "data": [0.924, 1.0]
            }, 
            "comp1.Scr2.Pos": {
                "unit": "0-1", 
                "data": [0.908, 0.997]
            }, 
            "comp1.Lmp1.ElecUse": {
                "unit": "W/m2", 
                "data": [0.0, 0.0]
            }, 
            "comp1.McPureAir.Value": {
                "unit": "kg/m2/s", 
                "data": [0.0, 0.0]
            }, 
            "comp1.Setpoints.SpCO2": {
                "unit": "ppm", 
                "data": [310.0, 300.0]
            }, 
            "comp1.Growth.FruitFreshweight": {
                "unit": "gram plant-1", 
                "data": [0.0, 0.0]
            }, 
            "comp1.Growth.DVSfruit": {
                "unit": "0-1", 
                "data": [0.0, 0.0]
            }, 
            "comp1.Growth.DryMatterFract": {
                "unit": "0-1", 
                "data": [0.0, 0.0]
            }, 
            "comp1.Growth.CropAbs": {
                "unit": "0-1", 
                "data": [0.0, 0.0]
            }, 
            "comp1.Growth.PlantDensity": {
                "unit": "plants m-2", 
                "data": [56.0, 56.0]
            }, 
            "common.ElecPrice.PeakHour": {
                "unit": "bool", 
                "data": [0.0, 0.0]
            }
        }, 
        "stats": {
            "economics": {
                "info": {
                    "unit": "euro/m2", 
                    "fractionOfYear": 0.003, 
                    "averageDensity": 56.0
                }, 
                "fixedCosts": {
                    "objects": {
                        "comp1.Greenhouse": 0.041, 
                        "comp1.Lmp1": 0.029, 
                        "comp1.Scr1": 0.003, 
                        "comp1.Scr2": 0.003, 
                        "comp1.ConCO2": 0.004, 
                        "spacingSystem": 0.0
                    }, 
                    "total": 0.079
                }, 
                "variableCosts": {
                    "objects": {
                        "gas": 0.044, 
                        "elec": 0.001, 
                        "CO2": 0.029, 
                        "plants": 42.0
                    }, 
                    "total": 42.074
                }, 
                "gains": {
                    "objects": {
                        "product": 0.0
                    }, 
                    "total": 0.0
                }, 
                "balance": -42.154
            }
        }, 
        "usage": "0% of quotum used"
    }

    data_str = json.dumps(data_dict)
    
    @classmethod
    def from_response(cls, response):
        """
            Load data from a response object.
        """
        return cls(response.json(), 
                   response.text)
    
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
