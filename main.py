from core.data import *
from core.settings import *
import logging
import os.path
from os import path


def main():
    logging.basicConfig(filename='ParserLog.log', level=logging.DEBUG)    
    if path.exists(export_file):
        getData(export_path, export_file)
        logging.info("Getting Zip file and exporting data!")
    logging.info("Replacing Caspio column headers")
    replaceCaspioDbHeaders()
    logging.info("Collecting all data from csv file!")
    updateDatabase()

if __name__ == "__main__":
    main()