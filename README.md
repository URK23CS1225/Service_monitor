# Service Monitoring Dashboard

A Flask-based web app to monitor service URLs and display their status (UP/DOWN) and response time.

---

## Project Structure

```
dev_pro/
├── app/
│   └── main.py
├── templates/
│   └── index.html
├── tests/
│   └── test_api.py
├── k8s/
│   ├── deployment.yaml
│   └── service.yaml
├── ansible/
│   ├── playbook.yml
│   └── inventory.ini
├── terraform/
│   └── main.tf
├── .github/
│   └── workflows/
│       └── ci.yml
├── Dockerfile
├── requirements.txt
└── README.md
```

---

## Setup on Ubuntu

```bash
git clone https://github.com/URK23CS1225/Service_monitor.git
cd dev_pro
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app/main.py
```

Visit `http://localhost:5000`

---

## Run Tests

```bash
pytest tests/
```

---

## Docker

```bash
docker build -t service-monitor:latest .
docker run -d -p 5000:5000 service-monitor:latest
```

---

## CI/CD

Triggers automatically on every push to `main`. Runs tests and builds the Docker image via GitHub Actions.

---

## Kubernetes

```bash
minikube start
minikube image load service-monitor:latest
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
```

App accessible at `http://192.168.49.2:30080`

---

## Ansible

```bash
ansible-playbook ansible/playbook.yml -i ansible/inventory.ini -K
```

Installs Docker and runs the container on the target server.
