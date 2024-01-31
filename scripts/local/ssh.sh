#!/usr/bin/env bash

minikube_profile="raft-marketing-chat-bot"

source deployment/scripts/local/.env

minikube ssh \
    -p ${minikube_profile} \
    $@
