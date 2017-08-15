#!/bin/bash
set -e
python manage.py collectstatic <<<yes

echo "Starting Supervisor"
service supervisor start
echo "Starting Supervisor Services"
supervisorctl restart all
echo "Starting Nginx"
service nginx stop
echo "microservice running on $public_ip"
sed -i 's/server_name $hostname;/server_name '$public_ip';/g' /etc/nginx/sites-available/user_service.conf
nginx -g 'daemon off;'

exec "$@"
