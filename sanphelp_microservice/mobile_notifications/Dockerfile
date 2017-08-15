 FROM faizanscuelogic/python-2.7
 ENV PYTHONUNBUFFERED 1
 RUN mkdir /mobile_notifications
 WORKDIR /mobile_notifications
 RUN apt-get -y update
 RUN apt-get -y install curl wget make gcc build-essential
 RUN apt-get install -y python-dev
 RUN apt-get install -y supervisor
 RUN apt-get install -y nginx
 RUN pip install gunicorn
 RUN pip install setproctitle
 ADD requirements.txt /mobile_notifications/
 RUN pip install -r requirements.txt
 ADD . /mobile_notifications/
 COPY docker-entrypoint.sh /mobile_notifications/
 RUN chmod u+x docker-entrypoint.sh
 RUN chmod u+x bin/gunicorn_start  
 COPY mobile_notifications.conf /etc/nginx/sites-available/
 RUN ln -s /etc/nginx/sites-available/mobile_notifications.conf /etc/nginx/sites-enabled
 COPY mobile_notifications_supervisor.conf  /etc/supervisor/conf.d/
 EXPOSE 80
 RUN mkdir -p /mobile_notifications/logs
 RUN mkdir -p /static
 RUN mkdir -p /mobile_notifications/static
 RUN chmod -R 777 /static
 RUN touch /mobile_notifications/logs/gunicorn_supervisor.log
 RUN python manage.py migrate
 CMD ["bash", "/mobile_notifications/docker-entrypoint.sh"]
