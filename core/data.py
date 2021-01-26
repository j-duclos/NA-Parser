import os
import zipfile
import MySQLdb
import logging
import sys
import os.path
from os import path

from MySQLdb.cursors import Cursor
from . import settings
import csv
from . import database

# Unzip exported file and delete file afterwards
def getData(export_path, export_file):
    try:
        data_zip = zipfile.ZipFile(export_file, 'r')
        data_zip.extractall(export_path)
        os.remove(export_file) 
    except FileNotFoundError as err:
        logging.error("No Zip File in the directory")
        logging.error(err)
        sys.exit()
    

# Caspio does not like long column names with symbols like # in it.  If you have columns that were renamed to fit into the Caspio format
# Rename them to match the MariaDb original name.  The will need to be formatted like '`ATTRIBUTE_NAME`'
def replaceCaspioDbHeaders():
    try:
        file = settings.file

        text = open(file, "r") 
        text = ''.join([i for i in text])  
        # search and replace the contents 
        text = text.replace("ANNUAL__DAYS_NOTIFICATION_ANNUAL", '`ANNUAL_#_DAYS_NOTIFICATION_ANNUAL_MTG`')  
        text = text.replace("REGULAR__DAYS_NOTIFICATION_FOR_R", '`REGULAR_#_DAYS_NOTIFICATION_FOR_REGULAR_MTG`') 
        # When adding images to Caspio the Caspio database will point to that folder.  This must be changed back to the original format
        # Deleting the Capio folder from the database corrects this format
        text = text.replace("/Neighborhood/", "")  
        
        # output.csv is the output file opened in write mode 
        x = open(file, "w") 
    
        # all the replaced text is written in the output.csv file 
        x.writelines(text) 
        x.close() 
    except Exception as err:
        logging.error("Error updating CSV file.")
        logging.error(err)
        sys.exit()

def updateDatabase():
    # Create database connection
    db_connection = database.db_connection
    cur = db_connection.cursor()
    file = settings.file
    rows = ""
    head = ""
    
    
    with open(file, 'r', encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        header = []
        dataRow = []
        column = ""
        head = ""
        for row in csv_reader:
            if line_count == 0:
                if row[0].__contains__("ID"):
                    # Puts all of the column from the header row into a list but removes the Id in the first column 
                    header = row[1::]
                    # This removes a 'Display' Column Caspio adds
                    header = header[:-1]
                    line_count += 1
                else:
                    # If there are no header columns, script will quit
                    logging.error("There are no header columns!")
                    break
            else:
                # Collects all column data into a list and removes the last column
                # The last column is added by Caspio and must be removed
                for i in range(1, len(row)):
                    dataRow.append(row[i])
                del dataRow[-1]

                # Uses Column index 0 to get ID number
                id = row[0]
                
                # Creates the query string and executes
                for col in range(len(dataRow)):
                    for col in range(len(header)):
                        column = dataRow[col]
                        query = (column, id)

                        queryString = str("UPDATE neighborhoods SET " + header[col] + str(" = %s WHERE ID = %s"))                    
                        try:
                            cur.execute(queryString, query)
                            db_connection.commit()
                        except Exception as err:
                            logging.error("An Error has occured:", err)

        logging.info("Updated database successfully!")
        logging.info("Closing csv_reader.")
        csv_file.close()
    logging.info("Closing db_connection.")
    db_connection.close()
    logging.info("Deleting CSV File.")
    os.remove(file) 