# Plants API

Plants API is a Django Rest Framework (DRF) project designed to serve as an e-commerce marketplace for vendors and customers. It provides functionalities for customers to browse categories, subcategories, and products, sign up, log in, and place orders. Vendors can post their products and manage customer orders, while administrators have full control over the system.

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
git clone https://github.com/konstantine25b/Backend-Of-Plants-Ecommerce-Website
2. Navigate to the project directory:
cd plants_api
3. Build Docker containers:
docker-compose build
4. Start Docker containers:
docker-compose up
5. Access the API at `http://localhost:8000`.

## API Endpoints

## Authentication

- **Token Generation:** To obtain an access token, use the `/api/token/` endpoint with valid credentials.
- **Authorization:** Include the access token in the Authorization header for accessing protected endpoints.


## Deployment

1. Set up a DigitalOcean droplet.
2. Install Docker and Docker Compose.
3. Clone the repository onto the droplet.
4. Follow the installation steps mentioned above.
5. Configure NGINX and Gunicorn for production deployment.

## Contributors

- Konstantin Bakhutashvili (https://github.com/konstantine25b)

## License

This project is licensed under the [MIT License](LICENSE).
