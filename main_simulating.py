import argparse
import copy
from datetime import datetime
from pathlib import Path

## TODO SECTION

# TODO general:
# TODO implement LED variations + further, non-dimmable, only on-off

# TODO start:
# TODO check for all input parameters whether important or not. Which order is senseful
# TODO check for all input parameters how they can be expressed. Which ways are easiest to implement?! -> encoding?!
# TODO implement rules for parameter value generations, like limitations, dependencies, ordering, etc.
# TODO invent own parametization, e.g. invent interdependencies between parameters. Like for timepoints etc, with datetimes

# TODO pipeline:
# TODO write postprocessing script: not as script but as method/function/module/... in the src folder as tool. So it is run "automatically" after the simulation while learning
# TODO write postprocessing script: Which metrics to calculate? Which features to extract and interpret?!

# TODO training features:
# TODO Controller soll in den 1h, die der Simulator offen ist, sich an diesen "anpassen"?! -> Wie livetraining in RL
# TODO Kann ich irgendwas/irgendein Netz trainieren, mit dem ich analysieren kann, welche Parameter besonders relevant sind?!

# TODO modelling:
# TODO idea in general: Benutze Infos aus Modellen aus PDF dazu, genauere Vorhersagen (bspw. des Wetters) zu treffen, um die Control parameter besser vorgeben zu können. Erstelle entsprechende Modelle / Networks.
# TODO starte mit einem heruntergebrochenes Problem. Fange an, etwas lauffähiges zu erzeugen
# TODO starte zB mit: NN mit randomparametern testen, wie BasicNN (bei Part A). Denn: normalerweise try-and-error, alles austesten und besten nehmen. Hier: Lücken approximieren
# TODO RL oder NN: mache wie in KTH_RL: a) indexing von ausgewählten diskreten variablen werten (für manche variablen); b) und funktion approx für andere variablen lernen

# TODO training:
# TODO baue conda environment (create als yaml file), pip tensorboard, pip ..., vgl MG
# TODO invent yaml file to configure the simulation
# TODO invent logger to track the simulation

# TODO finetuning:
# TODO limit of nested for loops is 20!
# TODO simulation end date could be adjusted at the end when all other parameters are fix... maybe

## METHODS SECTION

def method_1():
    pass

## MAIN SECTION

if __name__ == "__main__":
    
    # Parse arguments
    #parser = argparse.ArgumentParser()
    #parser.add_argument("dummy")
    #args = parser.parse_intermixed_args()
    print(len([float(x) for x in range(0, 51, 5)]))