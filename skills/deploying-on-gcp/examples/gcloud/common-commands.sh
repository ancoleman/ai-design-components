#!/bin/bash

################################################################################
# GCP gcloud CLI Common Commands Reference
################################################################################
#
# Comprehensive reference for the most common gcloud CLI operations.
# Organized by service category with helpful comments and flag combinations.
#
# Usage:
#   - Copy and adapt commands for your specific needs
#   - Replace placeholders (PROJECT_ID, REGION, etc.) with actual values
#   - All commands are non-destructive examples unless marked with [DESTRUCTIVE]
#
# Prerequisites:
#   - gcloud CLI installed: https://cloud.google.com/sdk/docs/install
#   - Authenticated: gcloud auth login
#   - Project set: gcloud config set project PROJECT_ID
#
################################################################################

################################################################################
# 1. PROJECT AND ORGANIZATION MANAGEMENT
################################################################################

# List all projects you have access to
gcloud projects list

# Show detailed information about a project
gcloud projects describe PROJECT_ID

# Set active project (affects all subsequent commands)
gcloud config set project PROJECT_ID

# Show current configuration
gcloud config list

# Create a new project [REQUIRES ORG PERMISSIONS]
gcloud projects create PROJECT_ID \
  --name="Project Display Name" \
  --organization=ORGANIZATION_ID

# Link project to billing account [REQUIRES BILLING ADMIN]
gcloud billing projects link PROJECT_ID \
  --billing-account=BILLING_ACCOUNT_ID

# List available billing accounts
gcloud billing accounts list

# Enable required APIs for a project
gcloud services enable compute.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable container.googleapis.com
gcloud services enable sqladmin.googleapis.com
gcloud services enable storage.googleapis.com
gcloud services enable bigquery.googleapis.com

# List enabled services in current project
gcloud services list --enabled

# Set default region and zone
gcloud config set compute/region us-central1
gcloud config set compute/zone us-central1-a

# View all available regions
gcloud compute regions list

# View all available zones
gcloud compute zones list


################################################################################
# 2. COMPUTE ENGINE OPERATIONS
################################################################################

# List all VM instances
gcloud compute instances list

# List instances in specific zone
gcloud compute instances list --zones=us-central1-a

# Create a standard VM instance
gcloud compute instances create INSTANCE_NAME \
  --zone=us-central1-a \
  --machine-type=e2-medium \
  --image-family=debian-11 \
  --image-project=debian-cloud \
  --boot-disk-size=20GB \
  --boot-disk-type=pd-standard \
  --tags=http-server,https-server

# Create VM with custom startup script
gcloud compute instances create INSTANCE_NAME \
  --zone=us-central1-a \
  --machine-type=e2-medium \
  --image-family=debian-11 \
  --image-project=debian-cloud \
  --metadata-from-file=startup-script=startup.sh

# Create VM with service account and scopes
gcloud compute instances create INSTANCE_NAME \
  --zone=us-central1-a \
  --machine-type=e2-medium \
  --image-family=debian-11 \
  --image-project=debian-cloud \
  --service-account=SERVICE_ACCOUNT_EMAIL \
  --scopes=cloud-platform

# Start a stopped instance
gcloud compute instances start INSTANCE_NAME --zone=us-central1-a

# Stop a running instance
gcloud compute instances stop INSTANCE_NAME --zone=us-central1-a

# Reset (restart) an instance
gcloud compute instances reset INSTANCE_NAME --zone=us-central1-a

# SSH into an instance
gcloud compute ssh INSTANCE_NAME --zone=us-central1-a

# SSH with specific user
gcloud compute ssh USERNAME@INSTANCE_NAME --zone=us-central1-a

# Copy files to instance
gcloud compute scp LOCAL_FILE INSTANCE_NAME:~/REMOTE_PATH --zone=us-central1-a

# Copy files from instance
gcloud compute scp INSTANCE_NAME:~/REMOTE_FILE ./LOCAL_PATH --zone=us-central1-a

