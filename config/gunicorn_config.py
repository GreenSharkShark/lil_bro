bind = "0.0.0.0:8000"
module = "aurigaone.wsgi:application"

workers = 1  # Adjust based on your server's resources
worker_connections = 1000
threads = 4
