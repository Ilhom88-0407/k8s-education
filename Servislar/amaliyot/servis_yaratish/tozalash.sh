#!/usr/bin/env bash
# Servislar bo'limida yaratilgan barcha obyektlarni o'chiradi.
set -euo pipefail
kubectl delete -f 04-loadbalancer.yaml --ignore-not-found
kubectl delete -f 03-nodeport.yaml --ignore-not-found
kubectl delete -f 02-clusterip.yaml --ignore-not-found
kubectl delete -f 01-deployment.yaml --ignore-not-found
kubectl delete service web-mashq --ignore-not-found
echo "Tozalandi."
