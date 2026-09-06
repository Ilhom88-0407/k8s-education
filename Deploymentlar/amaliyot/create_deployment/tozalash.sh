#!/usr/bin/env bash
# Bu bo'limda yaratilgan obyektlarni o'chiradi.
set -euo pipefail
kubectl delete -f 02-nginx-service.yaml --ignore-not-found
kubectl delete -f 01-nginx-deployment.yaml --ignore-not-found
kubectl delete deployment mashq-deploy --ignore-not-found
echo "Tozalandi."
