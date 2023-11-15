import sys
from pathlib import Path
sys.path.append(str(Path.cwd())+'\project_env\Lib\site-packages')
import os
#print(os.path.isdir(sys.path[-1]))
pip_path = str(Path.cwd())+'\project_env\Scripts\pip.exe'
requirement_path = str(Path.cwd())+r'\list_analyse\requirements.txt'
os.system(pip_path+ ' install -r '+requirement_path)
import pandas as pd
import re
import unidecode
from os import listdir
from os.path import isfile, join
from collections import Counter
import numpy as np
import time
import json