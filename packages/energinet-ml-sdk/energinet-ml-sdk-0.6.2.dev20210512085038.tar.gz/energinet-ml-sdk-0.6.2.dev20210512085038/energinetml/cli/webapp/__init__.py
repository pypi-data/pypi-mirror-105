import click

from .build import build as build_webapp


@click.group()
def webapp_group():
    """
    Manage Python Web Apps.
    """
    pass


webapp_group.add_command(build_webapp)
