from core.data import *
from core.settings import *
import logging


def main():
    logging.basicConfig(filename='ParserLog.log', level=logging.DEBUG)    
    logging.info("Getting Zip file and exporting data!")
    getData(export_path, export_file)
    logging.info("Replacing Caspio column headers")
    replaceCaspioDbHeaders()
    logging.info("Collecting all data from csv file!")
    updateDatabase()

if __name__ == "__main__":
    main()