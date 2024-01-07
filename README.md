RAFT Chat bot
=============

This bot is a simple chatbot that can answer questions about RAFT projects.

RAFT marketing [presentations](https://space.raftds.com/apps/files/?dir=/Raft%20Marketing&fileid=8651)

frameworks: LangChain and RAG. 

UseCase
1. chatbot should be able to answer about RAFT projects
2. chatbot should be able to give a detailed answer about specific RAFT project


## Installation

### General 
You should copy ./deployment/.env.example to ./deployment/.env and fill it with your data.  
You need to install kubectl, gcloud, terraform, docker, minikube

### Local
You should use minikube for local development. Also, you need to use Elastic instance somewhere and fill .env variable
Deployment scripts located in `./scripts/local/deploy.sh` folder.

### Google Cloud Platform (GCP)
At this moment there is no Terraform+Skaffold scripts for GCP services activating.
You should create Google Cloud Platform project and activate manually:
- Google Kubernetes Engine for AI worker (worker_ai.py), Augmentation worker (worker_aug.py) and FastAPI web project (web.py)
- Google Cloud Storage / Google Cloud Artifact Registry for storing raw data (marketing presentations)
- Google Cloud Artifact Registry for image storing 
- Google Elastic Cloud for artifact storing (parsed data from marketing presentations)
- Google Redis Cloud for tasks queue 
- Google API Gateway for API endpoint

and then you should log in to gcloud, create a credential file `gcloud.json`, put it into ./credentials folder, fill some variable in the .env file and run `./scripts/gcp/deploy.sh` script.