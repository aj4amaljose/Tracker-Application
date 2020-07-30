Person Of Interest - Tracking Applicaion

This application is used to track persons who were present in the same location at the same day. Application is written in Python 3.8.
Application helps to load the data into the database. Also enables to search persons who were in same locations of person of interest.
Application visualizes as a cluster image.This is a light wight application hosted using Flask application.

Steps to be followed:
 1.Requires Python 3.8
 2.poetry is used for Python Packaging and dependency management. Run pip install poetry and run Poetry install with tracker as current directory.
 3.clone from https://github.com/aj4amaljose/Tracker-Application.git
 4.Add extension https://chrome.google.com/webstore/detail/web-server-for-chrome/ofhbbkphhbklhfoeikjpcbhemlocgigb  for local development(optional)
 5.Set Environmental variables 
   . TRACKER_DB_URL - DataBase Url
   . TRACKER_GRAPH_FOLDER - Local directory for saving Cluster Images
   . TRACKER_HTTP_SERVER - Provide the server details set in step 4 or the server where you want to save and pull the generated cluster image

WorkFlows

1. Data Load
   Data is to loaded into database. You configure it at TRACKER_DB_URL environmental variable
   CSV files are loaded into the database. Please find the sample files at https://github.com/aj4amaljose/Tracker-Application/tree/master/tracker/tracker/sample_files .
   DataBase Sample can be found at https://github.com/aj4amaljose/Tracker-Application/tree/master/tracker/tracker/sample_db .
   As as an initial setup you can create tables manualy or running https://github.com/aj4amaljose/Tracker-Application/blob/master/tracker/tracker/model.py
   In DataBase, data is stored in 3 Tables. Person or Identity details are saved in Identity Table. Location details in Location table and Tracking data in tracker_data
   
2. Track person
   Input social no of the person and also number of days in past to be considered for tracking persons who are in the same location in the same day.
   Cluster Image is saved at the location given in TRACKER_GRAPH_FOLDER.

