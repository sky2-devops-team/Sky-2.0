#!/usr/bin/env bash
set -e
cd /opt/clientes-app
python3 -m venv .venv || true
. .venv/bin/activate
pip install --upgrade pip
[ -f requirements.txt ] && pip install -r requirements.txt
sudo cp -f service/clientes.service /etc/systemd/system/clientes.service
sudo systemctl daemon-reload
sudo systemctl enable clientes --now
sudo systemctl restart clientes
