Person Of Interest - Tracking Application

Application can be deployed using Kubernetes. 
Configurations in https://github.com/aj4amaljose/Tracker-Application/tree/master/tracker/k8s/local_deployment folder can be used to setup application in local K8 cluster.
Application uses PostgreSQL Database. 

Follow below steps:

1. postgres_secrets.yaml setup
   Secret accepts requires encoded values.( Ref https://kubernetes.io/docs/concepts/configuration/secret/)
   Encode secret value for each key using command :   echo -n '<value>' | base64
   Values to be configured in postgres_secrets.yaml are:
    1. POSTGRES_DB: Encoded Database Name
    2. POSTGRES_USER: Encoded User Name 
    3. POSTGRES_PASSWORD: Encoded Database password
   Deploy secret in cluster using command: kubectl create -f postgres_secrets.yaml
   
2. poi_aws_secret.yaml setup for  AWS S3 update 
    1. AWS_ACCESS_KEY_ID: Encoded AWS access key id
    2. AWS_SECRET_ACCESS_KEY: Encoded secret access key
    3. TRACKER_AWS_S3_BUCKET: Encoded AWS S3 bucket name
    
    if you don't need AWS S3 updated, don't deploy this secret. Also remove below lines from deployment.yaml
	
	"""- secretRef:
        name: poi-aws-secret"""
	
    else fillup details and deploy secret using command: kubectl create -f poi_aws_secret.yaml
	
3. Deploy remaining k8 resources using command: kubectl create -f deployment.yaml

4. Access application http://localhost:30216

   
