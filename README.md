# Full-Stack ERP Application (FastAPI + Nuxt 4)
The project make by myself for learning and simple code
This repository is an academic/practice project created for learning
You guys can run the project follow command below:

This project is a full-stack Enterprise Resource Planning (ERP) application featuring a FastAPI backend, Nuxt 4 frontend, PostgreSQL database, and Redis cache. It is designed to run seamlessly on Docker Desktop with Kubernetes enabled.

# ====System Architecture & Tech Stack=====
Frontend: Nuxt 4, PrimeVue, Pinia, TailwindCSS

Backend: FastAPI (Python 3.12), SQLAlchemy, Passlib, Bcrypt

Database & Cache: PostgreSQL, Redis

Orchestration: Kubernetes / Docker Desktop

# =======Requirements=====
Before running the application, ensure you have the following installed on your host machine:

Docker Desktop with Kubernetes enabled and WSL 2 backend.

kubectl CLI tool installed.

Node.js (v22 or higher) and Python (v3.12).

# 1. Create Namespace
kubectl apply -f k8s/namespace.yaml

# 2. Deploy Infrastructure Services (Database & Redis)
kubectl apply -f k8s/postgres/ -n erp
kubectl apply -f k8s/redis/ -n erp

# 3. Deploy Application Services (Backend & Frontend)
kubectl apply -f k8s/backend/ -n erp
kubectl apply -f k8s/frontend/ -n erp

# 4. Apply Ingress (Optional)
If you are using an Ingress Controller (like NGINX Ingress Controller):

kubectl apply -f k8s/ingress.yaml -n erp

# 5. Verify Resources
Check that all pods are running:

kubectl get pods -n erp

===============================
If you are not using Ingress, expose the services locally using port-forward

# 1. Forward Backend Service
kubectl port-forward service/backend-service 8000:8000 -n erp
Backend API Docs: http://localhost:8000

# 2. Forward Frontend Service
kubectl port-forward service/frontend-service 3000:3000 -n erp
Frontend Application: http://localhost:3000

===============================
# Useful Kubernetes Commands
# View Pod logs
kubectl logs -f deployment/backend-deployment -n erp
kubectl logs -f deployment/frontend-deployment -n erp

# Re-deploy after updating Docker images
kubectl rollout restart deployment backend-deployment -n erp
kubectl rollout restart deployment frontend-deployment -n erp