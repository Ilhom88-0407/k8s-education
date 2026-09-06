#!/usr/bin/env bash
# Bu darsda yaratilgan obyektlarni o'chiradi.
set -euo pipefail
kubectl delete pod sinov-nginx --ignore-not-found
kubectl delete pod mashq-shell --ignore-not-found
echo "Tozalandi."
