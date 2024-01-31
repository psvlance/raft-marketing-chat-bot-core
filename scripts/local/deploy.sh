#!/usr/bin/env bash

image_path="./deployment/Dockerfile"
image_name="raft-marketing-chat-bot"
image_version="0.1.0"
generic_image=$image_name:$image_version
minikube_profile="raft-marketing-chat-bot"
local_path=`pwd`

source deployment/scripts/local/.env

#minikube -p "${minikube_profile}" image load "${generic_image}" --daemon=true

minikube start -p ${minikube_profile} --cpus=2 --memory=4096m --driver=docker --kubernetes-version=v1.21.2 \
    --mount=true --mount-string="${local_path}/raft-marketing-chat-bot/src/:/raft-marketing-chat-bot"

eval $(minikube docker-env -p ${minikube_profile})
docker image build --rm --file $image_path --tag $generic_image .

kubectl apply -f ./deployment/local/redis.yaml
kubectl apply -f ./deployment/local/web.yaml
kubectl apply -f ./deployment/local/worker_ai.yaml
kubectl apply -f ./deployment/local/worker_aug.yaml

minikube -p ${minikube_profile} service raft-marketing-chat-bot-web-service --url
minikube -p ${minikube_profile} dashboard
