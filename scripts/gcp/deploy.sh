#!/usr/bin/env bash

gcloud__sa="raft-marketing-chat-bot-sa@raft-marketing-chat-bot.iam.gserviceaccount.com"
gcloud_project="raft-marketing-chat-bot"
gcloud_region="us-east1"
gcloud_sa_file="./credentials/gcloud.json"
gcloud_cluster="raft-marketing-chat-bot-cluster"

image_path="./deployment/Dockerfile"
image_name="raft-marketing-chat-bot"
image_version="0.1.0"

repo_name="raft-marketing-chat-bot"

generic_image=us-east1-docker.pkg.dev/$gcloud_project/$repo_name/$image_name:$image_version

gcloud auth activate-service-account --key-file=$gcloud_sa_file
#gcloud config set project $gcloud_project
gcloud --quiet config set compute/zone $gcloud_region
gcloud auth configure-docker $gcloud_region-docker.pkg.dev

docker image build \
  --rm \
  --file $image_path \
  --tag $generic_image .

docker push $generic_image

gcloud container clusters get-credentials $gcloud_cluster --region $gcloud_region --project $gcloud_project

kubectl apply -f ./deployment/gcp/namespace.yaml
kubectl apply -f ./deployment/gcp/web.yaml
kubectl apply -f ./deployment/gcp/worker_ai.yaml
kubectl apply -f ./deployment/gcp/worker_aug.yaml
