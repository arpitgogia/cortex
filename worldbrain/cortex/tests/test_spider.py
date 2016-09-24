import pytest
import pika
from worldbrain.cortex.daemons.spider import *

# Set up RabbitMQ connection
SPIDER_QUEUE = 'worldbrain-spider'
CREDENTIALS = pika.PlainCredentials('worldbrain', 'worldbrain')
CONNECTION_PARAMETERS = pika.ConnectionParameters('polisky.me', 5672,
                                                  '/worldbrain', CREDENTIALS)


def test_domain_consumer():
    success = True

    try:
        domain_consumer = DomainConsumer()
        domain_consumer.test_run()
    except Exception as e:
        success = False

    assert success


@pytest.mark.django_db
def test_run_spider():

    success = True
    domain_name = 'funnymals.org'

    try:
        run_spider(domain_name)
    except Exception as e:
        success = False

    assert success
