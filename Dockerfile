FROM centos:8

WORKDIR /usr/src/app
COPY . .

# Set environment variables for SQL Server libraries to work
RUN source /usr/src/app/requirements.sh

EXPOSE 443
CMD ["gunicorn", "-b", "0.0.0.0:443", "--certfile=ssl/intaxlligence-crt", "--keyfile=ssl/intaxlligence-key", "--workers", "4", "main:app"]
