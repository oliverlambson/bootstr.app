# bootstr.app

A template for a fully-featured python monolith containing multiple libraries and applications.

- Uses uv's workspaces to separate libraries and applications.
- Deployment to ECS.
- All CI/CD scripts in bash for portability.

## Prerequisites

Only [uv](https://docs.astral.sh/uv/getting-started/installation/).

## Deployment

- Every merge to main creates a release image published to ECR.
- Every merge to main changing `deployment/**` creates an AWS CodeDeploy release of the ECS service(s).
