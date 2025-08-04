# Model Router Makefile

.PHONY: help install test lint build run docker-build docker-run k8s-deploy k8s-clean argocd-install

# Default target
help:
	@echo "Available commands:"
	@echo "  install      - Install dependencies"
	@echo "  test         - Run tests"
	@echo "  lint         - Run linting"
	@echo "  build        - Build the application"
	@echo "  run          - Run the application locally"
	@echo "  docker-build - Build Docker image"
	@echo "  docker-run   - Run with Docker Compose"
	@echo "  k8s-deploy   - Deploy to Kubernetes"
	@echo "  k8s-clean    - Clean Kubernetes resources"
	@echo "  argocd-install - Install ArgoCD"

# Development
install:
	uv sync

test:
	uv run pytest tests/ -v

lint:
	uv run ruff check

lint-fix:
	uv run ruff check --fix

build:
	uv sync

run:
	uv run uvicorn model_router.main:app --host 0.0.0.0 --port 8000 --reload

# Docker
docker-build:
	docker build -t model-router:latest .

docker-run:
	docker-compose up -d

docker-logs:
	docker-compose logs -f model-router

docker-stop:
	docker-compose down

# Kubernetes
k8s-deploy:
	kubectl apply -f devops/k8s/applications/

k8s-clean:
	kubectl delete -f devops/k8s/applications/

k8s-logs:
	kubectl logs -f deployment/model-router -n model-router

k8s-port-forward:
	kubectl port-forward svc/model-router-service -n model-router 8080:80

# ArgoCD
argocd-install:
	kubectl apply -f devops/k8s/infra/argocd-namespace.yaml
	kubectl apply -k devops/k8s/infra/
	@echo "Waiting for ArgoCD to be ready..."
	kubectl wait --for=condition=available --timeout=300s deployment/argocd-server -n argocd
	@echo "Getting ArgoCD admin password:"
	kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d
	@echo ""
	@echo "Access ArgoCD at: http://localhost:8080"
	@echo "Run: kubectl port-forward svc/argocd-server -n argocd 8080:443"

argocd-deploy-app:
	kubectl apply -f devops/k8s/infra/model-router-application.yaml

# CI/CD
check-ci:
	@echo "Running CI checks locally..."
	make lint
	make test
	make docker-build
	@echo "✅ All CI checks passed!"

# Release
tag:
	@read -p "Enter version (e.g., v1.0.0): " version; \
	git tag -a $$version -m "Release $$version"; \
	git push origin $$version

# Cleanup
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -name "*.pyc" -delete
	find . -name "*.pyo" -delete
	find . -name ".coverage" -delete
	rm -rf .pytest_cache/
	rm -rf htmlcov/

# Development environment
dev-setup:
	@echo "Setting up development environment..."
	make install
	make lint-fix
	make test
	@echo "✅ Development environment ready!"

# Production checks
prod-check:
	@echo "Running production readiness checks..."
	@echo "Checking Kubernetes manifests..."
	kubeval devops/k8s/applications/*.yaml || echo "Install kubeval for manifest validation"
	@echo "Checking Docker build..."
	make docker-build
	@echo "✅ Production checks completed!"