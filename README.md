# Fabric CLI by Rubicon

Fabric CLI is a powerful command-line tool for managing workspaces on the Microsoft Fabric platform. It provides options to create, list, and provision identities for workspaces, making your workflow more efficient and streamlined.

The current state of the Microsoft Fabric is documented on the following URL:

https://learn.microsoft.com/en-us/rest/api/fabric/articles/

Not all API endpoints are SPN supported. :(

If not use short lived token that you can copy from the browser.

## 🚀 Features (MORE TO COME)

- Create new workspaces
- List existing workspaces
- Provision identities for workspaces (is done when when creating new workspaces)
- Assign capacity to workspaces (is done when when creating new workspaces)
- Create Lakehouses
- List Lakehouses
- Create Warehoues (gives a error, but works) (SPN doesnt work)
- List Warehouses (SPN doesnt work)
- Add Git repo

## 📝 TODOs

- [ ] Add AAD group to workspace

- [ ] Add shortcut with OneLake from storage account.

- [ ] Pause and Resume capacity (80% working)

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
