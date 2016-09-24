"""
Test for spider feeder.
Prerequisites: The Source table is empty.
"""

import pytest

from worldbrain.cortex.models import Source, SourceStates
from worldbrain.cortex.management.commands.feedspider import Command

TEST_DOMAIN_NAME = 'funnymals.org'


def create_source():
    source = Source(domain_name=TEST_DOMAIN_NAME)
    source.save()


def get_source():
    create_source()
    return Source.objects.get(domain_name=TEST_DOMAIN_NAME)


@pytest.mark.django_db
def test_feedspider():

    source = get_source()
    source.ready()
    source.save()

    command = Command()

    success = True
    sources = []

    try:
        command.handle()
        sources = [source.domain_name for source in command.all_sources]
    except:
        success = False

    # Test whether the feeder was able to send the source to RabbitMQ
    assert success

    # Test whether exactly the newly created and as ready marked source
    # has been sent to RabbitMQ
    assert sources == ['funnymals.org']
