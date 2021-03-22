"""
   Copyright 2021 InfAI (CC SES)

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""


import os
import datetime
import uuid
import requests


dep_instance = os.getenv("DEP_INSTANCE")
job_callback_url = os.getenv("JOB_CALLBACK_URL")
input_file = os.getenv("source_csv")
delimiter = os.getenv("delimiter")
time_col = os.getenv("time_column")
time_format = os.getenv("time_format")
target_columns = set(os.getenv("target_columns").split(delimiter))
data_cache_path = "/data_cache"


def get_microseconds(timestamp: str) -> int:
    dt = datetime.datetime.strptime(timestamp, time_format)
    return int(dt.timestamp() * 1000000)


def linear_interpolation(x_1, y_1, x_2, y_2, x):
    return y_1 + (y_2 - y_1) / (x_2 - x_1) * (x - x_1)


data = list()

with open(os.path.join(data_cache_path, input_file), "r") as in_file:
    first_line = in_file.readline().strip()
    first_line = first_line.split(delimiter)
    for line in in_file:
        data.append(line.strip().split(delimiter))

time_col_num = first_line.index(time_col)

print("number of target columns: {}".format(len(target_columns)))
buffer = list()
for col in target_columns:
    print("interpolating '{}' ...".format(col))
    pos = first_line.index(col)
    for line in data:
        if line[pos] and not buffer or not line[pos] and buffer:
            buffer.append(line)
        elif line[pos] and buffer:
            buffer.append(line)
            buffer_len = len(buffer)
            last_line = buffer[buffer_len - 1]
            x_2 = get_microseconds(last_line[time_col_num])
            y_2 = float(last_line[pos])
            for x in range(buffer_len):
                if x < buffer_len - 2:
                    buffer[x + 1][pos] = str(linear_interpolation(
                        x_1=get_microseconds(buffer[x][time_col_num]),
                        y_1=float(buffer[x][pos]),
                        x_2=x_2,
                        y_2=y_2,
                        x=get_microseconds(buffer[x + 1][time_col_num])
                    ))
            buffer.clear()
            buffer.append(last_line)
    buffer.clear()

output_file = uuid.uuid4().hex

with open(os.path.join(data_cache_path, output_file), "w") as out_file:
    out_file.write(delimiter.join(first_line) + "\n")
    line_count = 1
    for line in data:
        out_file.write(delimiter.join(line) + "\n")
        line_count += 1

with open(os.path.join(data_cache_path, output_file), "r") as file:
    for x in range(5):
        print(file.readline().strip())
print("total number of lines written: {}".format(line_count))

try:
    resp = requests.post(
        job_callback_url,
        json={dep_instance: {"output_file": output_file}}
    )
    if not resp.ok:
        raise RuntimeError(resp.status_code)
except Exception as ex:
    try:
        pass
        os.remove(os.path.join(data_cache_path, output_file))
    except Exception:
        pass
    raise ex
