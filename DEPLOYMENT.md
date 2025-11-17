# OneTrueAddress - Deployment Guide

## Local Development (Current Setup)

The application is currently running in development mode on your local machine.

**Access the application at**: `http://localhost:5000`

### Current Configuration

- **Flask Debug Mode**: Enabled (auto-reloads on code changes)
- **Host**: 0.0.0.0 (accessible from all network interfaces)
- **Port**: 5000
- **Database**: PostgreSQL at 212.2.245.85:6432

### Starting/Stopping the Server

**Start:**
```bash
python app.py
```

**Stop:**
Press `Ctrl+C` in the terminal

---

## Production Deployment Options

### Option 1: Deploy with Gunicorn (Linux/Mac)

1. **Update .env for production:**
```bash
FLASK_ENV=production
FLASK_DEBUG=False
```

2. **Run with Gunicorn:**
```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

**For Windows**, Gunicorn is not supported. Use Option 2 or Option 3.

### Option 2: Deploy with Waitress (Windows Compatible)

1. **Install Waitress:**
```bash
pip install waitress
```

2. **Create a production server file** (`server.py`):
```python
from waitress import serve
from app import app
import os

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    serve(app, host='0.0.0.0', port=port)
```

3. **Run the server:**
```bash
python server.py
```

### Option 3: Deploy to Cloud Platform

#### Heroku

1. **Create `Procfile`:**
```
web: gunicorn app:app
```

2. **Add PostgreSQL connection pooling** (recommended for Heroku):
```bash
pip install psycopg2-pool
```

3. **Deploy:**
```bash
heroku create your-app-name
git push heroku main
```

#### Google Cloud Run

1. **Create `Dockerfile`:**
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8080", "app:app"]
```

2. **Build and deploy:**
```bash
gcloud builds submit --tag gcr.io/PROJECT_ID/onetrueaddress
gcloud run deploy onetrueaddress --image gcr.io/PROJECT_ID/onetrueaddress --platform managed
```

#### AWS Elastic Beanstalk

1. **Install EB CLI:**
```bash
pip install awsebcli
```

2. **Initialize and deploy:**
```bash
eb init -p python-3.11 onetrueaddress
eb create onetrueaddress-env
eb deploy
```

#### Azure Web Apps

1. **Create `startup.txt`:**
```
gunicorn --bind=0.0.0.0 --timeout 600 app:app
```

2. **Deploy using Azure CLI:**
```bash
az webapp up --name onetrueaddress --resource-group myResourceGroup
```

### Option 4: Docker Deployment

1. **Create `Dockerfile`:**
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Expose port
EXPOSE 5000

# Run with gunicorn
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

2. **Create `docker-compose.yml`:**
```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "5000:5000"
    environment:
      - DB_HOST=212.2.245.85
      - DB_PORT=6432
      - DB_NAME=postgres
      - DB_USER=postgres
      - DB_PASSWORD=${DB_PASSWORD}
      - FLASK_ENV=production
    restart: unless-stopped
```

3. **Build and run:**
```bash
docker-compose up -d
```

---

## Security Considerations

### Environment Variables

**Never commit** the `.env` file to version control. Always use:
- Environment variables on the server
- Secret management services (AWS Secrets Manager, Azure Key Vault, etc.)
- `.env` files only for local development

### Database Connection

Consider these security improvements:

1. **Use SSL for database connections:**
```python
conn = psycopg2.connect(
    **DB_CONFIG,
    sslmode='require'
)
```

2. **Use connection pooling:**
```python
from psycopg2 import pool

connection_pool = psycopg2.pool.SimpleConnectionPool(
    1, 20,  # min and max connections
    **DB_CONFIG
)
```

3. **Add rate limiting:**
```bash
pip install flask-limiter
```

```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)
```

### HTTPS/SSL

For production, always use HTTPS:

1. **With reverse proxy (Nginx):**
```nginx
server {
    listen 443 ssl;
    server_name yourdomain.com;

    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;

    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

2. **With Cloudflare** (easiest):
- Point your domain to your server
- Enable SSL in Cloudflare dashboard
- Automatic HTTPS with free certificate

---

## Performance Optimization

### Database Indexing

Add indexes to improve search performance:

```sql
CREATE INDEX idx_full_address ON team_cool_and_gang.pinellas_fl ("Full Address");
CREATE INDEX idx_full_address_lower ON team_cool_and_gang.pinellas_fl (LOWER("Full Address"));
```

### Caching

Add Redis caching for frequent searches:

```bash
pip install redis flask-caching
```

```python
from flask_caching import Cache

cache = Cache(app, config={'CACHE_TYPE': 'redis', 'CACHE_REDIS_URL': 'redis://localhost:6379/0'})

@app.route('/search', methods=['POST'])
@cache.cached(timeout=300, query_string=True)
def search_address():
    # ... existing code
```

### Connection Pooling

Implement connection pooling to reuse database connections:

```python
from psycopg2 import pool

# Create pool at startup
connection_pool = pool.SimpleConnectionPool(
    minconn=1,
    maxconn=10,
    **DB_CONFIG
)

def get_db_connection():
    return connection_pool.getconn()

def return_connection(conn):
    connection_pool.putconn(conn)
```

---

## Monitoring & Logging

### Application Logging

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)
```

### Health Monitoring

Use the `/health` endpoint with monitoring tools:
- UptimeRobot
- Pingdom
- AWS CloudWatch
- Azure Monitor

---

## Scaling

### Horizontal Scaling

1. **Load Balancer**: Use Nginx, HAProxy, or cloud load balancer
2. **Multiple Instances**: Run multiple app instances
3. **Session Storage**: Use Redis for session management if needed

### Vertical Scaling

- Increase server resources (CPU, RAM)
- Optimize database queries
- Add caching layers

---

## Backup & Recovery

### Database Backups

```bash
pg_dump -h 212.2.245.85 -p 6432 -U postgres -t team_cool_and_gang.pinellas_fl postgres > backup.sql
```

### Application Backups

- Use version control (Git)
- Regular repository backups
- Document deployment procedures

---

## Troubleshooting

### Common Issues

**Port Already in Use:**
```bash
# Find process using port 5000
netstat -ano | findstr :5000  # Windows
lsof -i :5000                 # Mac/Linux

# Kill the process
taskkill /PID <PID> /F        # Windows
kill -9 <PID>                 # Mac/Linux
```

**Database Connection Timeout:**
- Check firewall rules
- Verify database credentials
- Test network connectivity: `ping 212.2.245.85`

**Module Not Found:**
```bash
pip install -r requirements.txt
```

---

## Support & Maintenance

### Regular Updates

```bash
# Update dependencies
pip install --upgrade -r requirements.txt

# Check for security vulnerabilities
pip install safety
safety check
```

### Logs Location

- **Development**: Console output
- **Production**: `/var/log/app.log` or specified log file

---

For questions or issues, refer to the main README.md or create an issue in the repository.

