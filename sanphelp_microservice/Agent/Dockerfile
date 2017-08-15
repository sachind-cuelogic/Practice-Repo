 FROM faizanscuelogic/python-2.7
 ENV PYTHONUNBUFFERED 1
 RUN mkdir /Agent
 WORKDIR /Agent
 RUN apt-get -y update
 RUN apt-get -y install curl wget make gcc build-essential
 RUN apt-get install -y python-dev
 RUN apt-get install -y supervisor
 RUN apt-get install -y nginx
 RUN pip install gunicorn
 RUN pip install setproctitle
 ADD requirements.txt /Agent/
 RUN pip install -r requirements.txt
 ADD . /Agent/
 COPY docker-entrypoint.sh /Agent/
 RUN chmod u+x docker-entrypoint.sh
 RUN chmod u+x bin/gunicorn_start  
 COPY agent.conf /etc/nginx/sites-available/
 RUN ln -s /etc/nginx/sites-available/agent.conf /etc/nginx/sites-enabled
 COPY agent_supervisor.conf  /etc/supervisor/conf.d/
 EXPOSE 80
 RUN mkdir -p /Agent/logs
 RUN mkdir -p /static
 RUN mkdir -p /Agent/static
 RUN chmod -R 777 /static
 RUN touch /Agent/logs/gunicorn_supervisor.log
 RUN python manage.py migrate
 ENTRYPOINT ["bash", "/Agent/docker-entrypoint.sh"]
