# Sky-2.0



Sky-2.0 — Fase II: Implementación en AWS + CI/CD + Mejora Continua

📌 Proyecto



Sky-2.0 — Fase II: despliegue en AWS EC2 de una API Python (Flask/SQLite) con Nginx + Gunicorn + systemd, CI/CD en GitHub Actions, flujos de issues y rollback por versiones.



Esta Fase II continúa lo construido en Fase I y agrega operación en la nube + automatización.



🎯 Objetivos



Publicar la app en AWS EC2 y hacerla accesible por HTTP.



Implementar CI (lint, seguridad, pruebas) y CD (deploy a EC2).



Definir flujos de trabajo con Issues (altas/cambios/consultas de clientes y mejoras).



Demostrar versionado y rollback con tags/releases.



🧩 Alcance → Entregables

Requisito	Entregable

App Python de clientes	API Flask + SQLite

CI (calidad y seguridad)	flake8, bandit, pytest en ci.yml

CD (deploy a EC2)	Workflow deploy.yml (Actions → EC2)

Flujos de Issues	issue-flows.yml + etiquetas (new/update/query-client, feature/enhancement/code-change)

Infra AWS	EC2 t2.micro, Amazon Linux 2, Nginx, Gunicorn, systemd

Acceso público	/health operativo desde IP/DOMINIO

Versionado/rollback	Tags/Releases + redeploy a una versión estable

🏗️ Arquitectura

Usuarios ──> Nginx (EC2) ──> Gunicorn ──> Flask (API) ──> SQLite (clientes.db)

&nbsp;                   ↑

&nbsp;           GitHub Actions (CI/CD)



📁 Estructura sugerida del repo

clientes-app/

├─ app/

│  ├─ app.py

│  ├─ db.py

│  ├─ models.py

│  └─ \_\_init\_\_.py

├─ tests/

│  └─ test\_app.py

├─ service/

│  └─ clientes.service

├─ scripts/

│  ├─ bootstrap\_ec2\_amzn2.sh

│  └─ deploy.sh

├─ .github/workflows/

│  ├─ ci.yml

│  ├─ issue-flows.yml

│  └─ deploy.yml

├─ requirements.txt

├─ clients.json

├─ README.md

└─ LICENSE



🔧 Requisitos previos



GitHub: repo con rama main; Secrets en Settings → Secrets and variables → Actions:



EC2\_HOST (IP pública o DNS de la instancia)



EC2\_SSH\_KEY (clave privada para ec2-user)



AWS:



EC2: Amazon Linux 2, tipo t2.micro, disco 8 GiB (gp3).



Security Group: Inbound 80/TCP (HTTP); 22/TCP (SSH) solo para tu IP.



Nginx instalado como reverse proxy a Gunicorn.



Local (opcional): Python 3.11+, Git.



▶️ Ejecución local (dev)

python -m venv .venv

\# Windows: .venv\\Scripts\\activate

\# Linux/Mac: source .venv/bin/activate

pip install -r requirements.txt

flask --app app.app run -p 8000

\# prueba: http://localhost:8000/health



✅ CI (calidad y seguridad)



Lint: flake8



Seguridad: bandit



Tests: pytest



Se ejecutan en cada push/PR por ci.yml.



🚀 CD (deploy a EC2)



En la EC2, preparar entorno (una sola vez):



sudo bash scripts/bootstrap\_ec2\_amzn2.sh





Instala Nginx, Python, configura reverse proxy a 127.0.0.1:8000.



Workflow deploy.yml (GitHub Actions) copia el repo vía SSH, instala dependencias, y reinicia el servicio systemd:



Servicio: service/clientes.service (Gunicorn, 2 workers, puerto 8000).



Verificación:



sudo systemctl status clientes



Navegador: http://<EC2\_PUBLIC\_IP>/health



🔁 Rollback (tags/releases)



Crear tag estable (ej. v1.0.0).



Si una versión falla, redeploy del tag estable:



Actions → Deploy to EC2 → Run workflow → ref: v1.0.0



Confirmar /health y systemctl status clientes.



🧪 Endpoints de la API



GET /health → {"status":"ok"}



GET /clients → Lista clientes



GET /clients/<id> → Cliente por ID



POST /clients → JSON: {nombre, email, telefono?, categoria?}



PUT /clients/<id> → Campos opcionales



DELETE /clients/<id> → Borrado



🏷️ Flujos de trabajo con Issues (etiquetas)



Usa estas etiquetas para automatizar respuestas y traza:



new-client, update-client, query-client



feature-request, enhancement, code-change



issue-flows.yml comenta en el issue y (si aplica) registra traza en clients.json.



👥 Roles (equipo / IAM sugerido)



Developers: código, PRs, pueden lanzar deploy con aprobación.



IT: infraestructura, Nginx/SSL, monitoreo, rollback.



Support: crea Issues funcionales (altas/cambios/consultas), confirma servicio.



📹 Evidencias (para la entrega)



Video 1: repo + PR + CI en verde + deploy desde Actions + /health en EC2.



Video 2: IAM (si aplica), CRUD desde Postman/cURL, simulación de falla y rollback a un tag estable.



Reporte (DOCX/PDF): arquitectura, pasos, capturas, pruebas, conclusiones.



📄 Licencia



MIT (o la que el curso indique).