# View instance details
gcloud compute instances describe INSTANCE_NAME --zone=us-central1-a

# List available machine types
gcloud compute machine-types list --filter="zone:us-central1-a"

# List available images
gcloud compute images list

# Delete an instance [DESTRUCTIVE]
gcloud compute instances delete INSTANCE_NAME --zone=us-central1-a --quiet

# Create instance template for managed instance groups
gcloud compute instance-templates create TEMPLATE_NAME \
  --machine-type=e2-medium \
  --image-family=debian-11 \
  --image-project=debian-cloud \
  --boot-disk-size=20GB

# Create managed instance group
gcloud compute instance-groups managed create GROUP_NAME \
  --base-instance-name=INSTANCE_PREFIX \
  --template=TEMPLATE_NAME \
  --size=3 \
  --zone=us-central1-a

# Set autoscaling for managed instance group
gcloud compute instance-groups managed set-autoscaling GROUP_NAME \
  --zone=us-central1-a \
  --min-num-replicas=2 \
  --max-num-replicas=10 \
  --target-cpu-utilization=0.75


################################################################################
# 3. CLOUD RUN DEPLOYMENTS
################################################################################

# Deploy a Cloud Run service from container image
gcloud run deploy SERVICE_NAME \
  --image=gcr.io/PROJECT_ID/IMAGE_NAME:TAG \
  --region=us-central1 \
  --platform=managed

# Deploy with specific memory and CPU limits
gcloud run deploy SERVICE_NAME \
  --image=gcr.io/PROJECT_ID/IMAGE_NAME:TAG \
  --region=us-central1 \
  --platform=managed \
  --memory=512Mi \
  --cpu=1 \
  --max-instances=10 \
  --min-instances=1

# Deploy with environment variables
gcloud run deploy SERVICE_NAME \
  --image=gcr.io/PROJECT_ID/IMAGE_NAME:TAG \
  --region=us-central1 \
  --set-env-vars=KEY1=VALUE1,KEY2=VALUE2

# Deploy with secrets from Secret Manager
gcloud run deploy SERVICE_NAME \
  --image=gcr.io/PROJECT_ID/IMAGE_NAME:TAG \
  --region=us-central1 \
  --set-secrets=DB_PASSWORD=db-password:latest

# Deploy with custom service account
gcloud run deploy SERVICE_NAME \
  --image=gcr.io/PROJECT_ID/IMAGE_NAME:TAG \
  --region=us-central1 \
  --service-account=SERVICE_ACCOUNT_EMAIL

# Deploy with VPC connector (private networking)
gcloud run deploy SERVICE_NAME \
  --image=gcr.io/PROJECT_ID/IMAGE_NAME:TAG \
  --region=us-central1 \
  --vpc-connector=CONNECTOR_NAME \
  --vpc-egress=private-ranges-only

# Allow unauthenticated access (public)
gcloud run services add-iam-policy-binding SERVICE_NAME \
  --region=us-central1 \
  --member="allUsers" \
  --role="roles/run.invoker"

# List all Cloud Run services
gcloud run services list

# Get service details
gcloud run services describe SERVICE_NAME --region=us-central1

# View service URL
gcloud run services describe SERVICE_NAME \
  --region=us-central1 \
  --format='value(status.url)'

# Update service with new image
gcloud run services update SERVICE_NAME \
  --region=us-central1 \
  --image=gcr.io/PROJECT_ID/IMAGE_NAME:NEW_TAG

# Set traffic to specific revision (blue-green deployment)
gcloud run services update-traffic SERVICE_NAME \
  --region=us-central1 \
  --to-revisions=REVISION_1=50,REVISION_2=50

# View service logs
gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=SERVICE_NAME" \
  --limit=50 \
  --format=json

# Delete a service [DESTRUCTIVE]
gcloud run services delete SERVICE_NAME --region=us-central1 --quiet

# Create Cloud Run Job (non-HTTP workload)
gcloud run jobs create JOB_NAME \
  --image=gcr.io/PROJECT_ID/IMAGE_NAME:TAG \
  --region=us-central1 \
  --tasks=1 \
  --max-retries=3

