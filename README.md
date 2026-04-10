# Service Monitoring Dashboard with DevOps Automation

---

## 1. Flask Web Application (Backend + UI)

**Purpose:**
To allow users to add service URLs and monitor their status (UP/DOWN) and response time.

**File: `app/main.py`**
```python
import time
import requests
from flask import Flask, request, jsonify, render_template

app = Flask(__name__, template_folder="../templates")
services = []

def check_service(url):
    try:
        start = time.time()
        response = requests.get(url, timeout=5)
        elapsed = round((time.time() - start) * 1000, 2)
        status = "UP" if response.status_code == 200 else "DOWN"
    except Exception:
        elapsed = 0
        status = "DOWN"
    return status, elapsed

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form.get("url", "").strip()
        if url:
            status, response_time = check_service(url)
            services.append({"url": url, "status": status, "response_time": response_time})
    return render_template("index.html", services=services)

@app.route("/check", methods=["POST"])
def check():
    data = request.get_json()
    if not data or "url" not in data:
        return jsonify({"error": "url is required"}), 400
    status, response_time = check_service(data["url"])
    return jsonify({"status": status, "response_time": response_time})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
```

---

## 2. Dockerfile (Containerization)

**Purpose:**
To containerize the Flask application.

**File: `Dockerfile`**
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app/ ./app/
COPY templates/ ./templates/
EXPOSE 5000
CMD ["python", "app/main.py"]
```

---

## 3. Pytest Tests (Testing)

**Purpose:**
To validate the `/check` API endpoint.

**File: `tests/test_api.py`**
```python
import json
import pytest
from app.main import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_check_missing_url(client):
    response = client.post("/check", data=json.dumps({}), content_type="application/json")
    assert response.status_code == 400

def test_check_down_service(client):
    payload = {"url": "http://localhost:19999"}
    response = client.post("/check", data=json.dumps(payload), content_type="application/json")
    assert response.get_json()["status"] == "DOWN"

def test_check_valid_url(client):
    payload = {"url": "https://httpbin.org/status/200"}
    response = client.post("/check", data=json.dumps(payload), content_type="application/json")
    assert response.get_json()["status"] in ("UP", "DOWN")
```

---

## 4. CI/CD Pipeline

**Purpose:**
To automate testing and Docker image build on every push to `main`.

**File: `.github/workflows/ci.yml`**
```yaml
name: CI/CD Pipeline
on:
  push:
    branches: [main]
jobs:
  build-and-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - run: pip install -r requirements.txt
      - run: pytest tests/
      - run: docker build -t service-monitor:latest .
```

---

## 5. Kubernetes (Orchestration)

**Purpose:**
To deploy and expose the app on a Kubernetes cluster.

**File: `k8s/deployment.yaml`**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: service-monitor
spec:
  replicas: 1
  selector:
    matchLabels:
      app: service-monitor
  template:
    metadata:
      labels:
        app: service-monitor
    spec:
      containers:
        - name: service-monitor
          image: service-monitor:latest
          imagePullPolicy: Never
          ports:
            - containerPort: 5000
```

**File: `k8s/service.yaml`**
```yaml
apiVersion: v1
kind: Service
metadata:
  name: service-monitor
spec:
  type: NodePort
  selector:
    app: service-monitor
  ports:
    - port: 5000
      targetPort: 5000
      nodePort: 30080
```

---

## 6. Ansible (Infrastructure as Code)

**Purpose:**
To automate Docker installation and container deployment on a server.

**File: `ansible/playbook.yml`**
```yaml
- name: Deploy Service Monitor
  hosts: servers
  become: true
  tasks:
    - name: Install Docker dependencies
      apt:
        name: [apt-transport-https, ca-certificates, curl, software-properties-common]
        state: present
        update_cache: true
    - name: Add Docker GPG key
      apt_key:
        url: https://download.docker.com/linux/ubuntu/gpg
    - name: Add Docker repository
      apt_repository:
        repo: deb https://download.docker.com/linux/ubuntu focal stable
    - name: Install Docker
      apt:
        name: docker-ce
        state: present
        update_cache: true
    - name: Start and enable Docker
      service:
        name: docker
        state: started
        enabled: true
    - name: Wait for Docker to be ready
      wait_for:
        path: /var/run/docker.sock
        timeout: 30
    - name: Run service-monitor container
      community.docker.docker_container:
        name: service-monitor
        image: service-monitor:latest
        state: started
        restart_policy: always
        ports:
          - "5000:5000"
```

---

## Setup on Ubuntu

```bash
# Clone and setup
git clone https://github.com/URK23CS1225/Service_monitor.git
cd dev_pro
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run app
python app/main.py

# Run tests
pytest tests/

# Docker
docker build -t service-monitor:latest .
docker run -d -p 5000:5000 service-monitor:latest

# Kubernetes (minikube)
minikube start
minikube image load service-monitor:latest
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml

# Ansible
ansible-playbook ansible/playbook.yml -i ansible/inventory.ini -K
```
