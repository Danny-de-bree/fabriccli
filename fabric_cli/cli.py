import click
from .auth import Auth
from .fabric import (
    create_workspace,
    get_workspaces,
    provision_workspace_identity,
    assign_workspace_to_capacity,
    create_lakehouse,
    get_lakehouses,
    create_warehouse,
    get_warehouses,
)


@click.group()
def main():
    """Fabric CLI tool"""
    pass


@main.command(hidden=True)
@click.option("--token", "-t", required=True, help="Power BI access token")
def login(token):
    """Login to Microsoft Fabric"""
    try:
        auth = Auth()
        auth.set_token(token)
        click.echo("Successfully logged in")
    except Exception as e:
        click.echo(f"Error logging in: {e}")


@main.group(name="create")
def create():
    """Create Fabric resources"""
    pass


@create.command()
@click.argument("name")
@click.option("--capacity-id", help="Capacity ID for the workspace")
@click.option(
    "--provision-identity", is_flag=True, help="Provision identity for the workspace after creation"
)
def workspace(name, capacity_id, provision_identity):
    """Create a new workspace"""
    try:
        auth = Auth()

        # Create workspace
        workspace_id = create_workspace(name, auth, capacity_id)
        click.echo(f"Created workspace '{name}' with ID: {workspace_id}")

        # If capacity ID provided, assign it
        if capacity_id:
            assign_workspace_to_capacity(workspace_id, capacity_id, auth)
            click.echo(f"Assigned workspace to capacity {capacity_id}")

        # Provision identity if requested
        if provision_identity:
            provision_workspace_identity(workspace_id, auth)
            click.echo(f"Successfully provisioned identity for workspace '{name}'")

        return workspace_id

    except Exception as e:
        click.echo(f"Error: {e}")
        return None


@create.command()
@click.argument("name")
@click.option("--workspace-id", required=True, help="Workspace ID where to create the lakehouse")
@click.option("--description", help="Optional description for the lakehouse")
def lakehouse(name, workspace_id):
    """Create a new lakehouse in a workspace"""
    try:
        auth = Auth()

        lakehouse_id = create_lakehouse(workspace_id, name, auth)
        click.echo(f"Created lakehouse '{name}' with ID: {lakehouse_id}")
        return lakehouse_id

    except Exception as e:
        click.echo(f"Error: {e}")
        return None


@create.command()
@click.argument("name")
@click.option("--workspace-id", required=True, help="Workspace ID where to create the warehouse")
def warehouse(name, workspace_id):
    """Create a new warehouse in a workspace"""
    try:
        auth = Auth()
        warehouse_id = create_warehouse(workspace_id, name, auth)
        click.echo(f"Created warehouse '{name}' with ID: {warehouse_id}")
        return warehouse_id
    except Exception as e:
        click.echo(f"Error: {e}")
        return None


@main.group()
def display():
    """Display Microsoft Fabric resources"""
    pass


@display.command(name="workspaces")
def list_workspaces():
    """List all workspaces"""
    auth = Auth()
    try:
        spaces = get_workspaces(auth)
        if not spaces:
            click.echo("No workspaces found")
            return

        click.echo("\nWorkspaces:")
        for workspace_id, display_name, capacity_id in spaces:
            capacity_info = f" (Capacity ID: {capacity_id})" if capacity_id else ""
            click.echo(f"  • {display_name} (ID: {workspace_id}){capacity_info}")
    except Exception as e:
        click.echo(f"Error listing workspaces: {e}")


@display.command(name="lakehouses")
@click.option("--workspace-id", required=True, help="Workspace ID to list lakehouses from")
@click.option("--workspace-id", required=True, help="Workspace ID to list lakehouses from")
def list_lakehouses(workspace_id):
    """List all lakehouses in a workspace"""
    auth = Auth()
    try:
        lakehouses = get_lakehouses(workspace_id, auth)
        if not lakehouses:
            click.echo(f"No lakehouses found in workspace {workspace_id}")
            return

        click.echo(f"\nLakehouses in workspace {workspace_id}:")
        for lakehouse_id, display_name in lakehouses:
            click.echo(f"  • {display_name} (ID: {lakehouse_id})")
    except Exception as e:
        click.echo(f"Error listing lakehouses: {e}")


@display.command(name="warehouses")
@click.option("--workspace-id", required=True, help="Workspace ID to list warehouses from")
@click.option("--workspace-id", required=True, help="Workspace ID to list warehouses from")
def list_warehouses(workspace_id):
    """List all warehouses in a workspace"""
    auth = Auth()
    try:
        warehouses = get_warehouses(workspace_id, auth)
        if not warehouses:
            click.echo(f"No warehouses found in workspace {workspace_id}")
            return

        click.echo(f"\nWarehouses in workspace {workspace_id}:")
        for warehouse_id, display_name in warehouses:
            click.echo(f"  • {display_name} (ID: {warehouse_id})")
    except Exception as e:
        click.echo(f"Error listing warehouses: {e}")


if __name__ == "__main__":
    main()
