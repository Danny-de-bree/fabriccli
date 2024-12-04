import click
import logging
from .auth import Auth, SPNConfig
from .workspaces import (
    create_workspace,
    get_workspaces,
    assign_workspace_to_capacity,
    provision_workspace_identity,
)
from .lakehouses import create_lakehouse, get_lakehouses
from .warehouses import create_warehouse, get_warehouses
from .git import connect_git_repository
from .capacity_management import suspend_capacity, resume_capacity
from .capacity import get_capacities
from .logging_config import setup_logging

# Configure logging
setup_logging()
logger = logging.getLogger(__name__)

# Create a single instance of Auth
auth = Auth()


@click.group()
def main():
    """🟠☁️   Welcome to the Fabric CLI Tool! 🟠☁️

    Manage your Microsoft Fabric resources with ease!

    Made by Danny de Bree with the help of Rubicon

    www.Rubicon.nl
    """  # I know strange outlining, but otherwise Click will not show the text
    pass


@main.command(hidden=True)
@click.option("--token", "-t", required=True, help="Power BI access token")
def login(token):
    """Login to Microsoft Fabric using a token"""
    try:
        auth.set_token(token, 3600)  # Assuming the token is valid for 1 hour
        click.echo("✅ Successfully logged in with token")
        logger.debug("Token login successful")
    except Exception as e:
        click.echo(f"❌ Error logging in: {e}")
        logger.error(f"Error logging in with token: {e}")


@main.command(hidden=True)
@click.option("--client-id", required=True, help="Azure AD Client ID")
@click.option("--client-secret", required=True, help="Azure AD Client Secret")
@click.option("--tenant-id", required=True, help="Azure AD Tenant ID")
def login_spn(client_id, client_secret, tenant_id):
    """Login to Microsoft Fabric using SPN"""
    try:
        logger.debug(f"Logging in with SPN: client_id={client_id}, tenant_id={tenant_id}")
        config = SPNConfig(client_id=client_id, client_secret=client_secret, tenant_id=tenant_id)
        auth.set_spn_config(config)

        click.echo("✅ Successfully logged in with SPN")
        logger.debug("SPN login successful")
    except Exception as e:
        click.echo(f"❌ Error logging in: {e}")
        logger.error(f"Error logging in with SPN: {e}")


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
        # Create workspace
        workspace_id = create_workspace(name, auth, capacity_id)
        click.echo(f"✅ Created workspace '{name}' with ID: {workspace_id}")
        logger.debug(f"Workspace created with ID: {workspace_id}")

        # If capacity ID provided, assign it
        if capacity_id:
            assign_workspace_to_capacity(workspace_id, capacity_id, auth)
            click.echo(f"✅ Assigned workspace to capacity {capacity_id}")
            logger.debug(f"Assigned workspace to capacity {capacity_id}")

        # Provision identity if requested
        if provision_identity:
            provision_workspace_identity(workspace_id, auth)
            click.echo(f"✅ Successfully provisioned identity for workspace '{name}'")
            logger.debug(f"Provisioned identity for workspace '{name}'")

        return workspace_id

    except Exception as e:
        click.echo(f"❌ Error: {e}")
        logger.error(f"Error creating workspace: {e}")
        return None


@create.command()
@click.argument("name")
@click.option("--workspace-id", required=True, help="Workspace ID where to create the lakehouse")
def lakehouse(name, workspace_id):
    """Create a new lakehouse in a workspace"""
    try:
        lakehouse_id = create_lakehouse(workspace_id, name, auth)
        click.echo(f"✅ Created lakehouse '{name}' with ID: {lakehouse_id}")
        logger.debug(f"Lakehouse created with ID: {lakehouse_id}")
        return lakehouse_id
    except Exception as e:
        click.echo(f"❌ Error: {e}")
        logger.error(f"Error creating lakehouse: {e}")
        return None


@create.command()
@click.argument("name")
@click.option("--workspace-id", required=True, help="Workspace ID where to create the warehouse")
def warehouse(name, workspace_id):
    """Create a new warehouse in a workspace !!not working with SPN!!"""
    try:
        warehouse_id = create_warehouse(workspace_id, name, auth)
        click.echo(f"✅ Created warehouse '{name}' with ID: {warehouse_id}")
        logger.debug(f"Warehouse created with ID: {warehouse_id}")
        return warehouse_id
    except Exception as e:
        click.echo(f"❌ Error: {e}")
        logger.error(f"Error creating warehouse: {e}")
        return None


@main.group()
def display():
    """Display Microsoft Fabric resources"""
    pass


@display.command(name="workspaces")
def list_workspaces():
    """Display all workspaces"""
    try:
        spaces = get_workspaces(auth)
        if not spaces:
            click.echo("⚠️ No workspaces found")
            return

        for workspace_id, display_name, capacity_id in spaces:
            capacity_info = f" (Capacity ID: {capacity_id})" if capacity_id else ""
            click.echo(f"  • {display_name} (ID: {workspace_id}){capacity_info}")
        logger.debug(f"Listed workspaces: {spaces}")
    except Exception as e:
        click.echo(f"❌ Error listing workspaces: {e}")
        logger.error(f"Error listing workspaces: {e}")


