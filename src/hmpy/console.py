# src/hypermodern_python/console.py
import textwrap  # wrap lines when printing text

import click     # create CLI interfaces
import requests  # perform HTTP requests

from . import __version__
from . import get_os_language


# URL from Wikipedia REST API that returns the summary of a random Wikipedia
# article.
API_URL = "https://%s.wikipedia.org/api/rest_v1/page/random/summary"

@click.command()
@click.version_option(version=__version__)
@click.option("-l", "--language", default=get_os_language(), help=("Choose language (default: %s)" % get_os_language()))

def get_random_summary(language="en"):
    """Get a random Wikipedia article summary in the specified language"""

    try:
        response = requests.get(API_URL % language)
        response.raise_for_status()
        data = response.json()

        title = data["title"]
        extract = data["extract"]

        click.secho(title, fg="green")
        click.echo(textwrap.fill(extract))

    except requests.exceptions.ConnectionError as ce:
        click.secho("Connection error", fg="red")
        click.echo("Unable to connect to Wikipedia. Does your computer have internet access?")
        raise SystemExit(ce)
    except requests.exceptions.Timeout as te:
        click.secho("Timeout error", fg="red")
        click.echo("It took to long to get a response from Wikipedia. The service may be down.")
        raise SystemExit(te)
    except requests.exceptions.RequestException as re:
        click.secho("Error", fg="red")
        click.echo("Unable to process the request.")
        raise SystemExit(re)


def main():
    """Show the summary of a random Wikipedia article."""
    get_random_summary()
