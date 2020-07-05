import pandas as pd
import os
import numpy as np
from pandas import DataFrame

#### Importing csv
dir = 'F:/Downloads/Device Wizard Documentation/docs/AMMP/PV Task/Input/'
filepaths = [dir + f for f in os.listdir(dir) if f.endswith('.csv')]
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', 100)

def read_csv(fp):
    return pd.read_csv(fp, delimiter=';', index_col=['timestep(hours)'])

data = pd.concat(map(read_csv, filepaths), sort=False, axis=1)

#### Calculation of PV Generation, Total energy demand, and Electric demand after using PV
data['pv gen kWh'] = 0.2 * 10 ** 3 * 0.18 * data['capacity factor']
data['total_energy_demand'] = data['damand elec (kWh)'] + data['demand hot water (kWh)']
data['ELec_demand_after_using_pv'] = data['damand elec (kWh)'] - data['pv gen kWh']

#### with storage  turbine generation
data['turbine_gen'] = data['damand elec (kWh)'] - data['pv gen kWh']

#### Without storage turbine generation
data['turbine_gen_1'] = data['total_energy_demand'] - data['pv gen kWh']

###### Storage Level calculation
initialize_soc_kWh = 0.25 * (10 ** 3)
minimum_soc_KWh = 0.1 * (10 ** 3)

data['storage_level_kWh'] = 0
data.iloc[0, data.columns.get_loc('storage_level_kWh')] = 250
data['storage_level_kWh'] = np.where(data['ELec_demand_after_using_pv'] < 0, -data['ELec_demand_after_using_pv'],
                                     data['storage_level_kWh'])
data['temp'] = data['storage_level_kWh'].shift(-1)
data['temp1'] = 0

co2= 0      ####CO2 Emission with storage
co2_1= 0    ####CO2 Emission without storage

for index, row in data.iterrows():
    index = index + 1
    if (data.loc[index - 1, 'storage_level_kWh'] < 100):                          ####  Correcting SOC below 20%
        row['temp1'] = 200 - data.loc[index - 1, 'storage_level_kWh']
        data.loc[index - 1, 'storage_level_kWh'] = 200
        data.loc[index - 1, 'turbine_gen'] = data.loc[index - 1, 'turbine_gen'] + row['temp1']
    data.loc[index, 'storage_level_kWh'] = row['temp'] + data.loc[index - 1, 'storage_level_kWh'] - data.loc[
        index - 1, 'demand hot water (kWh)']
    co2= co2 + 0.4 * data.loc[index - 1, 'turbine_gen']
    co2_1= co2_1 + 0.4 * data.loc[index - 1, 'turbine_gen_1']

del data['temp']
del data['temp1']

#### Correcting Turbine generation values by excluding extra PV generation (With storage)
data['turbine_generation_s'] = data['turbine_gen']
for index, row in data.iterrows():
    if (data.loc[index, 'turbine_gen'] < 0):
        row['turbine_generation_s'] = 0
        
#### Correcting Turbine generation values by excluding extra PV generation (Without storage)
data['turbine_generation_ws'] = data['turbine_gen_1']
for index, row in data.iterrows():
    if (data.loc[index, 'turbine_gen_1'] < 0):
        row['turbine_generation_ws'] = 0


#### Writing Output in Output.csv
df = DataFrame(data, columns=['turbine_generation_s', 'pv gen kWh', 'storage_level_kWh'])
export_csv = df.to_csv('F:/Downloads/Device Wizard Documentation/docs/AMMP/PV Task/Output/Output.csv', index=True, header=True)

#Efficiency of renewable generation with storage and without storage
pv=data['pv gen kWh'].sum(axis=0)
turbine=data['turbine_generation_s'].sum(axis=0)
turbine1=data['turbine_gen_1'].sum(axis=0)
percentage=pv*100/(pv+turbine)
percentage1=pv*100/(pv+turbine1)

print ('Efficiency of renewable generation with storage')
print(pv,turbine,'\n', percentage,'%','\n')
print('Efficiency of renewable generation without storage')
print(pv, turbine1,'\n', percentage1,'%')

#CO2 Savings
print('\n','CO2 Emissions with storage','\n', co2,'\n')
print('CO2 Emission without storage','\n', co2_1,'\n')
print('CO2 Savings','\n', co2_1-co2, 'Kgs')