@display.command(name="lakehouses")
@click.option("--workspace-id", required=True, help="Workspace ID to list lakehouses from")
def list_lakehouses(workspace_id):
    """Display all lakehouses in a workspace"""
    try:
        lakehouses = get_lakehouses(workspace_id, auth)
        if not lakehouses:
            click.echo(f"⚠️ No lakehouses found in workspace {workspace_id}")
            return

        click.echo(f"\nLakehouses in workspace {workspace_id}:")
        for lakehouse_id, display_name in lakehouses:
            click.echo(f"  • {display_name} (ID: {lakehouse_id})")
        logger.debug(f"Listed lakehouses: {lakehouses}")
    except Exception as e:
        click.echo(f"❌ Error listing lakehouses: {e}")
        logger.error(f"Error listing lakehouses: {e}")


@display.command(name="warehouses")
@click.option("--workspace-id", required=True, help="Workspace ID to list warehouses from")
def list_warehouses(workspace_id):
    """Display all warehouses in a workspace !!not working with SPN!!"""
    logger.debug(f"Current state: {auth.get_state()}")
    try:
        warehouses = get_warehouses(workspace_id, auth)
        if not warehouses:
            click.echo(f"⚠️ No warehouses found in workspace {workspace_id}")
            return

        click.echo(f"\nWarehouses in workspace {workspace_id}:")
        for warehouse_id, display_name in warehouses:
            click.echo(f"  • {display_name} (ID: {warehouse_id})")
        logger.debug(f"Listed warehouses: {warehouses}")
    except Exception as e:
        click.echo(f"❌ Error listing warehouses: {e}")
        logger.error(f"Error listing warehouses: {e}")


@display.command(name="capacities")
def display_capacities():
    """Display all capacities."""
    try:
        capacities = get_capacities(auth)
        for capacity_id, display_name in capacities:
            click.echo(f"  • {display_name} (ID: {capacity_id})")
    except Exception as e:
        click.echo(f"❌ Error fetching capacities: {e}")
        logger.error(f"Error fetching capacities: {e}")


@main.group()
def capacity():
    """Manage Azure capacities"""
    pass


@capacity.command(name="suspend")
@click.option("--subscription-id", required=True, help="Azure subscription ID")
@click.option("--resource-group-name", required=True, help="Resource group name")
@click.option("--dedicated-capacity-name", required=True, help="Dedicated capacity name")
def suspend_capacity_cli(subscription_id, resource_group_name, dedicated_capacity_name):
    """Suspend a dedicated capacity in Azure"""
    try:
        response = suspend_capacity(subscription_id, resource_group_name, dedicated_capacity_name)
        click.echo(f"✅ Successfully suspended capacity '{dedicated_capacity_name}'")
        click.echo(response)
    except Exception as e:
        click.echo(f"❌ Error suspending capacity: {e}")
        logger.error(f"Error suspending capacity: {e}")


@capacity.command(name="resume")
@click.option("--subscription-id", required=True, help="Azure subscription ID")
@click.option("--resource-group-name", required=True, help="Resource group name")
@click.option("--dedicated-capacity-name", required=True, help="Dedicated capacity name")
def resume_capacity_cli(subscription_id, resource_group_name, dedicated_capacity_name):
    """Resume a dedicated capacity in Azure"""
    try:
        response = resume_capacity(subscription_id, resource_group_name, dedicated_capacity_name)
        click.echo(f"✅ Successfully resumed capacity '{dedicated_capacity_name}'")
        click.echo(response)
    except Exception as e:
        click.echo(f"❌ Error resuming capacity: {e}")
        logger.error(f"Error resuming capacity: {e}")


@main.group()
def git():
    """Manage Git repositories"""
    pass


@git.command(name="connect")
@click.option("--workspace-id", required=True, help="Workspace ID to connect to Git")
@click.option("--organization-name", required=True, help="Name of the organization")
@click.option("--project-name", required=True, help="Name of the project")
@click.option(
    "--git-provider-type",
    required=True,
    type=click.Choice(["AzureDevOps", "GitHub"]),
    help="Type of the Git provider",
)
@click.option("--repository-name", required=True, help="Name of the repository")
@click.option("--branch-name", required=True, help="Name of the branch")
@click.option("--directory-name", required=True, help="Name of the directory")
def connect_git(
    workspace_id,
    organization_name,
    project_name,
    git_provider_type,
    repository_name,
    branch_name,
    directory_name,
):
    """Connect a workspace to a Git repository"""
    git_provider_details = {
        "organizationName": organization_name,
        "projectName": project_name,
        "gitProviderType": git_provider_type,
        "repositoryName": repository_name,
        "branchName": branch_name,
        "directoryName": directory_name,
    }
    try:
        connect_git_repository(workspace_id, git_provider_details, auth)
        click.echo(f"✅ Successfully connected workspace '{workspace_id}' to Git repository")
    except Exception as e:
        click.echo(f"❌ Error connecting workspace to Git repository: {e}")
        logger.error(f"Error connecting workspace to Git repository: {e}")


if __name__ == "__main__":
    main()
