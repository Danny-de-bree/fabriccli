# Fabric CLI by Rubicon

To roll-out Fabric as a code we have developed a command line interface.

## Fabric API Client

https://learn.microsoft.com/en-us/rest/api/fabric/articles/

## Authentication

Not all API endpoints are SPN supported. If an endpoint is not supported by SPN, you can use a short-lived token that you can copy from the browser.

Beware! If you set POWER_BI_ACCESS_TOKEN it will overwrite all other authentication methods.

### Using SPN for Authentication

To use SPN (Service Principal Name) for authentication, follow these steps:

1. **Login with SPN**:
    ```sh
    fabric login-spn --client-id YOUR_CLIENT_ID --client-secret YOUR_CLIENT_SECRET --tenant-id YOUR_TENANT_ID
    ```

2. **Verify Token**:
    Ensure that the token is correctly saved and used for subsequent API calls.

### Using Short-Lived Token

If SPN is not supported for a specific endpoint, you can use a short-lived token:

1. **Get Token from Browser**:
    - Open your browser and authenticate with your Azure AD credentials.
    - Copy the token from the browser's developer tools.

2. **Set Token Manually**:
    - Use the copied token for your API calls.

## 🚀 Features (MORE TO COME)

- Create new workspaces
- List existing workspaces
- Provision identities for workspaces (is done when creating new workspaces)
- Assign capacity to workspaces (is done when creating new workspaces)
- Create Lakehouses
- List Lakehouses
- Create Warehouses (gives an error, but works) (SPN doesn't work)
- List Warehouses (SPN doesn't work)
- Add Git repo
- Pause and Resume capacity

## 📝 TODOs

- [ ] Add AAD group to workspace
- [ ] Add shortcut with OneLake from storage account

## 🛠 Prerequisites

- Python 3.10 or higher
- Microsoft Fabric Access Token or SPN

## 🔑 Obtaining and giving rights to SPN

#TODO

## 🔑 Obtaining the Access Token

When not using a SPN, you can use a Power BI token.

### Steps to Obtain the Bearer Token:

1. Go to [Microsoft Power BI](https://app.powerbi.com/)
2. Log in with your Microsoft Fabric credentials.
3. Open the browser's developer tools by pressing `F12`.
4. In the developer tools, press `Ctrl + F` (or `Cmd + F` on Mac) to open the search bar.
5. Search for `powerBIAccessToken`.
6. Copy the token value, then set it as an environment variable named `POWER_BI_ACCESS_TOKEN` in your terminal or IDE.

```bash
export POWER_BI_ACCESS_TOKEN="your-token-here"
```

### Be sure to update this token periodically, as it expires after a short time!

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
