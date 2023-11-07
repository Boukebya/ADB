import sys
from pathlib import Path
sys.path.append(str(Path.cwd())+'\project_env\Lib\site-packages')
import os
#print(os.path.isdir(sys.path[-1]))
pip_path = str(Path.cwd())+'\project_env\Scripts\pip.exe'
print(os.path.isfile(pip_path))
requirement_path = str(Path.cwd())+r'\OCR\requirements.txt'
print(os.path.isfile(requirement_path))
os.system(pip_path+ ' install -r '+requirement_path)
from enum import Enum
import io
import time
from PIL import Image
from google.cloud import vision
