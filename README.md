# Service Monitoring Dashboard

A simple web app built with Flask to monitor service URLs and display their status (UP/DOWN) and response time.

---

## Project Structure

```
dev_pro/
├── app/
│   └── main.py          # Flask application
├── templates/
│   └── index.html       # Dashboard UI
├── tests/
│   └── test_api.py      # Pytest tests
├── k8s/
│   ├── deployment.yaml  # Kubernetes Deployment
│   └── service.yaml     # Kubernetes Service (NodePort)
├── terraform/
│   └── main.tf          # Terraform IaC
├── .github/
│   └── workflows/
│       └── ci.yml       # GitHub Actions CI/CD
├── Dockerfile
├── requirements.txt
└── README.md
```

---

## Setup on Ubuntu

### 1. Clone the repo and create a virtual environment

```bash
git clone <your-repo-url>
cd dev_pro

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Run the app

```bash
python app/main.py
```

Visit `http://localhost:5000` in your browser.

---

## Running Tests

```bash
source venv/bin/activate
pytest tests/
```

---

## Docker

### Build and run the container

```bash
docker build -t service-monitor:latest .
docker run -d -p 5000:5000 service-monitor:latest
```

Visit `http://localhost:5000`.

---

## CI/CD (GitHub Actions)

The workflow in `.github/workflows/ci.yml` triggers on every push to `main`:
1. Installs Python dependencies
2. Runs pytest tests
3. Builds the Docker image

---

## Kubernetes

Apply the manifests to your cluster:

```bash
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
```

The app is exposed via NodePort on port `30080`.

---

## Terraform

Provisions an AWS EC2 VM, installs Docker, and runs the container:

```bash
cd terraform
terraform init
terraform apply
```

The public IP of the VM is shown as output after apply.
