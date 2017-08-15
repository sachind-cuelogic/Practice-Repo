 FROM faizanscuelogic/python-2.7
 ENV PYTHONUNBUFFERED 1
 RUN mkdir /comment_service
 WORKDIR /comment_service
 RUN apt-get -y update
 RUN apt-get -y install curl wget make gcc build-essential
 RUN apt-get install -y python-dev
 RUN apt-get install -y supervisor
 RUN apt-get install -y nginx
 RUN pip install gunicorn
 RUN pip install setproctitle
 ADD requirements.txt /comment_service/
 RUN pip install -r requirements.txt
 ADD . /comment_service/
 COPY docker-entrypoint.sh /comment_service/
 RUN chmod u+x docker-entrypoint.sh
 RUN chmod u+x bin/gunicorn_start  
 COPY comment_service.conf /etc/nginx/sites-available/
 RUN ln -s /etc/nginx/sites-available/comment_service.conf /etc/nginx/sites-enabled
 COPY comment_service_supervisor.conf  /etc/supervisor/conf.d/
 EXPOSE 80
 RUN mkdir -p /comment_service/logs
 RUN mkdir -p /static
 RUN mkdir -p /comment_service/static
 RUN chmod -R 777 /static
 RUN touch /comment_service/logs/gunicorn_supervisor.log
 RUN python manage.py migrate
 ENTRYPOINT ["bash", "/comment_service/docker-entrypoint.sh"]
