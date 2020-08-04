Person Of Interest - Tracking Applicaion

A simple application that tracks persons who were present in the same location at the same day of the interested person. Application is written in Python 3.8.
Application helps to load the data into the database. Application visualizes as cluster image of the tracking detail and image is be pushed to S3(if AWS configured) .This is a light wight application hosted using Flask application. Database used is PostgreSQL.


WorkFlows

1. Data Load
   Tracker Data needs to be loaded to the tables. Application uses 3 tables in POSTGRESQL DB.
   1. identity - Person or Identity details are saved in Identity Table
   2. location - Location Details
   3. tracker_data - Tracker data of users
   CSV files are loaded into the database. Please find the sample files at https://github.com/aj4amaljose/Tracker-Application/tree/master/tracker/tracker/sample_files 
   As as an initial setup you can create tables manualy or exectute command 
   """python https://github.com/aj4amaljose/Tracker-Application/blob/master/tracker/tracker/model.py -a create"""
  
2. Track person
   Input social no of the person and also number of days in past to be considered for tracking persons who are in the same location in the same day.

Deployment:
1. Manual:
   Steps to be followed:
    1. Requires Python 3.8
    2. poetry is used for Python Packaging and dependency management.In command prompt, Tracker as working directory,  Run "pip install poetry" and run  "poetry install".
    3. clone from https://github.com/aj4amaljose/Tracker-Application.git
    4. Set Environmental variables 
       1. POSTGRES_DB: DB Name
       2. POSTGRES_USER: DB user Name
       3. POSTGRES_PASSWORD: DB Password
       4. POI_APP_PORT: Default set to 80. Port at which app should be available

       If track image needs to be pushed to S3, then configure below environment variables.
       
       Create a user that has S3 push access. Fill up user credentials and bucket name for below environment variables
        1. AWS_ACCESS_KEY_ID
        2. AWS_SECRET_ACCESS_KEY
        3. AWS_DEFAULT_REGION
        4. TRACKER_AWS_S3_BUCKET
    5. Open http://localhost:POI_APP_PORT
    
2. Kubernetes deployment
   1. Deployment in local K8 cluster- Go through https://github.com/aj4amaljose/Tracker-Application/blob/master/tracker/k8s/local_deployment/README.md
    
   

