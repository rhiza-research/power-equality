## Data convertors
Each subfile in this folder contains scripts to convert different datasets into the standard format
accepted by the analysis functions in this library. 

The standard format has the following columns:
1. id [string / int] - measurement point identifier [eg - name or sensor uuid]
2. time [datetime] - timestamp of sample
3. value [float] - measured value
4. value name - name of value; must be one of the identifier strings documented below. 
4. location [tuple (lat, lon)] - location of measurement

Values
------
The value has the following form: [quantity]_[mag/ang]_[phase]_[units]
phase is one of A, B, C, N
units are: w (watts), kw (kilowatts), v (volts), kv (kilovolts), etc. 
Therefore: 
voltage_mag_A_v is voltage magnitude on phase A. 
power_mag_A_w is power on phase A in watts. 

