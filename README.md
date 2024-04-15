# Plants API

Plants API is a Django Rest Framework (DRF) project designed to serve as an e-commerce marketplace for vendors and customers. It provides functionalities for customers to browse categories, subcategories, and products, sign up, log in, and place orders. Vendors can post their products and manage customer orders, while administrators have full control over the system.

## Hosted on DigitalOcean, this website is secured with an SSL certificate. 
### Link: https://www.apikosaplants.online/ (I have "debug = False", therefore this link will show "Not Found", if you want to test my API add API endpoints explained below. For example: https://www.apikosaplants.online/admin/

### Domain: apikosaplants.online
### IP Address: 164.92.170.208

### Frontend Running at: https://konstantine25b.github.io/Frontend-Of-Plants-Ecommerce-website
#### Frontend: https://github.com/konstantine25b/Frontend-Of-Plants-Ecommerce-website

## Tech Stack

#### Django | Django-Rest-Framework | PostgreSQL | Simple JWT | Docker | Nginx | Redis | Gunicorn 

## Features

- **Authentication:** Utilizes Simple JWT tokens for authentication.
- **API Schema:** Accessible via `api/schema/` endpoint.
- **Docker:** Dockerized for easy deployment.
- **NGINX and Gunicorn:** Configured for serving the application.
- **Hosted on DigitalOcean:** Deployed on DigitalOcean's droplet.

## Installation

### Prerequisites

- Docker installed on your machine
- DigitalOcean account for deployment (optional)

### Steps

1. Clone the repository:
##### git clone https://github.com/konstantine25b/Backend-Of-Plants-Ecommerce-Website
2. Navigate to the project directory:
##### cd Backend-Of-Plants-Ecommerce-Website
3. Add .env file at Backend-Of-Plants-Ecommerce-Website based on .env.example:

##### SECRET_KEY=
##### DEBUG=
##### DATABASE_NAME= 
##### DATABASE_USER=
##### DATABASE_PASSWORD= 
##### DATABASE_HOST= 
##### DATABASE_PORT=

4. Change Settings.py (located in plants_api folder)
##### Change Debug=False to Debug=True
5. Build Docker containers:
##### docker-compose up --build
6. Access the API
##### http://localhost:8000

## API Endpoints

### Category Management
- **List and Create Categories:** GET/POST /api/product/categories/
-**Retrieve, Update, Delete Category:** GET/PUT/DELETE /api/product/categories/<id>/
-**Permissions:** Custom permissions are applied to categories to allow unauthenticated users to view categories, but only authenticated users with admin privileges can modify them.

### Product Management

- **List and Create Product:** `POST /api/product/products`
- **Retrieve, Update, Delete Product:** `GET/PUT/DELETE api/product/products/<id>/`
- **Filter Products:** Filtering functionality is available for products. You can filter products based on various criteria such as vendor, subcategory, title, description, price, quantity, size, is_featured, and is_active.
- **Permissions:** Custom permissions are applied to products to allow only vendors and admins to create products, but allow anyone to read them.

### Order Management

- **List and Create Orders:** `GET/POST api/order/orders/`
- **Retrieve, Update, Delete Order:** `GET/PUT/DELETE api/order/orders/<id>/`
- **List and Create Order Items:** `GET/POST api/order/order-items/`
- **Retrieve, Update, Delete Order Item:** `GET/PUT/DELETE api/order/order-items/<id>/`
- **Filter Orders:** Filtering functionality is available for orders. You can filter orders based on various criteria such as customer, total_cost, and created_at.
- **Permissions:** Custom permissions are applied to order items to allow only owners of an order item and admins to view the list of order items. These permissions ensure that users can only perform actions they are authorized to do.
  
### Order Item Management
- **List and Create Order Items:** GET/POST /api/order/order-items/
- **Retrieve, Update, Delete Order Item:** GET/PUT/DELETE /api/order/order-items/<id>/
- **Permissions:** Custom permissions are applied to order items to allow only owners of an order item and admins to view the list of order items. These permissions ensure that users can only perform actions they are authorized to do.

### Review Management

- **List and Create Reviews:** `GET/POST api/review/reviews/`
- **Retrieve, Update, Delete Review:** `GET/PUT/DELETE api/review/reviews/<id>/`
- **Permissions:** Custom permissions are applied to reviews to allow owners of a review and admins to edit or delete it, while allowing everyone to view reviews.

### User Management

#### Customer Management

- **Create Customer:** `POST api/user/customer/s`
- **Retrieve, Update, Delete Customer:** `GET/PUT/DELETE api/user/customers/<id>/`
- **Permissions:** Custom permissions are applied to users to allow only owners of an object or admins to perform actions. Additionally, specific permissions are applied for creating new admin users and updating or deleting user information.

#### Vendor Management

- **List and Create Vendors:** `GET/POST api/user/vendors/`
- **Retrieve, Update, Delete Vendor:** `GET/PUT/DELETE api/user/vendors/<id>/`
- **Permissions:** Custom permissions are applied to users to allow only owners of an object or admins to perform actions. Additionally, specific permissions are applied for creating new admin users and updating or deleting user information.

#### Admin Management

- **List and Create Admins:** `GET/POST api/user/admins/`
- **Retrieve, Update, Delete Admin:** `GET/PUT/DELETE api/user/admins/<id>/`
- **Permissions:** Custom permissions are applied to users to allow only owners of an object or admins to perform actions. Additionally, specific permissions are applied for creating new admin users and updating or deleting user information.

### Other Endpoints

- **API Schema:** `GET /api/schema/`
- **Swagger UI:** `GET /api/schema/swagger-ui/`
- **Token Obtain:** `POST /api/token/`
- **Token Refresh:** `POST /api/token/refresh/`
- **Token Verify:** `POST /api/token/verify/`


## Authentication

- **Token Generation:** To obtain an access token, use the `/api/token/` endpoint with valid credentials.
- **Authorization:** Include the access token in the Authorization header for accessing protected endpoints.

## Contributors

- Konstantin Bakhutashvili (https://github.com/konstantine25b)

## License

This project is licensed under the [MIT License](LICENSE).
