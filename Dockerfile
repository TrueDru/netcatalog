# Use alpine-based python image
FROM python:3-alpine3.20

# Set workdir
WORKDIR /opt

# Install deps
COPY ./net-catalog/requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy app
COPY ./net-catalog .

# Run app
ENTRYPOINT ["gunicorn", "-w", "4", "-b", "0.0.0.0:8080", "app:app"]