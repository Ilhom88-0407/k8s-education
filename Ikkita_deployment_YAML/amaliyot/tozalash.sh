#!/usr/bin/env bash
# Ikkala deployment va servisni o'chiradi.
set -euo pipefail
kubectl delete -f 02-k8s-web-to-nginx.yaml --ignore-not-found
kubectl delete -f 01-nginx.yaml --ignore-not-found
echo "Tozalandi."
