# College Syllabus & Notes AI Assistant - Deployment Guide

## 🌐 Deployment Options

### 1. Local Development
See [SETUP.md](SETUP.md) for local setup instructions.

### 2. Docker Compose (Recommended)
See [SETUP.md](SETUP.md#-docker-setup-guide) for Docker deployment.

### 3. Cloud Platforms

#### Railway

1. Push to GitHub
2. Connect repository on Railway.app
3. Add services:
   - Backend (Python)
   - Frontend (Node.js)
   - Ollama (via Docker)
4. Set environment variables
5. Deploy

#### Render

1. Create Web Services for backend and frontend
2. Use PostgreSQL for production database
3. Set environment variables
4. Deploy

#### AWS EC2

```bash
# 1. Launch Ubuntu instance
# 2. SSH into instance
ssh -i key.pem ubuntu@your-instance.com

# 3. Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# 4. Clone repository
git clone https://github.com/Rexin29/College-ai-agent-.git
cd College-ai-agent-

# 5. Deploy with Docker Compose
docker-compose up -d

# 6. Setup Nginx reverse proxy
sudo apt-get install nginx
sudo nano /etc/nginx/sites-available/default
# Configure proxy settings

# 7. Setup SSL with Let's Encrypt
sudo apt-get install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

#### DigitalOcean App Platform

1. Connect GitHub repository
2. Create App components for backend and frontend
3. Set environment variables
4. Deploy

#### Heroku (Alternative)

```bash
# Install Heroku CLI
brewinstall heroku/brew/heroku

# Login
heroku login

# Create app
heroku create college-rag-assistant

# Deploy
git push heroku main
```

---

## 📦 Production Checklist

- [ ] Use environment variables for all secrets
- [ ] Set up database for production (PostgreSQL)
- [ ] Enable CORS for production domain
- [ ] Setup SSL/TLS certificates
- [ ] Configure logging and monitoring
- [ ] Setup backup strategy for vector database
- [ ] Configure rate limiting
- [ ] Enable authentication if needed
- [ ] Setup error tracking (Sentry)
- [ ] Monitor resource usage
- [ ] Setup CI/CD pipeline
- [ ] Document deployment process

---

## 🔐 Security Considerations

1. **Environment Variables**: Never commit `.env` file
2. **CORS**: Restrict to your domain
3. **API Keys**: Use secure secret management
4. **Database**: Use strong passwords
5. **SSL/TLS**: Always use HTTPS in production
6. **Rate Limiting**: Implement to prevent abuse
7. **Input Validation**: Validate all user inputs
8. **Logging**: Log security events

---

## 📊 Monitoring & Logging

### Setup Sentry for Error Tracking

```python
import sentry_sdk
sentry_sdk.init(
    dsn="your-sentry-dsn",
    traces_sample_rate=1.0
)
```

### ELK Stack for Logs

```yaml
# docker-compose.yml addition
logstash:
  image: docker.elastic.co/logstash/logstash:8.0.0
  volumes:
    - ./logstash.conf:/usr/share/logstash/pipeline/logstash.conf

elasticsearch:
  image: docker.elastic.co/elasticsearch/elasticsearch:8.0.0
  environment:
    - discovery.type=single-node

kibana:
  image: docker.elastic.co/kibana/kibana:8.0.0
  ports:
    - "5601:5601"
```

---

## 📈 Scaling Strategies

### Horizontal Scaling

1. **Load Balancer**: Use Nginx or HAProxy
2. **Multiple Backend Instances**: Scale API servers
3. **Cache Layer**: Add Redis for caching
4. **Database Replication**: Setup master-slave replication

### Vertical Scaling

1. Increase server resources (CPU, RAM)
2. Optimize database queries
3. Implement caching strategies

---

## 🔄 CI/CD Pipeline

### GitHub Actions Example

```yaml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Build and Push Docker Images
        run: |
          docker build -t backend:latest ./backend
          docker build -t frontend:latest ./frontend
      - name: Deploy to Server
        run: |
          # SSH to server and pull latest images
          ssh deploy@your-server.com 'cd /app && docker-compose pull && docker-compose up -d'
```

---

## 📞 Support

For deployment issues:
1. Check logs: `docker-compose logs -f`
2. Open GitHub issue
3. Contact support
