#!/usr/bin/env bash
# Bu darsda yaratilgan barcha obyektlarni o'chiradi.
#
# Ishlatish:  bash tozalash.sh
set -euo pipefail

kubectl delete pod oddiy-nginx --ignore-not-found
kubectl delete pod sidecar-namuna --ignore-not-found
kubectl delete pod mashq-pod --ignore-not-found

echo "Tozalandi."
