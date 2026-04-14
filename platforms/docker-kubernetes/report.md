# Docker & Kubernetes Assessment Report

> [!TIP]
> Use this document to explain your design choices, optimisations and any challenges you faced.

## Dockerfile

<!-- Explain any specific goals or design decisions -->
Recommended to use a multi-stage build for a Fastify server in TS -> this creates smaller/secure final image by separating TS compilation from the runtime environment

1. BUILD STAGE - `node:24-alpine` for smaller image
2. PRODUCTION STAGE - add non-root user to run app to reduce security risks

`.dockerignore` excludes files not needed to send to Docker daemon to build & run container -> speeds up builds & prevents accidentally leaking sensitive files

Challenges - working with engine constraints (node 24) & pnpm + managing ownership to appuser    

The application writes a cache file at runtime.
After switching to a non-root container user for security, the process no longer had permission to create /app/cache.
I resolved this by explicitly assigning ownership of the working directory to the application user (chown -R appuser:appgroup /app) before dropping privileges.
This preserves least-privilege execution while allowing required runtime writes.

### Forked repository

<!-- If you submitted your changes to a fork, replace with your forked repository -->
`https://github.com/y1l1nnn/2026-recruitment-technical-assessment/tree/main/platforms/docker-kubernetes/unsw-calendar-api`

## Kubernetes

<!-- Document your process for deploying Navidrome on Kubernetes -->
Translate Docker Compose file -> Kubernetes (manifests)

restart -> `deployment.yaml` declares deployment state (for `deluan/navidrome:latest`)
ports -> `service.yaml` defines ClusterIP service that exposes port 4533 internally and accessed locally via `kubectl port-forward`
volumes -> `pvc.yaml` persistent volume claim for data specifying storage size (1Gi)

The Deployment manages the pod lifecycle and ensures the container is always running.
The Service provides a stable internal network endpoint.
The PersistentVolumeClaim allows Navidrome data to persist across pod restarts.

Challenges 
- ClusterIP (internal) vs NodePort (external)
    - ClusterIP recommended for local access via port forwarding, more secure and there's no need to assign a static node port
- `music` is `emptyDir` 
    - should replace with `hostPath` for music library
- testing for persistence by deleting running pod -> waiting for new pod -> checking acc data still exists (PVC backed)
