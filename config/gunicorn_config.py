bind = "0.0.0.0:8000"
module = "aurigaone.wsgi:application"

workers = 1 
worker_connections = 1000
threads = 4
