# ArgoCD Infrastructure Setup

## Installation Steps

### 1. Install ArgoCD
```bash
# Create namespace
kubectl apply -f argocd-namespace.yaml

# Install ArgoCD using kustomization
kubectl apply -k .
```

### 2. Get ArgoCD Admin Password
```bash
# Get initial admin password
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d
```

### 3. Access ArgoCD UI
```bash
# Port forward to access UI locally
kubectl port-forward svc/argocd-server -n argocd 8080:443

# Or get LoadBalancer IP (if using cloud provider)
kubectl get svc argocd-server -n argocd
```

### 4. Login to ArgoCD
- Username: `admin`
- Password: (from step 2)
- URL: `https://localhost:8080` (or LoadBalancer IP)

### 5. Deploy Model Router Application
```bash
# Apply the ArgoCD Application
kubectl apply -f model-router-application.yaml
```

## Configuration

### Update Repository URL
Before deploying, update the repository URL in `model-router-application.yaml`:
```yaml
source:
  repoURL: https://github.com/smith-ai-1/models-router
```

### API Keys Configuration
Update the secrets in `../applications/secrets.yaml` with your actual API keys:
```bash
# Encode your API keys
echo -n "your-openai-key" | base64
echo -n "your-anthropic-key" | base64
echo -n "your-groq-key" | base64
echo -n "your-deepseek-key" | base64
```

## ArgoCD Features Enabled

- **Automatic Sync**: Changes in Git trigger automatic deployments
- **Self-Healing**: ArgoCD will fix any drift from desired state  
- **Pruning**: Removes resources no longer defined in Git
- **Namespace Creation**: Automatically creates target namespace

## Monitoring

Check application status:
```bash
# Via CLI
argocd app get model-router

# Via kubectl
kubectl get applications -n argocd
```