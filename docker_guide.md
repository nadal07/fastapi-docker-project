# FastAPI Docker Deployment Guide

This guide walks you through creating a FastAPI application and deploying it using Docker for easy sharing and deployment.

## Project Structure

```
fastapi-docker-project/
├── main.py                 # FastAPI application
├── requirements.txt        # Python dependencies
├── Dockerfile             # Docker configuration
├── .dockerignore          # Files to exclude from Docker build
├── docker-compose.yml     # Docker Compose configuration
└── README.md             # This guide
```

## Step 1: Set Up the Project Directory

```bash
# Create project directory
mkdir fastapi-docker-project
cd fastapi-docker-project

# Create the files (copy content from artifacts above)
touch main.py requirements.txt Dockerfile .dockerignore docker-compose.yml
```

## Step 2: Install Dependencies Locally (Optional)

For local development and testing:

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Test the application locally
python main.py
# Or use uvicorn directly:
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## Step 3: Build the Docker Image

```bash
# Build the Docker image
docker build -t fastapi-app:latest .

# Build with a specific tag for sharing
docker build -t your-username/fastapi-app:v1.0 .
```

## Step 4: Run the Container

### Option A: Using Docker directly

```bash
# Run the container
docker run -d \
  --name fastapi-container \
  -p 8000:8000 \
  fastapi-app:latest

# Check if container is running
docker ps

# View logs
docker logs fastapi-container
```

### Option B: Using Docker Compose (Recommended)

```bash
# Start the application
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the application
docker-compose down
```

## Step 5: Test the Application

Once running, test your API:

```bash
# Test the root endpoint
curl http://localhost:8000/

# Test health check
curl http://localhost:8000/health

# Test creating an item
curl -X POST "http://localhost:8000/items" \
     -H "Content-Type: application/json" \
     -d '{"name": "Test Item", "price": 29.99, "category": "Electronics", "description": "A test item"}'

# Test getting all items
curl http://localhost:8000/items
```

Or visit `http://localhost:8000/docs` for the interactive API documentation.

## Step 6: Sharing the Docker Image

### Method 1: Save and Share as File

```bash
# Save image to tar file
docker save fastapi-app:latest > fastapi-app.tar

# Load on another machine
docker load < fastapi-app.tar
```

### Method 2: Push to Docker Hub

```bash
# Login to Docker Hub
docker login

# Tag your image
docker tag fastapi-app:latest your-username/fastapi-app:v1.0

# Push to Docker Hub
docker push your-username/fastapi-app:v1.0

# Others can pull and run:
docker pull your-username/fastapi-app:v1.0
docker run -d -p 8000:8000 your-username/fastapi-app:v1.0
```

### Method 3: Private Registry

```bash
# Tag for private registry
docker tag fastapi-app:latest your-registry.com/fastapi-app:v1.0

# Push to private registry
docker push your-registry.com/fastapi-app:v1.0
```

## Step 7: Production Deployment

### Environment Variables

Create a `.env` file for production:

```env
# .env
PYTHONPATH=/app
ENVIRONMENT=production
LOG_LEVEL=info
```

Update docker-compose.yml:

```yaml
services:
  fastapi-app:
    build: .
    env_file:
      - .env
    ports:
      - "8000:8000"
```

### Scaling with Docker Compose

```yaml
services:
  fastapi-app:
    build: .
    ports:
      - "8000-8002:8000"
    deploy:
      replicas: 3
```

## Step 8: Useful Docker Commands

```bash
# View running containers
docker ps

# Stop container
docker stop fastapi-container

# Remove container
docker rm fastapi-container

# View images
docker images

# Remove image
docker rmi fastapi-app:latest

# Clean up unused resources
docker system prune -a

# View container logs
docker logs -f fastapi-container

# Execute command in running container
docker exec -it fastapi-container bash

# Check container resource usage
docker stats fastapi-container
```

## Troubleshooting

### Common Issues

1. **Port already in use**: Change the host port in docker-compose.yml
   ```yaml
   ports:
     - "8001:8000"  # Use port 8001 instead
   ```

2. **Permission denied**: Make sure Docker daemon is running and user has permissions

3. **Build fails**: Check Dockerfile syntax and ensure all files exist

4. **Container exits immediately**: Check logs with `docker logs container-name`

### Health Checks

The application includes a health check endpoint at `/health`. Docker will automatically restart the container if health checks fail.

## Security Considerations

- The Dockerfile creates a non-root user for security
- Use environment variables for sensitive data
- Consider using Docker secrets for production passwords
- Keep base images updated
- Scan images for vulnerabilities: `docker scan fastapi-app:latest`

## Next Steps

- Add database integration (PostgreSQL, MongoDB)
- Implement authentication and authorization
- Add logging and monitoring
- Set up CI/CD pipeline
- Configure reverse proxy (Nginx)
- Add SSL/TLS certificates
- Implement caching (Redis)

Your FastAPI application is now containerized and ready for deployment!