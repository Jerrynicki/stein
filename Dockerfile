# Build Frontend
FROM node:20 as build
WORKDIR /app
COPY root/frontend/styn /app
RUN npm install
RUN npm run build

# Build Backend
FROM python:3.12-slim
WORKDIR /app
COPY root/backend/requirements.txt /app
RUN pip3 install -r requirements.txt
RUN pip3 install gunicorn
COPY --from=build /app/dist /app/dist
COPY root/backend/src/flask_app /app

EXPOSE 8000

# Start Gunicorn server
CMD ["gunicorn", "app:create_app()", "-b", "0.0.0.0:8000", "--access-logfile", "-", "--error-logfile", "-"]