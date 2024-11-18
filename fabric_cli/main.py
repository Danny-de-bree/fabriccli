"""
main.py

This is the entry point for the CLI application that manages Microsoft Fabric workspaces.

Author: Danny de Bree
Date: 05/11/2024
"""

import click
from .auth import Auth
from .fabric import create_workspace, get_workspaces, provision_identity

@click.group()
def main():
    """Fabric CLI tool"""
    pass

@main.command()
@click.option('--token', '-t', required=True, help="Power BI access token")
def login(token):
    """Login to Microsoft Fabric"""
    try:
        auth = Auth()
        auth.set_token(token)
        click.echo("Successfully logged in")
    except Exception as e:
        click.echo(f"Error logging in: {e}")

@click.group()
def provision():
    """Provision resources for Microsoft Fabric"""
    pass

@main.command()
@click.option('--create', multiple=True, help="List of display names for new workspaces")
@click.option('--capacity_id', help="Capacity ID for new workspaces", required=True, hidden=True)
def workspace(create, capacity_id, get):
    """Manage Microsoft Fabric workspaces"""
    auth = Auth()
    
    if create:
        for name in create:
            try:
                workspace_id = create_workspace(name, auth, capacity_id)
                click.echo(f"Created workspace '{name}' with ID: {workspace_id}")
            except Exception as e:
                click.echo(f"Error creating workspace '{name}': {e}")


@main.group()
def display():
    """Display Microsoft Fabric resources"""
    pass

@display.command(name='workspaces')
def list_workspaces():
    """List all workspaces"""
    auth = Auth()
    try:
        spaces = get_workspaces(auth)
        if not spaces:
            click.echo("No workspaces found")
            return
        click.echo("\nWorkspaces:")
        for id, name in spaces:
            click.echo(f"  • {name} (ID: {id})")
    except Exception as e:
        click.echo(f"Error listing workspaces: {e}")



if __name__ == '__main__':
    main()