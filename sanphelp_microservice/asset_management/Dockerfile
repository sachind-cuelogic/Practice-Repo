 FROM faizanscuelogic/python-2.7
 ENV PYTHONUNBUFFERED 1
 RUN mkdir /asset_management
 WORKDIR /asset_management
 RUN apt-get -y update
 RUN apt-get -y install curl wget make gcc build-essential
 RUN apt-get install -y python-dev
 RUN apt-get install -y supervisor
 RUN apt-get install -y nginx
 RUN pip install gunicorn
 RUN pip install setproctitle
 ADD requirements.txt /asset_management/
 RUN pip install -r requirements.txt
 ADD . /asset_management/
 COPY docker-entrypoint.sh /asset_management/
 RUN chmod u+x docker-entrypoint.sh
 RUN chmod u+x bin/gunicorn_start  
 COPY asset_management.conf /etc/nginx/sites-available/
 RUN ln -s /etc/nginx/sites-available/asset_management.conf /etc/nginx/sites-enabled
 COPY asset_management_supervisor.conf  /etc/supervisor/conf.d/
 EXPOSE 80
 RUN mkdir -p /asset_management/logs
 RUN mkdir -p /static
 RUN mkdir -p /asset_management/static
 RUN chmod -R 777 /static
 RUN touch /asset_management/logs/gunicorn_supervisor.log
 RUN python manage.py migrate
 CMD ["bash", "/asset_management/docker-entrypoint.sh"]
