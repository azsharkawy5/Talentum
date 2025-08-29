# 🏢 Talentum API

> **Enterprise-grade Company Management System — secure, workflow-driven, and built for managing talent, structure, and performance.**

[![Python](https://img.shields.io/badge/Python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![Django](https://img.shields.io/badge/Django-5.2+-green.svg)](https://www.djangoproject.com/)
[![DRF](https://img.shields.io/badge/DRF-3.16+-orange.svg)](https://www.django-rest-framework.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Tests](https://img.shields.io/badge/Tests-41%20Passing-brightgreen.svg)](tests)

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Architecture](#-architecture)
- [Quick Start](#-quick-start)
- [API Documentation](#-api-documentation)
- [Testing](#-testing)
- [Deployment](#-deployment)
- [Contributing](#-contributing)
- [License](#-license)

## 🎯 Overview

Talentum API is a comprehensive Django-based solution designed to streamline organizational management through:

- **Company & Department Management**: Hierarchical organizational structure
- **Employee Lifecycle**: Complete employee profile and management
- **Project Management**: Project tracking with employee assignments
- **Performance Reviews**: Structured workflow with state transitions
- **Role-Based Access Control**: Secure, granular permissions system

Built with enterprise-grade security and scalability in mind, the system provides a robust foundation for modern business operations.

## ✨ Features

### 🔐 Security & Authentication
- **JWT Authentication**: Industry-standard token-based security
- **Role-Based Access Control (RBAC)**: Admin, Manager, Employee roles
- **Granular Permissions**: Object-level access control
- **Data Isolation**: Users only see appropriate data

### 🏗️ Core Management
- **Companies**: Multi-company support with auto-calculated metrics
- **Departments**: Organizational structure management
- **Employees**: Comprehensive employee profiles and management
- **Projects**: Project lifecycle with team assignments

### 📊 Performance Reviews
- **Workflow Engine**: 6-stage review process
- **State Transitions**: Enforced workflow validation
- **Managerial Oversight**: Approval and rejection handling
- **Audit Trail**: Complete review history

### 🔧 Technical Features
- **RESTful API**: Professional-grade API design
- **Auto-calculated Fields**: Real-time metrics and counts
- **Advanced Filtering**: Search, sort, and filter capabilities
- **Pagination**: Built-in performance optimization
- **Comprehensive Testing**: 41+ test coverage

## 🏛️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Company Management System                │
├─────────────────────────────────────────────────────────────┤
│  Frontend (Future) │  API Layer │  Business Logic │  Data │
│                    │             │                 │       │
│  React/Vue.js      │  Django     │  Django         │  SQL  │
│  (Planned)         │  REST       │  Models         │  DB   │
│                    │  Framework  │  & Views        │       │
└─────────────────────────────────────────────────────────────┘
```

### Technology Stack

- **Backend**: Django 5.2+ with Python 3.13+
- **API**: Django REST Framework 3.16+
- **Authentication**: JWT with Simple JWT
- **Database**: PostgreSQL (production) / SQLite (development)
- **Testing**: pytest with Django integration
- **Documentation**: Comprehensive API docs and Postman collection

## 🚀 Quick Start

### Prerequisites

- Python 3.13+
- Poetry (dependency management)
- PostgreSQL (optional, SQLite for development)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd CMS
   ```

2. **Install dependencies**
   ```bash
   poetry install
   ```

3. **Set up environment variables**
   ```bash
   cp env.example .env
   # Edit .env with your configuration
   ```

4. **Run migrations**
   ```bash
   poetry run python manage.py migrate
   ```

5. **Create superuser**
   ```bash
   poetry run python manage.py createsuperuser
   ```

6. **Start development server**
   ```bash
   poetry run python manage.py runserver
   ```

### Environment Variables

```bash
# Required
SECRET_KEY=your-secret-key-here
DEBUG=True

# Database (optional - defaults to SQLite)
DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=5432

# JWT Settings
JWT_ACCESS_TOKEN_LIFETIME=1h
JWT_REFRESH_TOKEN_LIFETIME=7d
```

## 📚 API Documentation

### Base URL
```
http://localhost:8000/api/v1/
```

### Authentication
All API endpoints require JWT authentication:
```bash
Authorization: Bearer <your_access_token>
```

### Core Endpoints

| Resource | Endpoint | Methods | Description |
|----------|----------|---------|-------------|
| **Companies** | `/companies/` | `GET` | List and view companies |
| **Departments** | `/departments/` | `GET, POST, PATCH, DELETE` | Department management |
| **Employees** | `/employees/` | `GET, POST, PATCH, DELETE` | Employee management |
| **Projects** | `/projects/` | `GET, POST, PATCH, DELETE` | Project management |
| **Reviews** | `/performance-reviews/` | `GET, POST, PATCH, DELETE` | Performance reviews |

### Postman Collection

Easily test and interact with the API documentation using Postman

Import the provided Postman collection for easy API testing:
- **File**: `Talentum.postman_collection.json`
- **Setup**: Update environment variables with your server details

### API Examples

#### Create a Department
```bash
curl -X POST http://localhost:8000/api/v1/departments/ \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "company": 1,
    "name": "Engineering"
  }'
```

#### List Employees
```bash
curl -X GET http://localhost:8000/api/v1/employees/ \
  -H "Authorization: Bearer <token>"
```

## 🧪 Testing

### Run All Tests
```bash
poetry run python manage.py test
```

### Run Specific Test Suites
```bash
# Model tests
poetry run python manage.py test apps.companies.test_models

# View tests
poetry run python manage.py test apps.companies.test_views

# All company tests
poetry run python manage.py test apps.companies
```

### Test Coverage
- **Models**: 18 tests covering data validation and relationships
- **Views**: 23 tests covering API endpoints and permissions
- **Total**: 41+ tests ensuring system reliability

## 🚀 Deployment

### Production Setup

1. **Environment Configuration**
   ```bash
   DEBUG=False
   SECRET_KEY=<strong-secret-key>
   DATABASE_URL=<production-db-url>
   ```

2. **Static Files**
   ```bash
   poetry run python manage.py collectstatic
   ```

3. **WSGI Server**
   ```bash
   gunicorn Talentum.wsgi:application
   ```

### Docker (Future Enhancement)
```dockerfile
# Dockerfile will be added for containerized deployment
FROM python:3.13-slim
# ... container configuration
```

## 🔧 Development

### Project Structure
```
CMS/
├── apps/
│   ├── accounts/          # User authentication & management
│   └── companies/         # Core business logic
├── Talentum/              # Django project settings
├── migrations/            # Database migrations
├── tests/                 # Test suites
├── docs/                  # Documentation
└── requirements/          # Dependencies
```

### Code Style
- **Python**: PEP 8 compliance
- **Django**: Django best practices
- **API**: RESTful conventions
- **Testing**: Comprehensive coverage

### Adding New Features
1. Create models in appropriate app
2. Add serializers for API representation
3. Implement views with proper permissions
4. Write comprehensive tests
5. Update documentation

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Make your changes** with proper testing
4. **Commit your changes**: `git commit -m 'Add amazing feature'`
5. **Push to the branch**: `git push origin feature/amazing-feature`
6. **Open a Pull Request**

### Contribution Guidelines
- Follow existing code style and patterns
- Add tests for new functionality
- Update documentation as needed
- Ensure all tests pass before submitting

## 📊 Performance Review Workflow

The system implements a sophisticated 6-stage workflow:

```
Pending Review → Review Scheduled → Feedback Provided → Under Approval → Review Approved/Rejected
     ↓                ↓                ↓              ↓              ↓
  Employee      Meeting Set      Feedback        Manager        Final
  Flagged       Date/Time       Documented      Review         Decision
```

### Stage Transitions
- **Pending Review** → **Review Scheduled**: When review date is confirmed
- **Review Scheduled** → **Feedback Provided**: After feedback documentation
- **Feedback Provided** → **Under Approval**: Submitted for managerial review
- **Under Approval** → **Review Approved/Rejected**: Manager decision
- **Review Rejected** → **Feedback Provided**: For rework

## 🔒 Security Features

### Authentication
- JWT tokens with configurable expiration
- Refresh token rotation
- Token blacklisting for logout

### Authorization
- Role-based access control (Admin, Manager, Employee)
- Object-level permissions
- Company and department isolation

### Data Protection
- Input validation and sanitization
- SQL injection prevention
- XSS protection
- CSRF protection

## 📈 Roadmap

### Phase 1 (Current) ✅
- [x] Core models and API
- [x] Authentication system
- [x] Basic CRUD operations
- [x] Performance review workflow
- [x] Comprehensive testing

### Phase 2 (Planned) 🚧
- [ ] Frontend web application
- [ ] Advanced reporting and analytics
- [ ] Email notifications
- [ ] File uploads and attachments
- [ ] Mobile API optimization

### Phase 3 (Future) 🔮
- [ ] Real-time notifications
- [ ] Advanced workflow engine
- [ ] Integration APIs
- [ ] Multi-tenant architecture
- [ ] Advanced analytics dashboard

## 🐛 Troubleshooting

### Common Issues

**Database Connection Errors**
```bash
# Check database configuration in .env
# Ensure PostgreSQL is running (if using)
# Verify database credentials
```

**Migration Issues**
```bash
# Reset migrations if needed
poetry run python manage.py migrate --fake-initial
```

**Permission Errors**
```bash
# Check user role assignments
# Verify object-level permissions
# Ensure proper authentication headers
```

### Getting Help
- Check the [API Documentation](API_DOCUMENTATION.md)
- Review test cases for usage examples
- Open an issue with detailed error information

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Support

For support and questions:
- **Email**: [azsharkawy5@gmail.com](mailto:azsharkawy5@gmail.com)
- **Issues**: [GitHub Issues](https://github.com/azsharkawy5/Talentum/issues)
- **Documentation**: [API Documentation](API_DOCUMENTATION.md)

---

**Built with ❤️ by [Ahmad Zakaria](https://github.com/azsharkawy5)**

*Last updated: January 2025*