# Execute a Cloud Run Job
gcloud run jobs execute JOB_NAME --region=us-central1


################################################################################
# 4. GKE CLUSTER MANAGEMENT
################################################################################

# Create GKE Autopilot cluster (fully managed)
gcloud container clusters create-auto CLUSTER_NAME \
  --region=us-central1

# Create GKE Standard cluster (more control)
gcloud container clusters create CLUSTER_NAME \
  --zone=us-central1-a \
  --num-nodes=3 \
  --machine-type=e2-medium \
  --disk-size=50 \
  --enable-autoscaling \
  --min-nodes=2 \
  --max-nodes=10

# Create private GKE cluster
gcloud container clusters create CLUSTER_NAME \
  --zone=us-central1-a \
  --enable-private-nodes \
  --enable-private-endpoint \
  --master-ipv4-cidr=172.16.0.0/28 \
  --enable-ip-alias

# Create GKE cluster with Workload Identity
gcloud container clusters create CLUSTER_NAME \
  --zone=us-central1-a \
  --workload-pool=PROJECT_ID.svc.id.goog \
  --enable-stackdriver-kubernetes

# List all clusters
gcloud container clusters list

# Get cluster details
gcloud container clusters describe CLUSTER_NAME --zone=us-central1-a

# Get cluster credentials (configures kubectl)
gcloud container clusters get-credentials CLUSTER_NAME \
  --zone=us-central1-a

# Get credentials for regional cluster
gcloud container clusters get-credentials CLUSTER_NAME \
  --region=us-central1

# Resize cluster node pool
gcloud container clusters resize CLUSTER_NAME \
  --zone=us-central1-a \
  --num-nodes=5

# Upgrade cluster to latest version
gcloud container clusters upgrade CLUSTER_NAME \
  --zone=us-central1-a \
  --master \
  --cluster-version=latest

# Upgrade cluster nodes
gcloud container clusters upgrade CLUSTER_NAME \
  --zone=us-central1-a \
  --node-pool=default-pool

# Create additional node pool
gcloud container node-pools create POOL_NAME \
  --cluster=CLUSTER_NAME \
  --zone=us-central1-a \
  --machine-type=e2-standard-4 \
  --num-nodes=3 \
  --enable-autoscaling \
  --min-nodes=2 \
  --max-nodes=8

# List node pools
gcloud container node-pools list --cluster=CLUSTER_NAME --zone=us-central1-a

# Delete node pool [DESTRUCTIVE]
gcloud container node-pools delete POOL_NAME \
  --cluster=CLUSTER_NAME \
  --zone=us-central1-a \
  --quiet

# Delete cluster [DESTRUCTIVE]
gcloud container clusters delete CLUSTER_NAME --zone=us-central1-a --quiet


################################################################################
# 5. CLOUD SQL OPERATIONS
################################################################################

# Create PostgreSQL instance
gcloud sql instances create INSTANCE_NAME \
  --database-version=POSTGRES_15 \
  --tier=db-f1-micro \
  --region=us-central1

# Create PostgreSQL instance with high availability
gcloud sql instances create INSTANCE_NAME \
  --database-version=POSTGRES_15 \
  --tier=db-custom-2-7680 \
  --region=us-central1 \
  --availability-type=REGIONAL \
  --backup-start-time=03:00

# Create MySQL instance
gcloud sql instances create INSTANCE_NAME \
  --database-version=MYSQL_8_0 \
  --tier=db-n1-standard-1 \
  --region=us-central1

# List all Cloud SQL instances
gcloud sql instances list

# Get instance details
gcloud sql instances describe INSTANCE_NAME

# Set root password
gcloud sql users set-password root \
  --host=% \
  --instance=INSTANCE_NAME \
  --password=PASSWORD

# Create database
gcloud sql databases create DATABASE_NAME \
  --instance=INSTANCE_NAME

# List databases
gcloud sql databases list --instance=INSTANCE_NAME

