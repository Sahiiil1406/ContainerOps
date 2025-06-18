# ContainerOps

[![ContainerOps Demo](https://img.shields.io/badge/▶️-Watch%20Demo-red?style=for-the-badge)](https://github.com/user-attachments/assets/3634dca0-dfd0-4c35-a828-cf2b67e0f702)

[![Django](https://img.shields.io/badge/Django-3.2-green.svg)](https://www.djangoproject.com/)
[![Docker](https://img.shields.io/badge/Docker-20.10-blue.svg)](https://www.docker.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![GitHub](https://img.shields.io/badge/GitHub-Integration-purple.svg)](https://github.com)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-12+-orange.svg)](https://www.postgresql.org/)

## Table of Contents
- [Overview](#-overview)
- [Features](#-features)
- [Technology Stack](#%EF%B8%8F-technology-stack)
- [System Architecture](#%EF%B8%8F-system-architecture)
- [Workflow](#-workflow)
- [Database Schema](#%EF%B8%8F-database-schema)
- [Installation](#-installation)
  - [Prerequisites](#prerequisites)
  - [Setup Instructions](#setup-instructions)
  - [Docker Deployment](#docker-deployment)
- [Usage Guide](#-usage-guide)
  - [Authentication](#authentication)
  - [Repository Selection](#repository-selection)
  - [Deployment Configuration](#deployment-configuration)
  - [Monitoring](#monitoring)
- [Development](#-development)
  - [Project Structure](#project-structure)
- [Team](#-team)
- [License](#-license)

## Overview

ContainerOps is a comprehensive Continuous Deployment (CD) platform that simplifies Docker-based application deployment through automated Dockerfile generation, GitHub integration, and real-time monitoring capabilities. The platform is designed to empower developers by providing a seamless user experience for deploying applications using Docker orchestration, enabling teams to focus on development while ensuring smooth and secure deployment across various environments.

## Features

- **Automated Dockerfile Generation**
  - Intelligent project structure analysis to detect project type
  - Creates optimized Dockerfiles tailored to language and framework requirements
  - Supports custom Dockerfile overrides when needed

- **GitHub Integration**
  - Seamless OAuth authentication for secure repository access
  - Supports both public and private repositories
  - Webhook integration for automatic deployment on code changes
  - Branch selection for deployment flexibility

- **Continuous Deployment Pipeline**
  - Automatic builds triggered by GitHub commits
  - Consistent deployment process across environments
  - Rollback capabilities for failed deployments
  - Support for environment variables and secrets management

- **Container Management**
  - Full lifecycle control of Docker containers (create, start, stop, remove)
  - Container orchestration with health monitoring
  - Resource usage tracking and optimization
  - Container versioning and history

- **Live Monitoring**
  - Real-time build and application logs via WebSockets
  - Container status and health checks
  - Performance metrics and resource utilization

- **Domain Routing**
  - Dynamic Nginx configuration for custom domain mappin
  - Traffic routing

- **Docker Registry**
  - Built-in private registry for container images
  - Secure storage and distribution of application images
  - Version tagging and management


## 🛠Technology Stack

### Backend
- **Framework**: Django 3.2 (Python)
- **WebSockets**: Django Channels

### Frontend
- **HTML/CSS**: Responsive design with TailWind CSS
- **JavaScript**: Interactive dashboard components
- **Real-time Updates**: WebSocket integration

### Infrastructure
- **Containerization**: Docker, Docker Compose
- **Authentication**: OAuth 2.0 (GitHub, Google)
- **Database**: PostgreSQL 12+
- **Web Server**: Nginx for reverse proxy and domain mapping
- **CI/CD**: Webhook-based automated pipeline


## System Architecture

![Screenshot 2025-04-07 100714](https://github.com/user-attachments/assets/3eeec84a-eeb5-4f85-832d-9cd80b0d9021)

ContainerOps follows a microservices architecture with the following key components:

1. **Build Server**
   - Analyzes project structure and generates optimized Dockerfiles
   - Builds Docker images from source code
   - Pushes built images to the integrated Docker registry
   - Handles GitHub webhooks for automated builds

2. **Proxy Server**
   - Manages container lifecycle (create, start, stop, remove)
   - Configures Nginx for domain routing and SSL termination
   - Handles user authentication and authorization
   - Provides API endpoints for the dashboard

3. **Docker Registry**
   - Stores and distributes Docker images
   - Manages image versioning and tagging
   - Provides secure access to container images

4. **Monitoring Service**
   - Collects container metrics and logs
   - Provides real-time updates via WebSockets
   - Monitors container health and performance

5. **Database**
   - Stores user data, repository information, and deployment configurations
   - Tracks container status and history
   - Maintains system settings and environment variables

## Workflow

1. **Authentication & Repository Selection**
   - User authenticates through GitHub or Google OAuth
   - System requests appropriate permissions for repository access
   - User selects target repositories for deployment
   - System validates repository access and structure

2. **Configuration & Setup**
   - User provides deployment parameters (environment variables, resource limits)
   - System analyzes project structure to determine project type
   - User selects branch and deployment options
   - System validates configuration for potential issues

3. **Dockerfile Management**
   - System auto-generates optimized Dockerfiles based on project type
   - User can review and customize generated Dockerfiles
   - System uses existing Dockerfile if present in repository
   - Support for multi-stage builds and optimized caching

4. **Build & Registry**
   - System clones repository and builds Docker image
   - Build logs streamed in real-time via WebSockets
   - Built images are tagged and pushed to integrated Docker registry
   - Image metadata and version history maintained

5. **Deployment Pipeline**
   - GitHub webhooks trigger automatic deployment on code changes
   - System pulls updated images from registry
   - Container orchestration manages deployment updates
   - Zero-downtime deployments with health checks
   - Automatic rollback for failed deployments

6. **Monitoring & Management**
   - Interactive dashboard for container status monitoring
   - Live build and application log streaming
   - Resource utilization metrics and alerts
   - Complete container lifecycle management (scale, restart, stop)
   - Custom domain and routing configuration

## Database Schema
![WhatsApp Image 2025-04-06 at 11 29 43_a1f55b00](https://github.com/user-attachments/assets/b94c5404-b714-4ae3-81b3-ed87468c6365)

The ContainerOps database schema includes the following core tables:

1. **Users**
   - User authentication and profile information
   - OAuth tokens and permissions
   - User preferences and settings

2. **Repositories**
   - GitHub repository details and access credentials
   - Branch information and webhook configuration
   - Project type and structure metadata

3. **Deployments**
   - Container configuration and environment variables
   - Resource allocation and limits
   - Deployment history and versioning
   - Build and runtime logs

4. **Containers**
   - Container status and health metrics
   - Resource utilization statistics
   - Network configuration and port mappings
   - Related deployment and image references

5. **Domains**
   - Custom domain mappings and SSL certificates
   - Routing rules and load balancing configuration
   - DNS verification status and history

## Installation

### Prerequisites

- Python 3.8+
- Docker Engine 20.10+
- Docker Compose 1.29+
- GitHub Developer Account (for OAuth integration)
- PostgreSQL 12+
- Redis 6+
- Nginx 1.18+

### Setup Instructions

#### 1. Clone the repository:
```bash
git clone https://github.com/yourusername/containerops.git
cd containerops
```

#### 2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

#### 3. Install dependencies for build server:
```bash
cd buildServer
pip install -r requirements.txt
```

#### 4. Install dependencies for proxy server:
```bash
cd ../proxy_server
pip install -r requirements.txt
```

#### 5. Set up environment variables (create .env file in project root):
```
# Django Settings
SECRET_KEY=your_django_secret_key
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1,your-domain.com

# Database Configuration
DB_NAME=containerops
DB_USER=postgres
DB_PASSWORD=your_secure_password
DB_HOST=localhost
DB_PORT=5432

# OAuth Credentials
GITHUB_CLIENT_ID=your_github_oauth_id
GITHUB_CLIENT_SECRET=your_github_oauth_secret
GOOGLE_CLIENT_ID=your_google_oauth_id
GOOGLE_CLIENT_SECRET=your_google_oauth_secret

# Docker Registry
DOCKER_REGISTRY_URL=your_registry_url
DOCKER_REGISTRY_USERNAME=registry_username
DOCKER_REGISTRY_PASSWORD=registry_password

# Redis Configuration
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=your_redis_password

# Webhook Secret
WEBHOOK_SECRET=your_webhook_secret_key
```

#### 6. Initialize the database:
```bash
# For build server
cd buildServer
python manage.py migrate

# For proxy server
cd ../proxy_server
python manage.py migrate
```

#### 7. Create superuser for admin access:
```bash
python manage.py createsuperuser
```

#### 8. Start development servers:
```bash
# Start proxy server
cd proxy_server
python manage.py runserver 0.0.0.0:8000

# In a new terminal, start build server
cd buildServer
python manage.py runserver 0.0.0.0:8001
```

### Docker Deployment

For production deployment, use Docker Compose:

1. Configure environment variables in `.env` file
2. Start the services:
   ```bash
   docker-compose up -d
   ```

3. Initialize the database (first time only):
   ```bash
   docker-compose exec proxy_server python manage.py migrate
   docker-compose exec build_server python manage.py migrate
   docker-compose exec proxy_server python manage.py createsuperuser
   ```

4. Access the application at `http://your-domain.com`

## Usage Guide

### Authentication

1. Navigate to the ContainerOps login page
2. Select authentication method (GitHub or Google)
3. Grant the requested permissions for repository access
4. Complete the profile setup if first-time login

### Repository Selection

1. Browse available repositories from your GitHub account
2. Select a repository for deployment
3. Choose the branch to deploy (defaults to main/master)
4. Configure repository-specific settings and webhooks

### Deployment Configuration

1. Review the automatically detected project type
2. Configure environment variables and secrets
3. Set resource limits (CPU, memory)
4. Configure custom domain and SSL settings
5. Review and customize the generated Dockerfile (optional)
6. Initiate the deployment process

### Monitoring

1. View real-time build logs during deployment
2. Monitor container status and health metrics
3. Access application logs via the streaming interface
4. Configure alerts for container events
5. Manage container lifecycle (restart, stop, remove)



### Project Structure

```
containerops/
├── buildServer/             # Build service for Docker images
│   ├── api/                 # Build API endpoints
│   ├── dockerfiles/         # Dockerfile templates
│   ├── github/              # GitHub integration
│   ├── builder/             # Image building logic
│   └── management/          # Django management commands
├── proxy_server/            # Proxy service for container management
│   ├── api/                 # Proxy API endpoints
│   ├── auth/                # Authentication services
│   ├── containers/          # Container management
│   ├── domains/             # Domain routing
│   └── monitoring/          # Monitoring services
├── frontend/                # Frontend assets and templates
│   ├── static/              # Static files (CSS, JS)
│   └── templates/           # HTML templates
├── common/                  # Shared utilities
│   ├── models/              # Shared database models
│   └── utils/               # Helper functions
├── docs/                    # Documentation
├── tests/                   # Test suite
└── docker-compose.yml       # Docker Compose configuration
```
## Future Enhancements

- **Multi-Provider Support**: Extend beyond GitHub to support GitLab, Bitbucket, and Azure DevOps
- **Advanced Scaling**: Horizontal and vertical scaling capabilities for containerized applications
- **Enhanced Monitoring**: Advanced metrics collection with Prometheus integration
- **Multi-Cluster Support**: Distributed deployments across multiple Docker hosts or Kubernetes clusters
- **CI Pipeline Integration**: Complete CI/CD solution with testing frameworks
- **Blue-Green Deployments**: Advanced deployment strategies for zero-downtime updates
- **Service Mesh**: Integration with service mesh solutions for microservices
- **Custom Plugins**: Extensible plugin system for additional functionality
- **Team Collaboration**: Advanced team management and permission controls
- **Cost Optimization**: Resource allocation and cost tracking features

