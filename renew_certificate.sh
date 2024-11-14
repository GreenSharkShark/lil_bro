#!/bin/bash

docker-compose -f docker-compose-prod.yml run certbot renew --force-renewal
docker-compose -f docker-compose-prod.yml restart nginx
