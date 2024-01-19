# Deployment Process

This section provides step-by-step instructions on deploying the **Pineapple** on Azure Kubernetes Service (AKS).

## 1. Deploying Python Application

### Prerequisites

Before deploying the Python application, ensure the following prerequisites are met:

- Azure CLI is installed.
- Docker is installed.
- kubectl is installed.
- Resource Azure Container Registry.
- Resource Azure Kubernetes Services cluster.

### Steps

1. **Build the Docker Image:**
 Use the following command to build the Docker image for the Pineapple application. This step compiles the application and packages it into a Docker image named `bookstore-app`.

   `docker build -t bookstore-app .`

2. **Tag the Docker Image:**
Tagging associates the local Docker image with the target image repository in Azure Container Registry (ACR). Use the following command to tag the bookstore-app image with the ACR repository information.

   `(docker tag <local_image> <acr_login_server>/<image_name>:<tag>)`
   `docker tag f00eca538ff2 bookstoreapp.azurecr.io/bookstore-app:latest`

3. **Push the Docker Image to Azure Container Registry (ACR):**
Push the bookstore-app Docker image to the Azure Container Registry to make it available for deployment on Azure Kubernetes Service (AKS). Use the following command:

   `(docker push <acr_login_server>/<image_name>:<tag>)`
   `docker push bookstoreapp.azurecr.io/bookstore-app:latest`

4. **Authenticate Docker with ACR:**
Before deploying the application to AKS, authenticate Docker with the Azure Container Registry to enable seamless image pulling and pushing. Use the following command:

   `(az acr login --name <acr-name>)`
   `az acr login --name bookstoreapp.azurecr.io`

5. **Deploy the Application to AKS:**
Deploy the Pineapple application on Azure Kubernetes Service (AKS) using the Kubernetes deployment configuration provided in kubernetes/deployment.yaml. Apply the configuration with the following command:
   `kubectl apply -f myapp-deployment.yaml`

6. **Adding Service for the Web Application to AKS:**
The Service YAML is necessary to expose your application within the Kubernetes cluster and make it accessible to other services or external clients. The Service acts as a stable endpoint with a well-defined IP address and port, allowing other pods or external users to connect to your application.
   `kubectl apply -f myapp-service.yaml`

7. **Attach an ACR to an existing AKS cluster:**
Integrate an existing ACR with an existing AKS cluster using the az aks update command with the --attach-acr parameter and a valid value for acr-name or acr-resource-id. This is crucial because even if you give AcrPull role for your user, sometimes it may not be enough to authenticate for using that ACR.
   `az aks update -n <myAKSCluster> -g <myResourceGroup> --attach-acr <acr-name>`

### Checking the status of application
After we deploy the application, we need to check the status of the service and pods. We can both check it either with Azure Portal or kubectl. For example:
![image.png](/.attachments/image-f833661d-31b6-48f2-96cb-7a0692cc5e3a.png)
Everybody can reach the app with this external-ip `104.42.55.31` via passing into url (such as  http://104.42.55.31/books). 


### Using the application externally
We can use the app externally and access the endpoint for getting all books with following url endpoint: http://104.42.55.31/books, the result concludes that our app is working globally without an issue.

For example we can use the following url to get specific book with hitting the getbyid endpoint:
http://104.42.55.31/books/659829f3a5e6cecfe3f85308
![Ekran Resmi 2024-01-10 20.38.39.png](/.attachments/Ekran%20Resmi%202024-01-10%2020.38.39-020c0f63-17d0-4f00-8619-5d29ea955364.png)
# 2. Deploying MongoDB on AKS

This document provides an overview of the MongoDB deployment in the Kubernetes cluster. MongoDB is a NoSQL database used to store and manage data for the application. In this deployment, Cosmos DB is utilized as the backend to provide globally distributed, multi-model database services. So first we need to create CosmosDB with MongoDB API resource instance under our resource group.

# Deployment Components

## Steps

1. **StatefulSet**
The MongoDB deployment is managed by a StatefulSet named my-mongodb. The StatefulSet ensures stable and unique network identities for each MongoDB pod.
`kubectl apply -f my-mongodb-statefulset.yaml`
2. **ConfigMap**
The ConfigMap my-mongodb-config contains the configuration data for MongoDB, including the connection string and other relevant settings.
`kubectl apply -f my-mongodb-config.yaml`
3. **Service**
A Kubernetes Service named my-mongodb-service exposes the MongoDB deployment within the cluster. This service allows other components to discover and communicate with the MongoDB instances.
`kubectl apply -f my-mongodb-service.yaml`

##Cosmos DB Integration
Cosmos DB is utilized as the backend for MongoDB. The MongoDB connection string includes the Cosmos DB details. After we created a CosmosDB with MongoDB API resource instance we can use its connection string.
![image.png](/.attachments/image-180195fc-a7c3-40a0-9057-a18f5f6d3747.png)
 
In the application we will use this connection string to reach to MongoDB client, for python:

![Ekran Resmi 2024-01-10 22.52.57.png](/.attachments/Ekran%20Resmi%202024-01-10%2022.52.57-f9cce27b-de7b-463f-b1ad-e6d7f711ee97.png)



##Checking the status of the CosmosDB with MongoDB API instance and accessing it globally.

![image.png](/.attachments/image-4b2cf75f-d0de-446f-936a-14960778c02b.png)

After we see it running, we can reach it with username and secret that CosmosDB provide for us:

![image.png](/.attachments/image-fc104b76-4017-4f05-944d-a74270aeecbf.png)

Then we can run this code:

`mongosh "mongodb://<username>:<password>@<your-cosmosdb-name>.mongo.cosmos.azure.com:10255/<your-database>?ssl=true"`

So when we do this we will be inside of the database.

![image.png](/.attachments/image-e0793698-f1fd-4949-909c-b749571ac49d.png)














