#### Description

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

For the timestamp format as required by `time_format` please use these [format codes](https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes).
