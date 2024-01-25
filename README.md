# Project Documentation

Welcome to the documentation for the **Pineapple**. This documentation provides comprehensive information about the setup, deployment, and maintenance of the project components on the Azure cloud platform.

## Overview

- **Project Title:** Building and Deploying a Containerized Python Application with Flask and MongoDB on
Azure Kubernetes Service (AKS)
- **Objective:** The goal of this assignment is to create a scalable and containerized Python and Flask
application that interacts with a MongoDB database and deploy the application on Azure Kubernetes
Service (AKS)
- **Key Technologies:**
  - Python
  - Flask
  - MongoDB
  - Docker
  - Azure Kubernetes Service (AKS)
  - Azure CosmosDB

## Sections

1. **Project Components:**
   - Overview of the key components in the project, including the Python application, MongoDB setup, Docker containerization, and Azure Kubernetes Service.

2. **Deployment Process:**
   - Detailed instructions on deploying the Python application and MongoDB on Azure Kubernetes Service (AKS).

# Project Components

This section provides an overview of the key components in the **Pineapple**.

## 1. Python Application

### Overview

The Python application in this project serves as web application. It's including CRUD operations for `PineappleDB` database and `bookstore` collection with using MongoDB. The application is built using `flask`,`pymongo`.

Base URL

The API is accessible at http://104.42.55.31:5009.

#Endpoints
**1. Create Book**

**Endpoint**: POST /books
**Description**: Creates a new book entry in the bookstore database.
**Payload**:

_JSON format with the following required fields:
isbn: International Standard Book Number.
title: Title of the book.
year: Year of publication.
price: Price of the book.
page: Number of pages in the book.
category: Category or genre of the book.
coverPhoto: URL or file path of the book cover photo.
publisher: Publisher of the book.
author: Author of the book._

**Example Usage:**
`curl -X POST -H "Content-Type: application/json" -d '{"isbn":"1234567890", "title":"Sample Book", "year":2022, "price":19.99, "page":300, "category":"Fiction", "coverPhoto":"http://example.com/cover.jpg", "publisher":"Publisher Name", "author":"Author Name"}' http://104.42.55.31:5009/books`

**2. Get All Books**

**Endpoint**: GET /books
**Description**: Retrieves all books from the bookstore database.
**Example Usage:**
`curl http://104.42.55.31:5009/books`

**3. Get Book by ID**

**Endpoint**: GET /books/<string:book_id>
**Description**: Retrieves a specific book by its unique identifier.
**Example Usage:**
`curl http://104.42.55.31:5009/books/60f3c96a370efc3fdcc5f0fb`

**4. Delete Book by ID**

**Endpoint**: DELETE /books/<string:book_id>
**Description**: Deletes a specific book by its unique identifier.
**Example Usage:**

`curl -X DELETE http://104.42.55.31:5009/books/60f3c96a370efc3fdcc5f0fb`

**5. Update Book by ID**

**Endpoint**: PUT /books/<string:book_id>
**Description**: Updates a specific book's information by its unique identifier.
**Payload**:
JSON format with the same required fields as in the create book endpoint.
**Example Usage:**
`curl -X PUT -H "Content-Type: application/json" -d '{"isbn":"1234567890", "title":"Updated Book Title", "year":2022, "price":24.99, "page":350, "category":"Fiction", "coverPhoto":"http://example.com/updated_cover.jpg", "publisher":"Updated Publisher Name", "author":"Updated Author Name"}' http://104.42.55.31:5009/books/60f3c96a370efc3fdcc5f0fb`

**6. Update Book Price by ID**

**Endpoint**: PATCH /books/<string:book_id>/update_price
**Description**: Updates the price of a specific book by its unique identifier.
Query Parameter:
**price**: New price for the book (float).
**Example Usage:**
`curl -X PATCH http://104.42.55.31:5009/books/60f3c96a370efc3fdcc5f0fb/update_price?price=29.99`

### Important Files and Directories

- `app.py`: Main Python script for the application.
- `Dockerfile`: Container file for Docker including list of Python dependencies.
## 2. MongoDB Setup

### Overview

The MongoDB setup in this project involves deploying an instance on Azure Cosmos DB with the MongoDB API. The setup includes reaching client Azure Cosmos DB for MongoDB instance (`pineapple`) by it's connection string. The MongoDB instance is used to store data for the application.

### Database Information

- **Database Name:** PineappleDB
- **Collections:** bookstore
- **Connection String**: `mongodb://pineapple:aWU8ztWJpMUakEscOLItkXYzhKnXdvqRknbIzqUymFNew0ZACmfhbR3XhJxdxtl65rKv3EjgAIerACDbOq7oAA==@pineapple.mongo.cosmos.azure.com:10255/?ssl=true&retrywrites=false&replicaSet=globaldb&maxIdleTimeMS=120000&appName=@pineapple@`

## 3. Docker Containerization

### Overview

Docker containerization is employed to package the Python application along with its dependencies into a container. This ensures consistency across different environments and facilitates easy deployment. The Docker image is stored in Azure Container Registry for streamlined deployment on Azure Kubernetes Service (AKS).

### Dockerfile


```
FROM python:3.9

WORKDIR /app

RUN pip install bson
RUN pip install flask
RUN pip install pymongo

COPY . .

CMD ["python", "app.py"]
EXPOSE 5000
```

## 4. Azure Kubernetes Service (AKS)
### Overview

Azure Kubernetes Service (AKS) is used to orchestrate and manage the deployment of the Python application and MongoDB on the Azure cloud platform.

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
After we deploy the application, we need to check the status of the service and pods. We can both check it either with Azure Portal or kubectl.
Everybody can reach the app with this external-ip `104.42.55.31` via passing into url (such as  http://104.42.55.31/books). 


### Using the application externally
We can use the app externally and access the endpoint for getting all books with following url endpoint: http://104.42.55.31/books, the result concludes that our app is working globally without an issue.

For example we can use the following url to get specific book with hitting the getbyid endpoint:
http://104.42.55.31/books/659829f3a5e6cecfe3f85308

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
 
In the application we will use this connection string to reach to MongoDB client.

After we see it running, we can reach it with username and secret that CosmosDB provide for us.

Then we can run this code:

`mongosh "mongodb://<username>:<password>@<your-cosmosdb-name>.mongo.cosmos.azure.com:10255/<your-database>?ssl=true"`

So when we do this we will be inside of the database.
















  
