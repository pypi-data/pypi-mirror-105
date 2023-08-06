import click
import sys
import getpass
from pyhectiqlab.auth import AuthProvider
from pyhectiqlab.artifacts import SharedArtifactsManager

def get_creds():
	username = input("Username: ")
	password = getpass.getpass(prompt='Password: ', stream=None) 
	return username, password

@click.group()
def cli():
    """Just a group."""
    pass

@cli.command()
def login():
	auth = AuthProvider()
	if auth.is_logged():
		click.echo("User is already logged in.")
		return

	username, password = get_creds()
	click.echo("Connecting...")
	success = auth.login_with_password(username, password)
	if success:
		click.echo("User is authentificated.")
	else:
		click.echo('Unsuccessful login.')

@cli.command()
def logout():
	auth = AuthProvider()
	auth.logout()
	click.echo('Logout completed.')

@cli.command()
def projects():	
	manager = SharedArtifactsManager()
	manager.list_projects()

@cli.command()
@click.option('--project_id', help='id of the project', required=True)
def artifacts(project_id):
	manager = SharedArtifactsManager()
	manager.select_artifact(project_id)

@cli.command()
@click.option('--project_id', help='id of the project', required=True)
@click.option('--filename', help='Name of the shared artifact', required=True)
def post_artifact(project_id, filename):
	manager = SharedArtifactsManager()
	click.echo('Pushing artifacts.')
	manager.push_artifact(filename, project_id)
	click.echo('Artifact pushed')