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

  