# Create database user
gcloud sql users create USERNAME \
  --instance=INSTANCE_NAME \
  --password=PASSWORD

# List users
gcloud sql users list --instance=INSTANCE_NAME

# Connect to instance (requires Cloud SQL Proxy or whitelisted IP)
gcloud sql connect INSTANCE_NAME \
  --user=postgres

# Create on-demand backup
gcloud sql backups create \
  --instance=INSTANCE_NAME

# List backups
gcloud sql backups list --instance=INSTANCE_NAME

# Restore from backup
gcloud sql backups restore BACKUP_ID \
  --backup-instance=SOURCE_INSTANCE \
  --backup-id=BACKUP_ID

# Export database to Cloud Storage
gcloud sql export sql INSTANCE_NAME \
  gs://BUCKET_NAME/backup.sql \
  --database=DATABASE_NAME

# Import database from Cloud Storage
gcloud sql import sql INSTANCE_NAME \
  gs://BUCKET_NAME/backup.sql \
  --database=DATABASE_NAME

# Stop instance (save costs)
gcloud sql instances patch INSTANCE_NAME --activation-policy=NEVER

# Start instance
gcloud sql instances patch INSTANCE_NAME --activation-policy=ALWAYS

# Delete instance [DESTRUCTIVE]
gcloud sql instances delete INSTANCE_NAME --quiet


################################################################################
# 6. IAM AND SERVICE ACCOUNTS
################################################################################

# List IAM policy for project
gcloud projects get-iam-policy PROJECT_ID

# Grant role to user at project level
gcloud projects add-iam-policy-binding PROJECT_ID \
  --member="user:EMAIL@example.com" \
  --role="roles/viewer"

# Grant role to service account
gcloud projects add-iam-policy-binding PROJECT_ID \
  --member="serviceAccount:SERVICE_ACCOUNT_EMAIL" \
  --role="roles/storage.objectViewer"

# Grant role to group
gcloud projects add-iam-policy-binding PROJECT_ID \
  --member="group:GROUP_EMAIL@example.com" \
  --role="roles/editor"

# Remove role from member [DESTRUCTIVE]
gcloud projects remove-iam-policy-binding PROJECT_ID \
  --member="user:EMAIL@example.com" \
  --role="roles/viewer"

# Create service account
gcloud iam service-accounts create SERVICE_ACCOUNT_NAME \
  --display-name="Service Account Display Name" \
  --description="Service account for APPLICATION_NAME"

# List service accounts
gcloud iam service-accounts list

# Get service account details
gcloud iam service-accounts describe SERVICE_ACCOUNT_EMAIL

# Grant IAM role to service account
gcloud projects add-iam-policy-binding PROJECT_ID \
  --member="serviceAccount:SERVICE_ACCOUNT_EMAIL" \
  --role="roles/storage.admin"

# Create service account key [SECURITY RISK - use Workload Identity instead]
gcloud iam service-accounts keys create key.json \
  --iam-account=SERVICE_ACCOUNT_EMAIL

# List service account keys
gcloud iam service-accounts keys list \
  --iam-account=SERVICE_ACCOUNT_EMAIL

# Delete service account key [DESTRUCTIVE]
gcloud iam service-accounts keys delete KEY_ID \
  --iam-account=SERVICE_ACCOUNT_EMAIL

# Enable IAM policy binding on service account (impersonation)
gcloud iam service-accounts add-iam-policy-binding SERVICE_ACCOUNT_EMAIL \
  --member="user:EMAIL@example.com" \
  --role="roles/iam.serviceAccountTokenCreator"

# List all available IAM roles
gcloud iam roles list

# Describe specific role
gcloud iam roles describe roles/storage.admin

# Test IAM permissions
gcloud projects test-iam-permissions PROJECT_ID \
  --permissions=compute.instances.list,storage.buckets.list

# Delete service account [DESTRUCTIVE]
gcloud iam service-accounts delete SERVICE_ACCOUNT_EMAIL --quiet


################################################################################
# 7. NETWORKING (VPC, FIREWALL RULES)
################################################################################

