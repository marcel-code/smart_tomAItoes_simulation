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
            "DateTime": {                       # DateTime in Excel date format
                "unit": "OLE Automation date",
                "data": [45174.041667, 45174.083333]
            }, 
            "comp1.Air.T": {                    # inside greenhouse air temperature
                "unit": "oC", "data": [18.0, 19.28 ]
            }, 
            "comp1.Air.RH": {                   # inside greenhouse humidity (0-100)
                "unit": "%", 
                "data": [72.1, 68.7]
            }, 
            "comp1.Air.ppm": {                  # inside greenhouse CO2 concentration
                "unit": "ppm", 
                "data": [400.0, 400.0]
            }, 
            "common.Iglob.Value": {             # outside greenhouse solar radiation
                "unit": "W/m2", 
                "data": [0.0, 0.0]
            }, 
            "common.Tout.Value": {              # outside greenhouse air temperature
                "unit": "oC", 
                "data": [16.8, 16.4]
            }, 
            "common.RHout.Value": {             # outside greenhouse humidity (0-100)
                "unit": "%", 
                "data": [86.4, 87.3]
            }, 
            "common.Windsp.Value": {            # outside greenhouse wind speed
                "unit": "m/s", 
                "data": [0.8, 1.3]
            }, 
            "comp1.PARsensor.Above": {          # light intensity (= photon flux density) just above the crop inside greenhouse
                "unit": "umol/m2/s", 
                "data": [0.0, 0.0]
            }, 
            "comp1.TPipe1.Value": {             # average heating pipe temperature inside greenhouse
                "unit": "oC", 
                "data": [43.393038625547376, 37.263411730190654,]
            }, 
            "comp1.ConPipes.TSupPipe1": {       # supply pipe temperature inside greenhouse
                "unit": "oC", 
                "data": [47.5, 38.5]
            }, 
            "comp1.PConPipe1.Value": {          # heating power applied to the heating system inside greenhouse
                "unit": "W/m2", 
                "data": [108.3, 27.2]
            }, 
            "comp1.ConWin.WinLee": {            # vent/window-openings on lee side of greenhouse
                "unit": "%", 
                "data": [0.0, 0.0]
            }, 
            "comp1.ConWin.WinWnd": {            # vent/window-openings on wind side of greenhouse
                "unit": "%", 
                "data": [0.0, 0.0]
            }, 
            "comp1.Setpoints.SpHeat": {         # heating setpoint used in simulation
                "unit": "oC", 
                "data": [17.5, 18.5]
            }, 
            "comp1.Setpoints.SpVent": {         # ventilation setpoint used in simulation
                "unit": "oC", 
                "data": [19.5, 20.5]
            }, 
            "comp1.Scr1.Pos": {                 # position of transparent screen (transmission of 70%; upper most screen) on greenhouse roof
                "unit": "0-1", 
                "data": [0.924, 1.0]
            }, 
            "comp1.Scr2.Pos": {                 # position of light blocking screen (transmission of less than 1%; second screen) on greenhouse roof
                "unit": "0-1", 
                "data": [0.908, 0.997]
            }, 
            "comp1.Lmp1.ElecUse": {             # electrical power used to power LEDs for inside greenhouse illumination
                "unit": "W/m2", 
                "data": [0.0, 0.0]
            }, 
            "comp1.McPureAir.Value": {          # CO2 dosing rate inside greenhouse
                "unit": "kg/m2/s", 
                "data": [0.0, 0.0]
            }, 
            "comp1.Setpoints.SpCO2": {          # CO2 dosing setpoint used in simulation
                "unit": "ppm", 
                "data": [310.0, 300.0]
            }, 
            "comp1.Growth.FruitFreshweight": {  # total fruit fresh weight in grams per plant
                "unit": "gram plant-1", 
                "data": [0.0, 0.0]
            }, 
            "comp1.Growth.DVSfruit": {          # fruit development stage (raction of fruits that is ripe, 0 = no ripe fruits, 1 = all fruits are ripe, sellable for values higher equal 0.5 when value is not zero)
                "unit": "0-1", 
                "data": [0.0, 0.0]
            }, 
            "comp1.Growth.DryMatterFract": {    # dry matter content (DMC) of the fruits (indicator for tastefulness, ripeness, ...)
                "unit": "0-1", 
                "data": [0.0, 0.0]
            }, 
            "comp1.Growth.CropAbs": {           # fraction of PAR light absorbed by crop
                "unit": "0-1", 
                "data": [0.0, 0.0]
            }, 
            "comp1.Growth.PlantDensity": {      # number of plants per m² used in simulation
                "unit": "plants m-2", 
                "data": [56.0, 56.0]
            }, 
            "common.ElecPrice.PeakHour": {      # True (1) if it is (an expensive) peak hour
                "unit": "bool", 
                "data": [0.0, 0.0]
            }
        }, 
        "stats": {
            "economics": {
                "info": {
                    "unit": "euro/m2", 
                    "fractionOfYear": 0.003,    # of greenhouse occupation (here probably between 0.14 and 0.20)
                    "averageDensity": 56.0      # average number of plants per m² used in simulation
                }, 
                "fixedCosts": {
                    "objects": {
                        "comp1.Greenhouse": 0.041,  # fixed costs for greenhouse occupation
                        "comp1.Lmp1": 0.029,        # fixed costs for depreciation and maintenance of lamps
                        "comp1.Scr1": 0.003,        # fixed costs for depreciation and maintenance of screen 1
                        "comp1.Scr2": 0.003,        # fixed costs for depreciation and maintenance of screen 2
                        "comp1.ConCO2": 0.004,      # fixed costs for CO2 dosing system
                        "spacingSystem": 0.0        # fixed costs for level of sophistication of the spacing system
                    }, 
                    "total": 0.079          # total fixed costs
                }, 
                "variableCosts": {
                    "objects": {
                        "gas": 0.044,       # variable costs for heating
                        "elec": 0.001,      # variable costs for electricity
                        "CO2": 0.029,       # variable costs for CO2 dosing
                        "plants": 42.0      # variable costs for buying plants
                    }, 
                    "total": 42.074         # total variable costs
                }, 
                "gains": {
                    "objects": {
                        "product": 0.0      # gains for selling potted dwarf tomatoes
                    }, 
                    "total": 0.0            # total gains
                }, 
                "balance": -42.154          # net profit
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
