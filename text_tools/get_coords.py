'''
get_coords.py:

extract availible location co-oridnates from twitter data and write to json
file.
'''
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import zipfile
import json
from datetime import datetime, timedelta

# parse io args
parser = argparse.ArgumentParser(
    description="extract availible location co-oridnates from twitter data")
parser.add_argument(
    "-f", "--file", type=str, help="input filename", required=True)
parser.add_argument(
    "-o", "--out", type=str, help="output filename", required=True)
args = parser.parse_args()


coords = 0
total  = 0
files  = 0

location_data = []

time_read  = "%a %b %d %H:%M:%S +0000 %Y"

# [longitude, latitude]

def read_line(line):
    global coords, location_data
    tweet = json.loads(line)
    if tweet['coordinates']:
        lon, lat = tweet['coordinates']['coordinates']
        time = datetime.strptime(tweet["created_at"], time_read)
        location_data.append({"longitude": lon, "latitude": lat})
        coords += 1

with zipfile.ZipFile(args.file) as z:
    for fn in z.namelist()[1:]:
        print("reading:", fn)
        with z.open(fn) as f:
            for line in f:
                read_line(line)
                total += 1
        files += 1

print("{:.4f} location coverage".format(coords/total))
print("T:", total, "Coords:", coords)
print("files: ", files)
print("epocs:", epoch)

with open(args.out, "w") as f:
    json.dump(location_data, f, indent=2)
print("wrote file")