# List VPC networks
gcloud compute networks list

# Create custom VPC network
gcloud compute networks create NETWORK_NAME \
  --subnet-mode=custom

# Create subnet
gcloud compute networks subnets create SUBNET_NAME \
  --network=NETWORK_NAME \
  --region=us-central1 \
  --range=10.0.0.0/24

# List subnets
gcloud compute networks subnets list

# List firewall rules
gcloud compute firewall-rules list

# Create firewall rule (allow HTTP)
gcloud compute firewall-rules create allow-http \
  --network=NETWORK_NAME \
  --allow=tcp:80 \
  --source-ranges=0.0.0.0/0 \
  --target-tags=http-server

# Create firewall rule (allow HTTPS)
gcloud compute firewall-rules create allow-https \
  --network=NETWORK_NAME \
  --allow=tcp:443 \
  --source-ranges=0.0.0.0/0 \
  --target-tags=https-server

# Create firewall rule (allow SSH from specific IPs)
gcloud compute firewall-rules create allow-ssh \
  --network=NETWORK_NAME \
  --allow=tcp:22 \
  --source-ranges=203.0.113.0/24

# Create firewall rule (allow internal traffic)
gcloud compute firewall-rules create allow-internal \
  --network=NETWORK_NAME \
  --allow=tcp:0-65535,udp:0-65535,icmp \
  --source-ranges=10.0.0.0/8

# Update firewall rule
gcloud compute firewall-rules update RULE_NAME \
  --source-ranges=0.0.0.0/0

# Describe firewall rule
gcloud compute firewall-rules describe RULE_NAME

# Delete firewall rule [DESTRUCTIVE]
gcloud compute firewall-rules delete RULE_NAME --quiet

# List static external IP addresses
gcloud compute addresses list

# Reserve static external IP address
gcloud compute addresses create ADDRESS_NAME \
  --region=us-central1

# Reserve global static IP (for load balancer)
gcloud compute addresses create ADDRESS_NAME --global

# Release static IP [DESTRUCTIVE]
gcloud compute addresses delete ADDRESS_NAME --region=us-central1 --quiet

# Create VPC peering
gcloud compute networks peerings create PEERING_NAME \
  --network=NETWORK_NAME \
  --peer-network=PEER_NETWORK_NAME

# List VPC peerings
gcloud compute networks peerings list --network=NETWORK_NAME

# Create Cloud Router (for Cloud NAT)
gcloud compute routers create ROUTER_NAME \
  --network=NETWORK_NAME \
  --region=us-central1

# Create Cloud NAT (for outbound internet from private instances)
gcloud compute routers nats create NAT_NAME \
  --router=ROUTER_NAME \
  --region=us-central1 \
  --auto-allocate-nat-external-ips \
  --nat-all-subnet-ip-ranges

# List Cloud Routers
gcloud compute routers list

# Create VPN tunnel
gcloud compute vpn-tunnels create TUNNEL_NAME \
  --peer-address=PEER_IP \
  --shared-secret=SECRET \
  --target-vpn-gateway=GATEWAY_NAME \
  --region=us-central1


################################################################################
# 8. CLOUD STORAGE OPERATIONS
################################################################################

# Note: Most Cloud Storage operations use 'gsutil' instead of 'gcloud'

# Create bucket
gsutil mb gs://BUCKET_NAME

# Create bucket with specific location and storage class
gsutil mb -l us-central1 -c STANDARD gs://BUCKET_NAME

# List buckets
gsutil ls

# List objects in bucket
gsutil ls gs://BUCKET_NAME

# List objects recursively
gsutil ls -r gs://BUCKET_NAME/**

# Upload file to bucket
gsutil cp LOCAL_FILE gs://BUCKET_NAME/

# Upload directory recursively
gsutil cp -r LOCAL_DIR gs://BUCKET_NAME/

# Download file from bucket
gsutil cp gs://BUCKET_NAME/OBJECT_NAME ./LOCAL_PATH

# Download directory recursively
gsutil cp -r gs://BUCKET_NAME/PREFIX ./LOCAL_PATH

