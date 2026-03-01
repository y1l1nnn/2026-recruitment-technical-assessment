# Docker & Kubernetes Assessment Report

> [!TIP]
> Use this document to explain your design choices, optimisations and any challenges you faced.

## Dockerfile

<!-- Explain any specific goals or design decisions -->
Recommended to use a multi-stage build for a Fastify server in TS -> this creates smaller/secure final image by separating TS compilation from the runtime environment

1. BUILD STAGE - `node:20-alpine` for smaller image
2. PRODUCTION STAGE - add non-root user to run app to reduce security risks

### Forked repository

<!-- If you submitted your changes to a fork, replace with your forked repository -->
`https://github.com/y1l1nnn/2026-recruitment-technical-assessment/tree/main/platforms/docker-kubernetes/unsw-calendar-api`

## Kubernetes

<!-- Document your process for deploying Navidrome on Kubernetes -->
