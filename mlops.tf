# Variables
variable "aws_region" {
  default = "us-east-1"  # Change to your desired AWS region
}

variable "instance_type" {
  default = "t2.micro"
}

variable "key_name" {
  default = "my-key-pair"  # Replace with your actual key pair name
}

variable "app_port" {
  default = 8080
}

# Provider
provider "aws" {
  region = var.aws_region
}

# Security Group
resource "aws_security_group" "flask_app_sg" {
  name        = "flask-app-sg"
  description = "Allow traffic to Flask application"

  ingress {
    from_port   = var.app_port
    to_port     = var.app_port
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# EC2 Instance
resource "aws_instance" "flask_app_instance" {
  ami           = "ami-0c02fb55956c7d316"  # Amazon Linux 2 AMI (update if necessary)
  instance_type = var.instance_type
  key_name      = var.key_name
  security_groups = [aws_security_group.flask_app_sg.name]

  user_data = <<-EOF
              #!/bin/bash
              yum update -y
              amazon-linux-extras enable python3.8
              yum install python3.8 -y
              yum install git -y

              # Install Flask app dependencies
              pip3 install flask pandas scikit-learn joblib

              # Clone application repository
              git clone https://github.com/your-repo/flask-app.git /home/ec2-user/flask-app

              # Navigate to app directory
              cd /home/ec2-user/flask-app

              # Start Flask app
              FLASK_APP=app.py flask run --host=0.0.0.0 --port=${var.app_port} &
              EOF

  tags = {
    Name = "FlaskAppInstance"
  }
}

# Outputs
output "instance_public_ip" {
  value = aws_instance.flask_app_instance.public_ip
  description = "Public IP of the Flask app EC2 instance."
}

output "app_url" {
  value = "http://${aws_instance.flask_app_instance.public_ip}:${var.app_port}"
  description = "URL to access the Flask application."
}