# Sync local directory with bucket (like rsync)
gsutil rsync -r LOCAL_DIR gs://BUCKET_NAME/

# Move/rename object
gsutil mv gs://BUCKET_NAME/OLD_NAME gs://BUCKET_NAME/NEW_NAME

# Copy object to another bucket
gsutil cp gs://SOURCE_BUCKET/OBJECT gs://DEST_BUCKET/

# Delete object
gsutil rm gs://BUCKET_NAME/OBJECT_NAME

# Delete all objects with prefix
gsutil rm -r gs://BUCKET_NAME/PREFIX/**

# View object metadata
gsutil stat gs://BUCKET_NAME/OBJECT_NAME

# Make object publicly readable
gsutil acl ch -u AllUsers:R gs://BUCKET_NAME/OBJECT_NAME

# Make bucket publicly readable (all objects)
gsutil iam ch allUsers:objectViewer gs://BUCKET_NAME

# Set bucket lifecycle policy
gsutil lifecycle set lifecycle.json gs://BUCKET_NAME

# Example lifecycle.json for transitioning to Coldline after 90 days:
# {
#   "rule": [
#     {
#       "action": {"type": "SetStorageClass", "storageClass": "COLDLINE"},
#       "condition": {"age": 90}
#     }
#   ]
# }

# Enable versioning
gsutil versioning set on gs://BUCKET_NAME

# View bucket IAM policy
gsutil iam get gs://BUCKET_NAME

# Grant IAM role on bucket
gsutil iam ch serviceAccount:SERVICE_ACCOUNT_EMAIL:objectViewer gs://BUCKET_NAME

# Remove IAM role on bucket
gsutil iam ch -d serviceAccount:SERVICE_ACCOUNT_EMAIL:objectViewer gs://BUCKET_NAME

# Set CORS policy on bucket
gsutil cors set cors.json gs://BUCKET_NAME

# Example cors.json:
# [
#   {
#     "origin": ["https://example.com"],
#     "method": ["GET", "POST"],
#     "responseHeader": ["Content-Type"],
#     "maxAgeSeconds": 3600
#   }
# ]

# Delete bucket (must be empty) [DESTRUCTIVE]
gsutil rb gs://BUCKET_NAME


################################################################################
# 9. BIGQUERY OPERATIONS
################################################################################

# Note: BigQuery operations use 'bq' CLI tool

# List datasets
bq ls

# List datasets in specific project
bq ls --project_id=PROJECT_ID

# Create dataset
bq mk DATASET_NAME

# Create dataset with specific location
bq mk --location=US DATASET_NAME

# Create dataset with expiration (90 days)
bq mk --default_table_expiration 7776000 DATASET_NAME

# List tables in dataset
bq ls DATASET_NAME

# Show table schema
bq show DATASET_NAME.TABLE_NAME

# Show table details (schema, size, rows)
bq show --schema --format=prettyjson DATASET_NAME.TABLE_NAME

# Run query
bq query --use_legacy_sql=false 'SELECT * FROM `project.dataset.table` LIMIT 10'

# Run query and save results to table
bq query --use_legacy_sql=false --destination_table=DATASET.RESULT_TABLE \
  'SELECT * FROM `project.dataset.table` WHERE column = "value"'

# Load CSV data into table
bq load --source_format=CSV DATASET.TABLE_NAME gs://BUCKET/file.csv schema.json

# Load JSON data into table
bq load --source_format=NEWLINE_DELIMITED_JSON \
  DATASET.TABLE_NAME gs://BUCKET/file.json schema.json

# Load data with auto-detect schema
bq load --autodetect --source_format=CSV DATASET.TABLE_NAME gs://BUCKET/file.csv

# Export table to Cloud Storage
bq extract DATASET.TABLE_NAME gs://BUCKET/export.csv

# Export table as JSON
bq extract --destination_format=NEWLINE_DELIMITED_JSON \
  DATASET.TABLE_NAME gs://BUCKET/export.json

