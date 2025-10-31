#!/usr/bin/env bash
set -e
sudo yum update -y
sudo amazon-linux-extras enable nginx1
sudo yum install -y nginx git python3 python3-pip
sudo mkdir -p /opt/clientes-app
sudo chown ec2-user:ec2-user /opt/clientes-app
sudo tee /etc/nginx/conf.d/clientes.conf >/dev/null <<'NGINX'
server {
  listen 80;
  server_name _;
  location / {
    proxy_pass http://127.0.0.1:8000;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
  }
}
NGINX
sudo systemctl enable nginx --now
sudo systemctl restart nginx
echo "Bootstrap listo. Sube el código y activa el servicio systemd."
