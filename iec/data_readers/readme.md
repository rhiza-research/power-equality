## Data convertors
Each subfile in this folder contains scripts to convert different datasets into the standard format
accepted by the analysis functions in this library. 

The standard format has the following columns:
1. id [string / int] - measurement point identifier [eg - name or sensor uuid]
2. time [datetime] - timestamp of sample
3. value [float] - measured value
4. value name - name of value; must be one of the identifier strings documented below. 
5. latitude [float] - latitude of measurement
6. longitude [float] - longitude of measurement
7. site_class [string] - one of rural, urban, periurban
8. voltage_class [string] - one of lv, mv, hv
9. customer_class [string] - one of residential, commercial, industrial

Values
------
The value has the following form: [quantity]_[mag/ang]_[phase]_[units]
phase is one of A, B, C, N
units are: w (watts), kw (kilowatts), v (volts), kv (kilovolts), etc. 
Therefore: 
voltage_mag_A_v is voltage magnitude on phase A. 
power_mag_A_w is power on phase A in watts. 

Unknowns
--------
If a parameter is uknown for a measurement, it's value should be set to None.

