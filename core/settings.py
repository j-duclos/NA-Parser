import os
from pathlib import Path

# Get App Root Directory
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
# Get Export folder and file location
export_path = Path(ROOT_DIR + "/Exports/")
export_file = Path(str(export_path) + "/Neighborhood-Associations-Export.zip")
file = Path(str(export_path) + "/Update_Log.csv")

