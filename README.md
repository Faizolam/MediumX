# MediumX

**MediumX** is a full-stack blogging platform inspired by Medium.com, designed to offer users a seamless experience in creating, reading, and managing articles. Built with modern technologies, it ensures scalability, security, and performance.

## 🚀 Features

* **User Authentication & Authorization**: Secure user registration and login using JSON Web Tokens (JWT).
* **Article Management**: Create, edit, delete, and view articles with rich text support.
* **Responsive Design**: Optimized for various devices with a clean and intuitive interface.
* **Database Migrations**: Efficient schema management using Alembic.
* **Containerization**: Simplified development and deployment with Docker and Docker Compose.
* **Web Server Integration**: Nginx configured for serving the application in production.
* **Testing**: Robust testing suite using Pytest.
* **CI/CD**: Automated workflows with GitHub Actions for continuous integration and deployment.

## 🛠️ Tech Stack

* **Backend**: Python, FastAPI, Pydantic
* **Frontend**: HTML, CSS, JavaScript
* **Database**: PostgreSQL
* **Migrations**: Alembic
* **Containerization**: Docker, Docker Compose
* **Web Server**: Nginx
* **Testing**: Pytest
* **CI/CD**: GitHub Actions
* **Cloud**: GCP
* **Infrastructure as Code**: Terraform

## 📁 Project Structure

```
MediumX/
├── .github/workflows/       # CI/CD workflows
├── alembic/                 # Database migration scripts
├── app/                     # Backend application
├── client/                  # Frontend application
├── nginx/                   # Nginx configuration
├── terraform/               # Terraform configurations
├── tests/                   # Test cases
├── .dockerignore            # Docker ignore file
├── .gitignore               # Git ignore file
├── Dockerfile               # Dockerfile for backend
├── docker-compose-dev.yml   # Docker Compose for development
├── docker-compose-prod.yml  # Docker Compose for production
├── alembic.ini              # Alembic configuration
├── pytest.ini               # Pytest configuration
├── requirements.txt         # Python dependencies
└── README.md                # Project documentation
```

## ⚙️ Getting Started

### Prerequisites

* [Docker](https://www.docker.com/get-started)
* [Docker Compose](https://docs.docker.com/compose/install/)

### Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/Faizolam/MediumX.git
   cd MediumX
   ```

2. **Set up environment variables:**

   Create a `.env` file in the root directory and define necessary environment variables.

3. **Build and run the containers:**

   For development:

   ```bash
   docker-compose -f docker-compose-dev.yml up --build
   ```

   For production:

   ```bash
   docker-compose -f docker-compose-prod.yml up --build
   ```

4. **Apply database migrations:**

   ```bash
   docker-compose exec backend alembic upgrade head
   ```

5. **Access the application:**

   * Frontend: `http://localhost:3000`
   * Backend API: `http://localhost:8000/api`

## 🧪 Running Tests

To run backend tests:

```bash
docker-compose exec backend pytest
```

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## 📬 Contact

For questions or feedback, please contact [Faiz Alam](mailto:faiz@example.com).

---

Feel free to customize this `README.md` further to match the specific details and configurations of your project. If you need assistance with any particular section or additional features, feel free to ask!
