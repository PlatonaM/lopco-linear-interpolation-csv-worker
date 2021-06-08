## lopco-linear-interpolation-csv-worker

Uses linear interpolation to fill gabs in CSV files. CSV files must have a column with timestamps.

### Configuration

`delimiter`: Delimiter used by the CSV file.

`time_column`: Column containing timestamps.

`time_format`: Please use these [format codes](https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes) when providing the timestamp format.

`target_columns`: Columns containing gabs to fill.

### Inputs

Type: single

`source_csv`: Input CSV file.

### Outputs

Type: single

`output_file`: Result CSV file.

### Description

    {
        "name": "Linear Interpolation CSV",
        "image": "platonam/lopco-linear-interpolation-csv-worker:latest",
        "data_cache_path": "/data_cache",
        "description": "Use linear interpolation to fill empty fields of a Comma-Separated Values files.",
        "configs": {
            "delimiter": null,
            "time_format": null,
            "time_column": null,
            "target_columns": null
        },
        "input": {
            "type": "single",
            "fields": [
                {
                    "name": "source_csv",
                    "media_type": "text/csv",
                    "is_file": true
                }
            ]
        },
        "output": {
            "type": "single",
            "fields": [
                {
                    "name": "output_file",
                    "media_type": "text/csv",
                    "is_file": true
                }
            ]
        }
    }
