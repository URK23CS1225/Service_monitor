# Terraform configuration to provision a VM, install Docker, and run the container

terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "us-east-1"
}

# User data script: installs Docker and runs the container
locals {
  user_data = <<-EOF
    #!/bin/bash
    apt-get update -y
    apt-get install -y docker.io
    systemctl start docker
    systemctl enable docker
    docker run -d -p 5000:5000 service-monitor:latest
  EOF
}

# EC2 instance (generic VM)
resource "aws_instance" "service_monitor_vm" {
  ami           = "ami-0c02fb55956c7d316" # Amazon Linux 2 (us-east-1)
  instance_type = "t2.micro"
  user_data     = local.user_data

  tags = {
    Name = "service-monitor-vm"
  }
}

output "instance_public_ip" {
  value = aws_instance.service_monitor_vm.public_ip
}
