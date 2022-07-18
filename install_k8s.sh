#!/usr/bin/env sh
minikube start --kubernetes-version=v1.20.0 --memory 16384 --cpus 6
curl -s "https://raw.githubusercontent.com/kserve/kserve/release-0.8/hack/quick_install.sh" | bash

echo "Create namespace"
kubectl create namespace kserve-test

RUNTIME=docker

eval $(minikube docker-env)
$RUNTIME build -t ruivieira/kserve-trustyai-explainer:latest -f explainer.Dockerfile .

echo "Deploy inference service"
kubectl apply -f k8s/inference-service.yaml

export SERVICE_HOSTNAME=$(kubectl get inferenceservice income -n default -o jsonpath='{.status.url}' | cut -d "/" -f 3)
export INGRESS_HOST=$(kubectl -n istio-system get service istio-ingressgateway -o jsonpath='{.status.loadBalancer.ingress[0].ip}')
export INGRESS_PORT=$(kubectl -n istio-system get service istio-ingressgateway -o jsonpath='{.spec.ports[?(@.name=="http2")].port}')
export MODEL_NAME=income
export INGRESS_GATEWAY=istio-ingressgateway
export CLUSTER_IP=$(kubectl -n istio-system get service $INGRESS_GATEWAY -o jsonpath='{.status.loadBalancer.ingress[0].ip}')
