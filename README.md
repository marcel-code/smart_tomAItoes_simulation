# smart_tomAItoes_simulation
Part B. Simulation.

########################################################

# Explanations for input and output variables

########################################################

# Sensors

# weather station (measures outside greenhouse conditions)
# common.Iglob.Value # solar radiation
# common.Tout.Value # outside greenhouse air temperature
# common.RHout.Value # outside greenhouse humidity
# common.Windsp.Value # outside greenhouse wind speed

# measuring station (measures inside greenhouse conditions)
# comp1.Air.T # inside greenhouse air temperature
# comp1.Air.RH # inside greenhouse relative humidity
# comp1.Air.ppm # inside greenhouse CO2 concentration

# PAR sensor
# comp1.PARsensor.Above # photon flux density just above the crop in µmol/(m² s)

########################################################

# Actuators

# heating actuators
# comp1.PConPipe1.Value # heating power applied to the heating system in W/m²
# comp1.TPipe1.Value # average heating pipe temperature
# comp1.ConPipes.TSupPipe1 # supply temperature

# ventilation
# comp1.ConWin.WinLee # vent-openings on lee side
# comp1.ConWin.WinWnd # vent-openings on wind side

# screens
# comp1.Scr1.Pos # position of transparent screen (transmission of 70%)
# comp1.Scr2.Pos # position of light blocking screen (transmission of less than 1%)

# illumination (LEDs)
# comp1.Lmp1.ElecUse # electrical power used to power LEDs for inside greenhouse illumination

# CO2 supply
# comp1.McPureAir.Value # CO2 supply rate in kg/(m² s)

########################################################

# Temperature Control

# heating setpoints
# comp1.setpoints.temp.@heatingTemp # structure that represents a time-value combination (give as input)
# comp1.Setpoints.SpHeat # used heating setpoint (provided as output)

# ventilation setpoints (provided to the simulator as offset from heating setpoints -> P-Band?!)
# comp1.setpoints.temp.@ventOffset # ventilation line is defined as an offset relative to the heating setpoint. Limited by 2 °C/h
# comp1.Setpoints.SpVent # used ventilation setpoint (provided as output)

# (simulation-model) influence of solar radiation
# comp1.setpoints.temp.@radiationInfluence # parameters to define the table-like influence of solar radiation on the (minimum pipe) temperature. Deactivated with "0".

# (simulation-model) heating system settings
# comp1.heatingpipes.pipe1.@maxTemp # maximum applied heating pipe temperature (can also be changed during the year and over the day)
# comp1.heatingpipes.pipe1.@minTemp # minimum applied heating pipe temperature (can also be changed during the year and over the day)
# also: overrule min/max pipe temperature by setting them equal and @readiationInfluence to zero

# (simulation-model) windward-leeward-vents settings
# comp1.setpoints.temp.@PbandVent # P-band for the ventilation control. Leeward vent opening. Often: set proportional band depending on outside temperature
# comp1.setpoints.ventilation.@startWnd # Start of the windward vent opening
# comp1.setpoints.ventilation.@winLeeMin # limitations, can also be "abused" with direct passing of setpoints
# comp1.setpoints.ventilation.@winLeeMax # limitations, can also be "abused" with direct passing of setpoints
# comp1.setpoints.ventilation.@winWndMin # limitations, can also be "abused" with direct passing of setpoints
# comp1.setpoints.ventilation.@winWndMax # limitations, can also be "abused" with direct passing of setpoints

########################################################

# Humidity Control (fixed for all teams)

########################################################

# Screens

# (simulation-model) assign a certain screen type to a screen
# comp1.screens.scr1.@enable # enable/disable screen scr1
# comp1.screens.scr1.@material # type, like light blocking screen
# comp1.screens.scr1.@ToutMax # tells above what outside temperature the screen is not used
# comp1.screens.scr1.@closeBelow # Deploys the screen when the outside radiation is below a certain level, so controls the behaviour at dawn, early morning, and night
# comp1.screens.scr1.@closeAbove # controls the screen when the radiation exceeds a certain value, so is  meant to be used when using screens for shading.
# comp1.screens.scr1.@gapOnTempExc # screen gap as a function of air temperature excess compared to heating setpoint
# comp1.screens.scr1.@lightPollutionPrevention # tells that the controller should always close this screen when lights are on during night-time

# Examples/Types given: blackout screen settings / energy	screen	settings

########################################################

# Illumination control

# (simulation-model) assign a certain lamp settings (may also vary over the year / day-by-day)
# comp1.illumination.lmp1.@enabled # enabler (also particular for periods)
# comp1.illumination.lmp1.@intensity # define the amount of PAR light provided by the lamps in µmol/(m² s)
# comp1.illumination.lmp1.@hoursLight # defines the maximum number of running hours of the lamp
# comp1.illumination.lmp1.@endTime # defines at which time the lamps are switched off
# comp1.illumination.lmp1.@maxIglob # criterion for the outside radiation above which the lamps are switched off
# comp1.illumination.lmp1.@maxPARsum # prevent lamps switching on in the afternoon after a sunny day (this can be switched off by providing a high value)

########################################################

# CO2 supply control

# provide the CO2-capacity
# comp1.common.CO2dosing.@pureCO2cap # maximum CO2-capacity in kg/(ha h)

# control the CO2-supply (also date dependant)
# comp1.setpoints.CO2@setpoint # setpoints (expressed in ppm)
# comp1.setpoints.CO2@setpIfLamps # setpoint for CO2 can be overruled by a setpoint when the lamps are on (expressed in ppm)
# comp1.setpoints.CO2@doseCapacity # adjust the maximum supply rate.

# comp1.Setpoints.SpCO2 # used CO2 setpoint (provided as output)

########################################################

# Crop control

# Product quality
# comp1.Growth.DryMatterFract # dry matter content (DMC) of the fruits (provided as output) - tastefulness, ripeness, ...
# comp1.Growth.FruitFreshWeight # total fruit fresh weight in grams per plant (provided as output)
# comp1.Growth.DVSfruit # fruit development stage (provided as output) - sellable for values higher equal 0.5 (= value is not zero)

# crp_dwarftomato.cropModel.@plantDensity # set plant-density information to the crop-simulation-model

# comp1.Growth.PlantDensity # used plant density in plants per m² (provided as output)
# comp1.Growth.CropAbs # result of plant density and crop size (provided as output)

# simset.@startDate
# harvest moment

########################################################

# Net Profit calculation

# (total) gains
# comp1.Growth.DVSfruit # fruit development stage (provided as output) - sellable for values higher equal 0.5 (= value is not zero)
# stats.economics.averagePotPerM2 #  average number of pots per m² (provided as output)
# stats.economics.gains.total # total gain (provided as output)

# (total) fixed costs
# plantCosts # (provided as output)
# greenhouseOccupation # (provided as output)
# fractionOfYear # of greenhouse occupation (provided as output) - between 0.14 and 0.20
# Fixed	CO2 costs
# Fixed	Lamp costs
# Fixed	screen	costs
# Spacing costs

# (total) variable costs
# OnPeakElec # on-peak electricity costs for the LEDs (provided as output)
# OffPeakElec # off-peak electricity costs for the LEDs (provided as output)
# ElectricityCosts # total electricity costs for the LEDs (provided as output)
# HeatingCosts

# net profit
# res.stats.economics.@balance # net profit (provided as output)

########################################################