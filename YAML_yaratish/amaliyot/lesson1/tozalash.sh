#!/usr/bin/env bash
# YAML_yaratish bo'limida yaratilgan obyektlarni o'chiradi.
set -euo pipefail
kubectl delete -f 02-service.yaml --ignore-not-found
kubectl delete -f 01-deployment.yaml --ignore-not-found
echo "Tozalandi."
