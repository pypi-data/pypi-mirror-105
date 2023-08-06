import click
import time
import os
import logging
import sys
from .account import Account, ComputeStatus

logging.basicConfig(stream=sys.stdout, level=os.environ.get('LOGLEVEL', 'INFO').upper())

logger = logging.getLogger(__name__)

url_help = "X"
name_lower = "aero"
name_upper = "Aero"

def echo(line, **kwargs):
    click.secho(line, **kwargs)

def cyan(string):
    return click.style(string, fg='cyan')

def magenta(string):
    return click.style(string, fg='magenta')

@click.group()
def cli():
    pass

@cli.group(help="Account management")
def account():
    pass

@account.command(help="Login to an account")
def login():
    echo(f'Welcome to {magenta(name_upper)}! Follow the prompts to login.')

    email = click.prompt("Enter your email: ")
    password = click.prompt("Enter your password: ", hide_input=True)

    try:
        account = _login(email, password)
    except Exception as e:
        echo("An error occured when attempting to log in, please try again")
        logger.debug(e)
        return

    # TODO: Check if already provisioned. AWS creds need refreshing though.
    try:
        _provision(account)
    except Exception as e:
        echo("An error occured when attempting to provision, please try again")
        logger.debug(e)

    return

@account.command(help="Create an account")
def create():

    echo(f'Welcome to {magenta(name_upper)}! Follow the prompts to create an account.')

    email = click.prompt("Enter your email.")
    password = ""

    not_matching = True

    while not_matching:

        password = click.prompt("Enter your password: ", hide_input=True)
        password_confirmation = click.prompt("Confirm password: ", hide_input=True)

        if password != password_confirmation:
            echo("Passwords don't match, try again")
        else:
            # Passwords now match
            not_matching = False

    try:
        Account.create(email, password)
    except Exception as e:

        if str(e) == "409":
            echo("A user already exists with this Email")
        elif str(e) == "404":
            echo("An error has occurred connecting to our endpoint")
        else:
            echo("An error has occurred")

        logger.debug(e)
     
        return
    
    echo("Account Created!")

    try:
        account = _login(email, password)
    except Exception as e:
        echo("An error occured when attempting to log in, please try again")
        logger.debug(e)
        return

    try:
        _provision(account)
    except Exception as e:
        echo("An error occured when attempting to provision, please try again")
        logger.debug(e)

        return


def _login(email, password):

    try:
        acc = Account.login(email, password)
    except Exception as e:

        if str(e) == "403":
            echo("Incorrect email/password")
        elif str(e) == "404":
            echo("User doesnt exist")
        else:
            echo("An error has occurred")
    
    echo("Login Successful")

    return acc

def _provision(account):

    status = ComputeStatus.NO_VALUE
    i = 0

    while status != ComputeStatus.CREATED:
        status = account.provision()
        logger.debug(f"Current Status is {status}, iteration {i}")

        if status == ComputeStatus.INIT:
            echo(f"Initialised Compute Pool Creation")

        if status == ComputeStatus.CREATING:
            echo(f"Creating Compute Pool...")   
    
        if status == ComputeStatus.CREATED:
            echo(f"Compute Pool Created")
            echo(f"You are now ready to run Metaflow Flows through Aero. For more, read here: {url_help}")
            break  

        time.sleep(60)
        i += 1
