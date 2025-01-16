# Fabric CLI

![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/Danny-de-bree/fabriccli/test.yml?branch=main)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)
[![code style: black](https://img.shields.io/badge/code_style-black-000000.svg)](https://github.com/psf/black)

To roll-out Fabric as a code we have developed a command line interface.

## Fabric API Client

https://learn.microsoft.com/en-us/rest/api/fabric/articles/

## Authentication

Not all API endpoints are SPN supported. If an endpoint is not supported by SPN, you can use a short-lived token that you can copy from the browser.

Beware! If you set POWER_BI_ACCESS_TOKEN it will overwrite all other authentication methods.

### Using SPN for Authentication

To use SPN (Service Principal Name) for authentication, follow these steps:

1. **🔑Login with SPN**:
    ```sh
    fabric login-spn --client-id YOUR_CLIENT_ID --client-secret YOUR_CLIENT_SECRET --tenant-id YOUR_TENANT_ID
    ```

### Using a service-account or Personal account

At this moment not all api calls are supported by SPN.
A workaround for this is the following:

1. Login with your azure account with az login.

    ```sh
    az login
    ```

    ```sh
    fabric login default
    ```


## 🚀 Features (MORE TO COME)

- Create new workspaces
- List existing workspaces
- Provision identities for workspaces (is done when creating new workspaces)
- Assign capacity to workspaces (is done when creating new workspaces)
- Create Lakehouses
- List Lakehouses
- Create Warehouses (gives an error, but works) (SPN doesn't work)
- List Warehouses (SPN doesn't work)
- Add Git repo (SPN doesn't work)
- Pause and Resume capacity
- Get capacities

## 📝 TODOs

- [ ] Add AAD group to workspace
- [ ] Add shortcut with OneLake from storage account

## 🛠 Prerequisites

- Python 3.10 or higher
- Microsoft Fabric Access Token or SPN

## 🔑 Obtaining and giving rights to SPN


## 📦 Installation

To install FabricCLI locally:

1. Clone the repository and navigate to the project directory: (works not yey will do later )

```bash
git clone https://github.com/Danny-de-bree/fabriccli.git
cd fabriccli
```

2. Install the package in editable mode:

```bash
pip install -e .
```

## 📖 Documentation

More to come

## 🤝 Contributing

More to come

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📧 Contact

Author: Danny de Bree
Email: [d.debree@rubicon.nl](mailto:d.debree@rubicon.nl)