# Copy table
bq cp DATASET.SOURCE_TABLE DATASET.DEST_TABLE

# Create table from query results
bq query --use_legacy_sql=false --destination_table=DATASET.NEW_TABLE \
  'SELECT * FROM `project.dataset.table` WHERE date > "2024-01-01"'

# Create partitioned table (by date)
bq mk --table --time_partitioning_field=date \
  DATASET.TABLE_NAME schema.json

# Create clustered table
bq mk --table --clustering_fields=field1,field2 \
  DATASET.TABLE_NAME schema.json

# Update table schema
bq update DATASET.TABLE_NAME schema.json

# Delete table [DESTRUCTIVE]
bq rm -t DATASET.TABLE_NAME

# Delete dataset and all tables [DESTRUCTIVE]
bq rm -r -d DATASET_NAME

# Show running jobs
bq ls -j

# Cancel running job
bq cancel JOB_ID

# View job details
bq show -j JOB_ID

# Estimate query cost (dry run)
bq query --dry_run --use_legacy_sql=false \
  'SELECT * FROM `project.dataset.large_table`'


################################################################################
# 10. ADDITIONAL USEFUL COMMANDS
################################################################################

# View audit logs
gcloud logging read "protoPayload.serviceName=compute.googleapis.com" \
  --limit=50 \
  --format=json

# View logs for specific resource
gcloud logging read "resource.type=gce_instance AND resource.labels.instance_id=INSTANCE_ID" \
  --limit=50

# Create log sink (export to Cloud Storage)
gcloud logging sinks create SINK_NAME \
  gs://BUCKET_NAME \
  --log-filter='resource.type="gce_instance"'

# List log sinks
gcloud logging sinks list

# View Cloud Monitoring metrics
gcloud monitoring time-series list \
  --filter='metric.type="compute.googleapis.com/instance/cpu/utilization"'

# Create uptime check
gcloud monitoring uptime-checks create UPTIME_CHECK_NAME \
  --resource-type=uptime-url \
  --host=example.com

# List Secret Manager secrets
gcloud secrets list

# Create secret
echo -n "secret-value" | gcloud secrets create SECRET_NAME --data-file=-

# Access secret value
gcloud secrets versions access latest --secret=SECRET_NAME

# Add new secret version
echo -n "new-secret-value" | gcloud secrets versions add SECRET_NAME --data-file=-

# Grant access to secret
gcloud secrets add-iam-policy-binding SECRET_NAME \
  --member="serviceAccount:SERVICE_ACCOUNT_EMAIL" \
  --role="roles/secretmanager.secretAccessor"

# List operations (long-running tasks)
gcloud compute operations list

# View quota usage
gcloud compute project-info describe --project=PROJECT_ID

# Enable organization policies
gcloud resource-manager org-policies describe POLICY_NAME \
  --project=PROJECT_ID


################################################################################
# 11. HELPFUL TIPS AND FLAG COMBINATIONS
################################################################################

# Use --format flag for custom output (json, yaml, csv, table)
gcloud compute instances list --format=json
gcloud compute instances list --format="table(name,zone,machineType,status)"
gcloud compute instances list --format="csv(name,zone,status)"

# Use --filter flag for filtering results
gcloud compute instances list --filter="zone:us-central1-a"
gcloud compute instances list --filter="status=RUNNING"
gcloud compute instances list --filter="name:prod-*"

# Combine filter and format
gcloud compute instances list \
  --filter="status=RUNNING AND zone:us-central1" \
  --format="table(name,zone,machineType)"

# Use --quiet or -q to skip confirmation prompts (useful for scripts)
gcloud compute instances delete INSTANCE_NAME --zone=us-central1-a --quiet

# Use --project flag to specify project (override current config)
gcloud compute instances list --project=OTHER_PROJECT_ID

# Get help for any command
gcloud compute instances create --help
gcloud run deploy --help

# Check version
gcloud version

# Update gcloud CLI
gcloud components update

# List installed components
gcloud components list

# Install additional components
gcloud components install kubectl
gcloud components install beta
gcloud components install alpha

