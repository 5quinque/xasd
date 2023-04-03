#/bin/bash -e

# This script is used to deploy the application to a kubernetes cluster.

# The script assumes that the kubernetes cluster is already running and
# the kubectl command is configured to connect to the cluster.

# The script also assumes that the docker image has already been built
# and pushed to a docker registry with the tag "latest".

# The script will create a deployment and a service for the application.
# The script will also create a configmap for the application configuration.
# The script will also create a secret for the database password.

# build image
# docker build --tag xasd .
# docker tag xasd registry.digitalocean.com/xasd/xasd
# docker push registry.digitalocean.com/xasd/xasd


# api

# Create the secret.
kubectl apply -f deployment-resources/api/api-secret.yaml

# Create the configmap.
kubectl apply -f deployment-resources/api/api-configmap.yaml

# Create the deployment.
kubectl apply -f deployment-resources/api/api-deployment.yaml

# Create the service.
kubectl apply -f deployment-resources/api/api-service.yaml

# mariadb

# Create the secret.
kubectl apply -f deployment-resources/mariadb/mariadb-secret.yaml

# Create the configmap.
kubectl apply -f deployment-resources/mariadb/mariadb-configmap.yaml

# Create the statefulset.
kubectl apply -f deployment-resources/mariadb/mariadb-statefulset.yaml

# Create the service.
kubectl apply -f deployment-resources/mariadb/mariadb-service.yaml

# teardown

# kubectl delete -f deployment-resources/api/api-deployment.yaml
# kubectl delete -f deployment-resources/api/api-service.yaml
# kubectl delete -f deployment-resources/api/api-configmap.yaml
# kubectl delete -f deployment-resources/api/api-secret.yaml
# kubectl delete -f deployment-resources/mariadb/mariadb-statefulset.yaml
# kubectl delete -f deployment-resources/mariadb/mariadb-service.yaml
# kubectl delete -f deployment-resources/mariadb/mariadb-configmap.yaml
# kubectl delete -f deployment-resources/mariadb/mariadb-secret.yaml
