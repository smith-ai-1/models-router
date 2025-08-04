# Model Router Deployment Guide

## 🚀 Quick Start

### Prerequisites
- Kubernetes cluster (1.24+)
- kubectl configured
- Docker registry access (GitHub Container Registry)
- Domain name (optional, for production)

### 1. Deploy to Kubernetes

#### Option A: Direct Kubernetes Deployment
```bash
# Apply all manifests
kubectl apply -f k8s/applications/

# Check deployment status
kubectl get pods -n model-router
kubectl get svc -n model-router
```

#### Option B: ArgoCD GitOps Deployment (Recommended)
```bash
# Install ArgoCD
kubectl apply -f k8s/infra/argocd-namespace.yaml
kubectl apply -k k8s/infra/

# Get ArgoCD admin password
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d

# Access ArgoCD UI
kubectl port-forward svc/argocd-server -n argocd 8080:443

# Deploy Model Router app
kubectl apply -f k8s/infra/model-router-application.yaml
```

## ⚙️ Configuration

### API Keys Setup
Update `k8s/applications/secrets.yaml` with your API keys:
```bash
# Encode your keys
echo -n "your-openai-key" | base64
echo -n "your-anthropic-key" | base64
echo -n "your-groq-key" | base64
echo -n "your-deepseek-key" | base64

# Update secrets.yaml with encoded values
kubectl apply -f k8s/applications/secrets.yaml
```

### Environment Configuration
Modify `k8s/applications/configmap.yaml` for:
- Log levels
- Rate limiting
- Custom application settings

### Scaling Configuration
Adjust `k8s/applications/hpa.yaml` for:
- Min/max replicas
- CPU/Memory thresholds
- Scaling policies

## 🔧 CI/CD Pipeline

### GitHub Actions Workflows

1. **CI/CD Pipeline** (`.github/workflows/ci-cd.yaml`)
   - Runs on push to main
   - Tests, builds, and deploys automatically
   - Creates container images tagged with commit SHA

2. **PR Validation** (`.github/workflows/pr-check.yaml`)
   - Validates PRs before merge
   - Runs tests, linting, and manifest validation
   - Comments on PRs with results

3. **Release Pipeline** (`.github/workflows/release.yaml`)
   - Triggers on version tags (v*)
   - Creates GitHub releases with changelogs
   - Builds multi-architecture images

### Container Registry
Images are published to GitHub Container Registry:
```
ghcr.io/smith-ai-1/models-router:latest
ghcr.io/smith-ai-1/models-router:main-<sha>
ghcr.io/smith-ai-1/models-router:v1.0.0
```

### GitHub Actions Setup
No additional secrets needed! The workflows use:
- `GITHUB_TOKEN` (automatically provided)
- GitHub Container Registry (automatically configured)

To enable the full pipeline:
1. Push to `main` branch triggers deployment
2. Create tags like `v1.0.0` for releases
3. Pull Requests automatically run validation

## 🏗️ Architecture Overview

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   GitHub Repo   │───▶│  GitHub Actions │───▶│   Container     │
│                 │    │     CI/CD       │    │   Registry      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                                        │
                                                        ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│     ArgoCD      │───▶│   Kubernetes    │◀───│     Ingress     │
│   (GitOps)      │    │    Cluster      │    │   Controller    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 📊 Monitoring & Observability

### Health Checks
- Kubernetes liveness probe: `/health`
- Kubernetes readiness probe: `/health`
- Docker healthcheck included

### Scaling
- HorizontalPodAutoscaler configured
- CPU and memory-based scaling
- Min: 3 replicas, Max: 20 replicas

### Security
- Non-root container user
- Security contexts applied
- Secrets managed via Kubernetes
- Network policies (optional)

## 🔍 Troubleshooting

### Common Issues

**Pods not starting:**
```bash
kubectl describe pod -n model-router
kubectl logs -n model-router deployment/model-router
```

**ArgoCD not syncing:**
```bash
kubectl get applications -n argocd
kubectl describe application model-router -n argocd
```

**Image pull errors:**
```bash
# Check if you have access to GHCR
docker login ghcr.io
docker pull ghcr.io/smith-ai-1/models-router:latest
```

### Useful Commands
```bash
# Check all resources
kubectl get all -n model-router

# Port forward for local testing
kubectl port-forward svc/model-router-service -n model-router 8080:80

# Check HPA status
kubectl get hpa -n model-router

# Check ingress
kubectl get ingress -n model-router
```

## 🎯 Production Checklist

- [ ] Configure proper domain and TLS certificates
- [ ] Set up monitoring (Prometheus/Grafana)
- [ ] Configure log aggregation (ELK/Loki)
- [ ] Set up backup for ArgoCD
- [ ] Configure network policies
- [ ] Set resource quotas and limits
- [ ] Test disaster recovery procedures
- [ ] Set up alerting rules
- [ ] Configure authentication (OAuth/OIDC)
- [ ] Review security policies