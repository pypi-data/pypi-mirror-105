import os
import click

from energinetml.cli.utils import discover_model
from energinetml.core.docker import build_webapp_docker_image


@click.command()
@click.option('--tag', '-t', required=True,
              help='Name and optionally a tag in the ‘name:tag’ format')
def build(tag):
    """
    Build a Docker image with a HTTP web API for model prediction.
    \f

    :param str tag:
    """
    build_webapp_docker_image(path=os.path.join(os.getcwd(), 'src'), tag=tag)
