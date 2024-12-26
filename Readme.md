# Nginx Load Balancing with Docker

This project demonstrates how to set up Nginx as a load balancer for a Flask application running in Docker containers. The setup utilizes Docker Compose for orchestration and includes instructions for testing load balancing.

## Prerequisites

Before you begin, ensure you have the following installed on your machine:

- **Docker**: [Install Docker](https://docs.docker.com/get-docker/)
- **Docker Compose**: [Install Docker Compose](https://docs.docker.com/compose/install/)
- **Git (optional)**: [Install Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)

## Project Structure

Your project directory should look like this:

```
.
├── docker-compose.yml     # Orchestrates the containers
└── Readme.md           
```

## Setup and Run

Follow these steps to set up and run the application:

1. **Clone the Repository**:
```bash
git clone https://github.com/frenzywall/nginx_LoadBalance_test.git
cd nginx_LoadBalance_test
```

2. **Build and Run Containers**:
```bash
docker-compose up -d
```

3. **Verify Containers**:
```bash
docker ps
```

4. **Access the Application**:
Open your web browser and visit [http://localhost:8080](http://localhost:8080) to see the load balancing in action (using round-robin).

## Test Load Balancing

You can test the load balancing setup using the following methods:

### Manual Test (Curl)
```bash
curl http://localhost:8080/metrics
```

### Using wrk
```bash
sudo apt install wrk
```
```bash
wrk -t12 -c400 -d30s http://localhost:8080/health
```

### Stress Test (Linux using Apache Bench)

1. Install Apache Bench:
```bash
sudo apt-get install apache2-utils
```

2. Run the test:
```bash
ab -n 1000 -c 100 http://localhost:8080/metrics
```

### Stress Test (Windows using Curl)
Run this PowerShell command:
```powershell
for ($i=0; $i -lt 1000; $i++) { curl http://localhost:8080/metrics }
```

## Monitor Logs

To view logs from the Nginx container, run:
```bash
docker logs -f nginx
```

## Stop the Application

When you are done testing, stop and remove the containers with:
```bash
docker-compose down
```

## Conclusion

This setup demonstrates a Flask application with three backend instances (backend1, backend2, backend3). Nginx efficiently balances incoming requests across these backends, ensuring optimal resource utilization and improved response times.

Feel free to modify and expand upon this project as needed!