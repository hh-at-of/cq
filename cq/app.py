# CELERY_CONFIG_MODULE=cq.conf.default celery -A cq worker -E --loglevel=info

import os
from celery import Celery
import logging

# logger
logger = logging.getLogger(__name__)

# create celery application
#app = Celery('cq', broker='redis://guest@localhost//', backend='redis://localhost')
app = Celery('cq')

# configure
#app.config_from_envvar('CELERY_CONFIG_MODULE')
logger.info("configure celery")

app.conf.update({'BROKER_URL': 'amqp://cq:cQu3u3@10.0.52.24:5672/cq',
                 'CELERY_RESULT_BACKEND': 'rpc',
                 'AMQP_SERVER': '10.0.52.24',
                 'AMQP_PORT': 5672,
                 'AMQP_USER': "cq",
                 'AMQP_PASSWORD': "cQu3u3",
                 'AMQP_VHOST': "cq",
                 'CELERY_ACCEPT_CONTENT': ['pickle'],
                 'CELERY_RESULT_SERIALIZER': 'pickle',
                 'CELERY_TASK_SERIALIZER': 'pickle'})
##CELERY_QUEUES = (
##  Queue('default', Exchange('default'), routing_key='default'),
##  Queue('q1', Exchange('A'), routing_key='routingKey1'),
##  Queue('q2', Exchange('B'), routing_key='routingKey2'),
##)
##CELERY_ROUTES = {
## 'my_taskA': {'queue': 'q1', 'routing_key': 'routingKey1'},
## 'my_taskB': {'queue': 'q2', 'routing_key': 'routingKey2'},
##}

# register tasks
from cq.tasks import tasks
