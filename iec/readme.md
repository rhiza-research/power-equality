# iec

- `data_readers/` - readers that take arbitrary input files of measurements and convert them into the standard CSV format described in [data_readers/readme.txt](data_readers/readme.txt).
- `metrics/` - functions that take standardized pandas dfs as input and produce statistical outputs.
- `visuals/` - functions that take metrics and produce visualizations. Metrics and visuals of a single genre (e.g. map, time series) live together in one file.
