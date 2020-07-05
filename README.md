# PV-and-Heat-storage
Storages within the Energy System of the Future
(Veena Prakash Tantri)

 The aim of this python program is to calculate the power plant schedule (dispatch) of the gas turbine for all load hours with the goal of minimizing CO2 emissions.
 
Assumptions made: 
•	SOC must stay above 20%. 
•	initial stored energy is 0.25 MWh (50% state of charge)
•	There are no transmission/conversion losses. 
•	Temperatures within storage tank are neglected.

 <img src= "">

1.	I use input data from files “demand_elec_households”, “demand_hotwater_households” and “pv_capacity_factor”. 
2.	A file called “Output” is generated which consists of generation timeseries of the gas turbine, the photovoltaic panels and the level of the storage. 
3.	I have calculated the percentage of renewable energy supply of the household with and without storage. Also, the CO2 savings with storage is calculated. 

