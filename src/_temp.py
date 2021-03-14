import os
from os.path import join as opj
import numpy as np
import pandas as pd
import hjson as json
from datetime import datetime
import time
import pytz

myfiles = ['a', 'b', 'c', 'd']

for j, row in enumerate(myfiles):
    print(f'\r{j}/{len(myfiles)} ({row})', end='')
    time.sleep(1)
print()
