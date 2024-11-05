"""
main.py

This is the entry point for the CLI application that manages Microsoft Fabric workspaces.

Author: Danny de Bree
Date: 05/11/2024
"""

from fabric_cli.fabric import create_workspace, get_workspaces, provision_identity
import click

@click.command()
@click.option('--create', multiple=True, help="List of display names for new workspaces. Usage: --create 'name' --capacity_id 'id'")
@click.option('--capacity_id', help="Capacity ID for the new workspaces", required=True, hidden=True)
@click.option('--get', is_flag=True, help="Get existing workspaces")
def main(create, capacity_id, get):
    """Manage Microsoft Fabric workspaces.
    Before starting, ensure set environment variable "POWER_BI_ACCESS_TOKEN" with the token value.
    """
    created_workspace_ids = []

    # Create workspaces if names are provided
    if create:
        for display_name in create:
            try:
                workspace_id = create_workspace(display_name, capacity_id)
                if workspace_id:
                    created_workspace_ids.append(workspace_id)
                    click.echo(f"Successfully created workspace '{display_name}' with ID: {workspace_id}")
                else:
                    click.echo(f"Failed to create workspace '{display_name}'.")
            except Exception as e:
                click.echo(f"Error creating workspace '{display_name}': {e}")

    # Get existing workspaces if requested
    if get:
        try:
            workspaces = get_workspaces()
            for workspace_id, display_name in workspaces:
                click.echo(f"Workspace ID: {workspace_id}, Display Name: {display_name}")
        except Exception as e:
            click.echo(f"Error retrieving workspaces: {e}")

    # Provision identity for each created workspace
    for workspace_id in created_workspace_ids:
        provision_identity(workspace_id)

if __name__ == "__main__":
    main()
