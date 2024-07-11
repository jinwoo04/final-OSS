import os
from zipfile import ZipFile
from datetime import datetime

def get_region_name(file):

    filename = os.path.basename(file)
    region = filename.split('_')[-1].split('.')[0]
    return region