# Use beta or alpha commands for preview features
gcloud beta compute instances create INSTANCE_NAME ...
gcloud alpha run services update SERVICE_NAME ...

# Authenticate with service account key (CI/CD pipelines)
gcloud auth activate-service-account --key-file=key.json

# Switch between configurations (useful for multiple projects/accounts)
gcloud config configurations create CONFIG_NAME
gcloud config configurations activate CONFIG_NAME
gcloud config configurations list

# Set properties in current configuration
gcloud config set project PROJECT_ID
gcloud config set compute/region us-central1
gcloud config set compute/zone us-central1-a

# Unset properties
gcloud config unset project


################################################################################
# 12. COMMON WORKFLOWS
################################################################################

# Deploy containerized app to Cloud Run (complete workflow)
# 1. Build container
gcloud builds submit --tag gcr.io/PROJECT_ID/IMAGE_NAME:TAG

# 2. Deploy to Cloud Run
gcloud run deploy SERVICE_NAME \
  --image gcr.io/PROJECT_ID/IMAGE_NAME:TAG \
  --region us-central1 \
  --platform managed \
  --allow-unauthenticated

# 3. Get service URL
gcloud run services describe SERVICE_NAME \
  --region=us-central1 \
  --format='value(status.url)'


# Set up private GKE cluster with Cloud SQL (complete workflow)
# 1. Create VPC network
gcloud compute networks create gke-network --subnet-mode=custom

# 2. Create subnet
gcloud compute networks subnets create gke-subnet \
  --network=gke-network \
  --region=us-central1 \
  --range=10.0.0.0/24

# 3. Create GKE cluster
gcloud container clusters create gke-cluster \
  --region=us-central1 \
  --network=gke-network \
  --subnetwork=gke-subnet \
  --enable-private-nodes \
  --enable-ip-alias \
  --workload-pool=PROJECT_ID.svc.id.goog

# 4. Create Cloud SQL instance
gcloud sql instances create db-instance \
  --database-version=POSTGRES_15 \
  --tier=db-custom-2-7680 \
  --region=us-central1 \
  --network=gke-network

# 5. Get credentials
gcloud container clusters get-credentials gke-cluster --region=us-central1


# Create load balanced web service (complete workflow)
# 1. Create instance template
gcloud compute instance-templates create web-template \
  --machine-type=e2-medium \
  --image-family=debian-11 \
  --image-project=debian-cloud \
  --tags=http-server \
  --metadata-from-file=startup-script=startup.sh

# 2. Create managed instance group
gcloud compute instance-groups managed create web-group \
  --base-instance-name=web \
  --template=web-template \
  --size=3 \
  --region=us-central1

# 3. Set named port
gcloud compute instance-groups managed set-named-ports web-group \
  --region=us-central1 \
  --named-ports=http:80

# 4. Create health check
gcloud compute health-checks create http web-health-check \
  --port=80 \
  --request-path=/

# 5. Create backend service
gcloud compute backend-services create web-backend \
  --protocol=HTTP \
  --health-checks=web-health-check \
  --global

# 6. Add instance group to backend
gcloud compute backend-services add-backend web-backend \
  --instance-group=web-group \
  --instance-group-region=us-central1 \
  --global

# 7. Create URL map
gcloud compute url-maps create web-map \
  --default-service=web-backend

# 8. Create target HTTP proxy
gcloud compute target-http-proxies create web-proxy \
  --url-map=web-map

# 9. Create forwarding rule
gcloud compute forwarding-rules create web-forwarding-rule \
  --global \
  --target-http-proxy=web-proxy \
  --ports=80


################################################################################
# END OF GCLOUD CLI REFERENCE
################################################################################
#
# For more information:
# - gcloud CLI reference: https://cloud.google.com/sdk/gcloud/reference
# - Best practices: https://cloud.google.com/sdk/gcloud/reference/topic/startup
# - Scripting guide: https://cloud.google.com/sdk/docs/scripting-gcloud
#
################################################################################
