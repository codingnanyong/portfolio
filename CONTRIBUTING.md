# Contributing Guidelines

Thank you for your interest in contributing to the IoT Sensor Monitoring Data Platform portfolio project. This document provides guidelines for contributing.

## Getting Started

### Prerequisites

- Docker & Docker Compose (for data pipeline)
- Python 3.10+
- Kubernetes (Kind or similar) for microservices
- PostgreSQL / TimescaleDB

### Project Structure

- `data_pipeline/` — Apache Airflow DAGs, ETL workflows, DB hooks
- `flet_montrg/` — FastAPI microservices for real-time monitoring, alerts, aggregation

## How to Contribute

### Reporting Issues

- Use the [Issue templates](.github/ISSUE_TEMPLATE/) for bug reports or feature requests
- Search existing issues before creating a new one
- Provide clear steps to reproduce for bugs
- Include environment details (OS, Python version, Docker version, etc.) where relevant

### Pull Requests

1. **Fork** the repository and create a branch from `main`
2. **Make changes** following existing code style and conventions
3. **Test** locally (run DAGs, services, or tests as applicable)
4. **Commit** with clear, descriptive messages
5. **Open a PR** using the [Pull Request template](.github/PULL_REQUEST_TEMPLATE.md)
6. Reference any related issues in the PR description

### Code Style

- **Python**: Follow PEP 8; use type hints where possible
- **API (FastAPI)**: Use Pydantic models, async where appropriate
- **YAML/Kubernetes**: Keep formatting consistent with existing manifests

### Documentation

- Update README files when adding new services, DAGs, or configuration
- Add docstrings for new functions and modules
- Document environment variables and configuration options

## Development Setup

### Data Pipeline (Airflow)

```bash
cd data_pipeline
docker compose up -d
# Access Airflow UI and run DAGs as needed
```

### Microservices

See each service's README under `flet_montrg/services/` for run instructions (Docker, Kubernetes, or local).

## Questions?

- Open a [Discussion](https://github.com/codingnanyong/portfolio/discussions) for general questions
- Contact: codingnanyong@gmail.com

Thanks for contributing!
