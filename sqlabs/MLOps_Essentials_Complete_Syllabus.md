# MLOps Essentials: AI Lifecycle Management

**Duration:** 40 hours (8 sessions × 5 hours; approximately 30 hours of effective instruction)  
**Level:** Beginner  
**Format:** Short lectures, demonstrations, guided labs, and a final project  
**Prerequisites:** No prior Machine Learning experience. Basic Python and Git knowledge are helpful; starter code is provided.

## Course Introduction

Training a Machine Learning model is only the beginning. The bigger challenge is deploying it, keeping it reliable, and maintaining its prediction quality over time.

This course introduces **MLOps (Machine Learning Operations)**—the practices used to develop, automate, deploy, monitor, and maintain ML systems in production. Students will learn how DevOps principles extend to data and models through one beginner-friendly project.

## Course Syllabus

### Session 1 — Introduction to MLOps

**Goal:** Understand what MLOps is, why it exists, and how it relates to DevOps.

**Topics:**
- Software Development Lifecycle (SDLC), Waterfall, and Agile
- DevOps, CI/CD, automation, and monitoring
- AI vs. Machine Learning; training vs. inference
- MLOps challenges and the ML lifecycle
- CI/CD/Continuous Training (CT) at a high level

**Activity:** Discuss familiar ML applications and why a healthy API can still produce poor predictions.

### Session 2 — Machine Learning Fundamentals

**Goal:** Understand how to train and evaluate a simple ML model.

**Topics:**
- Datasets, samples, features, and labels
- Supervised learning; classification vs. regression
- Training, validation, testing, and generalization
- Overfitting; accuracy, precision, recall, and confusion matrix
- Making predictions on new examples

**Lab:** Explore data, train a simple classifier with scikit-learn, evaluate its predictions, and test custom inputs.

### Session 3 — Experiments & Model Management

**Goal:** Compare experiments and manage trained model versions.

**Topics:**
- Reproducibility and experiment tracking
- Parameters, metrics, and artifacts
- MLflow experiments and training runs
- Comparing models and choosing a candidate
- Introduction to the Model Registry

**Lab:** Run different training configurations, compare results in MLflow, and identify a candidate model.

### Session 4 — ML Pipelines & Automation

**Goal:** Turn manual model training into a repeatable workflow.

**Topics:**
- Notebooks vs. production execution
- Pipeline stages: load, validate, split, train, evaluate
- Why consistent preprocessing matters
- Basic data validation before training
- Automation and Continuous Training concepts

**Lab:** Build a simple training pipeline that **stops when required data is missing or invalid**.

### Session 5 — Model Deployment

**Goal:** Make a trained model available to other applications.

**Topics:**
- Training vs. inference; online vs. batch predictions
- REST APIs and JSON requests/responses
- Serving a model using FastAPI
- Docker fundamentals for ML applications
- Model versions and basic rollback concepts

**Lab:** Expose a prediction endpoint with FastAPI, test requests, and package the application with Docker.

### Session 6 — CI/CD for ML Systems

**Goal:** Automate testing and delivery of ML applications safely.

**Topics:**
- Git and CI/CD workflows for ML projects
- Automated code tests and pipeline checks
- **Model quality gates:** validating a candidate before promotion
- GitHub Actions fundamentals
- Secrets, approvals, and safe deployment practices

**Lab:** Build a GitHub Actions workflow that runs tests and blocks release if model quality falls below a defined threshold.

### Session 7 — Monitoring & Model Maintenance

**Goal:** Recognize when a deployed ML system needs attention.

**Topics:**
- Infrastructure and API monitoring vs. model monitoring
- Data quality, data drift, and concept drift
- Prediction-quality monitoring and delayed labels
- Retraining decisions and incident investigation
- Introduction to Evidently AI

**Lab:** Simulate changes in incoming data, generate a basic Evidently report, and discuss possible responses.

### Session 8 — AWS MLOps & Final Project

**Goal:** Connect the complete MLOps lifecycle to a practical cloud architecture.

**Topics:**
- AWS building blocks: S3, IAM, ECS, SageMaker, CloudWatch
- A simple end-to-end ML architecture on AWS
- Security, reliability, and cost considerations
- Brief introduction to LLMOps
- Review of the full lifecycle

**Final activity:** Demonstrate the course project and explain how it would be deployed and operated on AWS.

## Practical Project

Students gradually build an **SMS spam classifier** using a small labeled dataset and `scikit-learn`. Across the course they train and evaluate the model, track experiments with MLflow, automate a training pipeline, serve predictions through an API, add CI checks, and investigate simulated drift.

**Core tools:** Python, Google Colab, scikit-learn, MLflow, FastAPI, Docker, GitHub Actions, and Evidently AI. AWS is introduced mainly for architecture and deployment context.

## Assessment

| Component | Suggested Weight |
|---|---:|
| Short knowledge quizzes | 20% |
| Guided practical labs | 40% |
| Final project / demonstration | 40% |

## Expected Learning Outcomes

By the end of the course, students should be able to:
- Explain MLOps and its relationship to DevOps.
- Train, evaluate, and compare simple ML models.
- Understand experiment tracking, model versions, and training pipelines.
- Explain how model APIs, containers, and CI/CD support deployment.
- Identify data-quality and model-monitoring issues.
- Describe a basic production MLOps architecture on AWS.

**Scope:** Practical ML operations and lifecycle fundamentals—not advanced ML mathematics, deep learning, or complex Kubernetes deployments.
