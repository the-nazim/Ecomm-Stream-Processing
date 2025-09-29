# Ecommerce API using Stream Processing

An e-commerce platform built with FastAPI, designed for modularity and scalability. It features user authentication, product management, cart functionality, and real-time event streaming using Kafka.

## Features
- User authentication and authorization
- Product catalog and detail pages
- Shopping cart management
- RESTful API endpoints
- Real-time event streaming (Kafka)
- Dockerized Kafka setup
- Custom CSS and responsive templates

## Project Structure
```
app/
  ├── __init__.py
  ├── auth.py
  ├── crud.py
  ├── main.py
  ├── model.py
  ├── schemas.py
  ├── settings.py
  ├── routers/
  │   ├── __init__.py
  │   ├── cart.py
  │   └── product.py
  ├── static/
  │   └── css/
  │       └── custom.css
  └── templates/
      ├── base.html
      ├── cart.html
      ├── home.html
      ├── index.html
      ├── product-detail.html
      └── products.html
streams/
  ├── __init__.py
  ├── app.py
  └── events.py
kafka/
  └── docker-compose.yml
myapp-data/
  └── v1/tables/
requirements.txt
```

## Getting Started

### Prerequisites
- Python 3.12+
- Docker (for Kafka)
- Virtual environment (recommended)

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/the-nazim/ProjectE-c.git
   cd ProjectE-c
   ```
2. Create and activate a virtual environment:
   ```bash
   python3 -m venv env
   source env/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Start Kafka (optional, for event streaming):
   ```bash
   cd kafka
   docker-compose up -d
   ```

### Running the Application
```bash
uvicorn app.main:app --reload
```

Access the app at [http://localhost:8000](http://localhost:8000)

## Usage
- Register and log in to manage your cart and orders.
- Browse products and view details.
- Add products to your cart and checkout.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
This project is licensed under the MIT License.
