##########################################################
# COMBINING FRESNO RECORD CSVS, written by Lara Karacasu #
##########################################################

# NOTE: If a file named 'fresno.csv' exists on your machine, this code will throw a permission error - if that is the case, rename the CSV file

# IMPORT LIBRARIES
import pandas as pd
import glob
import os

# CHANGE WORKING DIRECTORY
os.chdir(r"C:\Users\larak\pit-dsc\fresno-scraping")

# SET PATH
fresno_csvs = [i for i in glob.glob('*.{}'.format('csv'))]

# COMBINE FILES
fresno_csv = pd.concat([pd.read_csv(file) for file in fresno_csvs])

# EXPORT 
fresno_csv.to_csv( "fresno.csv", index=False, encoding='utf-8-sig')