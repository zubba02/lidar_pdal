########Shuaib Rasheed/24112021/zubba1989@gmail.com########

import json
from glob import glob
import os
import subprocess

path_to_pdal = '../../PDAL/PDAL-2.3.0-src/build/bin/pdal'
file_name = 'cloud_7b61cea6'


subprocess.call('{} split --capacity 5000000 {}.las outfile.las'.format(path_to_pdal,file_name), shell=True)

all_files = [os.path.splitext(val)[0] for val in glob('out*')]

print (all_files)

with open ('make_ground.sh', 'w') as t_f:
	for i in all_files:
		t_f.write('echo EXECUTING GROUND LAS FOR FILE {}\n'.format(i))

		t_f.write("{} translate {}.las g_{}.las --json pipe1.json\n".format(path_to_pdal,i,i))


subprocess.call('./make_ground.sh', shell=True)

all_files = [os.path.splitext(val)[0] for val in glob('g_*')]

print (all_files)

for j in all_files:

  i = {
      "pipeline": [
      "{}.las".format(j),
          {
              "filename":"dem_{}.tif".format(j),
              "gdaldriver":"GTiff",
              "output_type":"all",
              "resolution":"1.0",
              "type": "writers.gdal"
          }
      ]
  }

  print(json.dumps(i, indent=8))

  with open('{}.json'.format(j), 'w') as outfile:
    json.dump(i, outfile)

  subprocess.call('{} pipeline {}.json'.format(path_to_pdal,j), shell=True)
	
all_files = [i for i in glob.iglob('*.tif')]

lines = all_files
with open('make_merge.sh', 'w') as f:
    f.write('gdal_merge.py  -init 255 -o Merged.tif ')
    for line in lines:
        f.write(line)
        f.write(' ')
	
subprocess.call('./make_merge.sh', shell=True)

subprocess.call('gdal2xyz.py -band 1 -csv Merged.tif To_Grid.csv', shell=True)
