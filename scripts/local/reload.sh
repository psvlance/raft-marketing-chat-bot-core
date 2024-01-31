#!/usr/bin/env bash

source deployment/scripts/local/.env

kubectl apply -f ./deployment/local/web.yaml
kubectl apply -f ./deployment/local/worker_ai.yaml
kubectl apply -f ./deployment/local/worker_aug.yaml
