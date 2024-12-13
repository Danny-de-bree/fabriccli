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


def handle_login_success(message: str):
    """Handle login success"""
    click.echo(f"✅ {message}")
    logger.debug(message)


def handle_login_error(e: Exception):
    """Handle login errors"""
    click.echo(f"❌ Error logging in: {e}")
    logger.error(f"Error logging in: {e}")


def execute_command(command_func, *args, **kwargs):
    """Helper function to execute a command with common error handling"""
    try:
        command_func(*args, **kwargs)
    except Exception as e:
        click.echo(f"❌ Error executing command: {e}")
        logger.error(f"Error executing command: {e}")


@click.group()
def main():
    """🟠☁️   Welcome to the Fabric CLI Tool! 🟠☁️

    Manage your Microsoft Fabric resources with ease!

    Made by Danny de Bree with the help of Rubicon

    www.Rubicon.nl
    """  # I know strange outlining, but otherwise Click will not show the text
    pass


@main.group(name="login")
def login_group():
    """Login to Microsoft Fabric"""
    pass


@login_group.command(hidden=True)
@click.option("--token", "-t", required=True, help="Power BI access token")
def token(token):
    """Login to Microsoft Fabric using a token"""
    execute_command(auth.set_token, token, "fabric")
    handle_login_success("Successfully logged in with token")


@login_group.command()
@click.option("--client-id", required=True, help="Azure AD Client ID")
@click.option("--client-secret", required=True, help="Azure AD Client Secret")
@click.option("--tenant-id", required=True, help="Azure AD Tenant ID")
def spn(client_id, client_secret, tenant_id):
    """Login to Microsoft Fabric using SPN"""
    config = SPNConfig(client_id=client_id, client_secret=client_secret, tenant_id=tenant_id)
    execute_command(auth.set_spn_config, config)
    handle_login_success("Successfully logged in with SPN")


@login_group.command()
def default():
    """Login to Microsoft Fabric using DefaultAzureCredential"""
    execute_command(
        auth.authenticate_with_default_credential, scope="https://api.fabric.microsoft.com/.default"
    )
    handle_login_success("Successfully logged in with DefaultAzureCredential")


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

    def command_logic():
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

    execute_command(command_logic)


@create.command()
@click.argument("name")
@click.option("--workspace-id", required=True, help="Workspace ID where to create the lakehouse")
def lakehouse(name, workspace_id):
    """Create a new lakehouse in a workspace"""

    def command_logic():
        lakehouse_id = create_lakehouse(workspace_id, name, auth)
        click.echo(f"✅ Created lakehouse '{name}' with ID: {lakehouse_id}")
        logger.debug(f"Lakehouse created with ID: {lakehouse_id}")
        return lakehouse_id

    execute_command(command_logic)


@create.command()
@click.argument("name")
@click.option("--workspace-id", required=True, help="Workspace ID where to create the warehouse")
def warehouse(name, workspace_id):
    """Create a new warehouse in a workspace"""

    def command_logic():
        warehouse_id = create_warehouse(workspace_id, name, auth)
        click.echo(f"✅ Created warehouse '{name}' with ID: {warehouse_id}")
        logger.debug(f"Warehouse created with ID: {warehouse_id}")
        return warehouse_id

    execute_command(command_logic)


@main.group()
def display():
    """Display Microsoft Fabric resources"""
    pass


@display.command(name="workspaces")
def list_workspaces():
    """Display all workspaces"""

    def command_logic():
        spaces = get_workspaces(auth)
        if not spaces:
            click.echo("⚠️ No workspaces found")
            return

        for workspace_id, display_name, capacity_id in spaces:
            capacity_info = f" (Capacity ID: {capacity_id})" if capacity_id else ""
            click.echo(f"  • {display_name} (ID: {workspace_id}){capacity_info}")
        logger.debug(f"Listed workspaces: {spaces}")

    execute_command(command_logic)


@display.command(name="lakehouses")
@click.option("--workspace-id", required=True, help="Workspace ID to list lakehouses from")
def list_lakehouses(workspace_id):
    """Display all lakehouses in a workspace"""

    def command_logic():
        lakehouses = get_lakehouses(workspace_id, auth)
        if not lakehouses:
            click.echo(f"⚠️ No lakehouses found in workspace {workspace_id}")
            return

        click.echo(f"\nLakehouses in workspace {workspace_id}:")
        for lakehouse_id, display_name in lakehouses:
            click.echo(f"  • {display_name} (ID: {lakehouse_id})")
        logger.debug(f"Listed lakehouses: {lakehouses}")

    execute_command(command_logic)


@display.command(name="warehouses")
@click.option("--workspace-id", required=True, help="Workspace ID to list warehouses from")
def list_warehouses(workspace_id):
    """Display all warehouses in a workspace !!not working with SPN!!"""
    logger.debug(f"Current state: {auth.get_state()}")

    def command_logic():
        warehouses = get_warehouses(workspace_id, auth)
        if not warehouses:
            click.echo(f"⚠️ No warehouses found in workspace {workspace_id}")
            return

        click.echo(f"\nWarehouses in workspace {workspace_id}:")
        for warehouse_id, display_name in warehouses:
            click.echo(f"  • {display_name} (ID: {warehouse_id})")
        logger.debug(f"Listed warehouses: {warehouses}")

    execute_command(command_logic)


@display.command(name="capacities")
def display_capacities():
    """Display all capacities."""

    def command_logic():
        capacities = get_capacities(auth)
        for capacity_id, display_name in capacities:
            click.echo(f"  • {display_name} (ID: {capacity_id})")

    execute_command(command_logic)


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

    def command_logic():
        response = suspend_capacity(subscription_id, resource_group_name, dedicated_capacity_name)
        click.echo(f"✅ Successfully suspended capacity '{dedicated_capacity_name}'")
        click.echo(response)

    execute_command(command_logic)


@capacity.command(name="resume")
@click.option("--subscription-id", required=True, help="Azure subscription ID")
@click.option("--resource-group-name", required=True, help="Resource group name")
@click.option("--dedicated-capacity-name", required=True, help="Dedicated capacity name")
def resume_capacity_cli(subscription_id, resource_group_name, dedicated_capacity_name):
    """Resume a dedicated capacity in Azure"""

    def command_logic():
        response = resume_capacity(subscription_id, resource_group_name, dedicated_capacity_name)
        click.echo(f"✅ Successfully resumed capacity '{dedicated_capacity_name}'")
        click.echo(response)

    execute_command(command_logic)


@main.group(hidden=True)
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

    def command_logic():
        git_provider_details = {
            "organizationName": organization_name,
            "projectName": project_name,
            "gitProviderType": git_provider_type,
            "repositoryName": repository_name,
            "branchName": branch_name,
            "directoryName": directory_name,
        }
        connect_git_repository(workspace_id, git_provider_details, auth)
        click.echo(f"✅ Successfully connected workspace '{workspace_id}' to Git repository")

    execute_command(command_logic)


if __name__ == "__main__":
    main()
