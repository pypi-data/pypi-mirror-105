import os

import click

from wipeit.models import AuthorizedClient
from wipeit.utils import const


@click.command()
def logout(*args, **kwargs):
    """Remove Reddit credentials from wipeit, you will be prompted to login the next time the program is run."""
    file_loc = AuthorizedClient(const.SCOPES, skip_login=True).refresh_token_filename
    if os.path.isfile(file_loc):
        os.remove(file_loc)
    click.echo("Successfully logged out.")
    click.echo("")
