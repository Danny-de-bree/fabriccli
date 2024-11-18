# FabricCLI

FabricCLI is a powerful command-line tool for managing workspaces on the Microsoft Fabric platform. It provides options to create, list, and provision identities for workspaces, making your workflow more efficient and streamlined.

## 🚀 Features (MORE TO COME)

- Create new workspaces
- List existing workspaces
- Provision identities for workspaces (is done when when creating new workspaces)

## 📝 TODOs

- [ ] Pass capacity_id from api to the create_workspace function.
        - What do we do if there are multiple capacity_ids?

- [ ] Add AAD group to workspace
        - Very hard need to investigate more.

- [ ] Add authentication with SPN
    - Investigate how to authenticate with SPN.

- [ ] Add shortcut with OneLake from storage account.

- [ ] Clean some print statements and add logging.

- [ ] Add tests for the functions.

## 🛠 Prerequisites

- Python 3.6 or higher
- Microsoft Fabric Access Token

## 🔑 Obtaining the Access Token

To use FabricCLI with Microsoft Fabric, you need a valid bearer token. Tokens are short-lived and need to be periodically updated.

### Steps to Obtain the Bearer Token:

1. Go to [Microsoft Power BI](https://app.powerbi.com/)
2. Log in with your Microsoft Fabric credentials.
3. Open the browser's developer tools by pressing `F12`.
4. In the developer tools, press `Ctrl + F` (or `Cmd + F` on Mac) to open the search bar.
5. Search for `powerBIAccessToken` among the network requests.
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

## 📝 Usage

### Creating Workspaces

```bash
fabric --create "Workspace Name" --capacity_id "Capacity ID"
```

### Listing Workspaces

```bash
fabric --get
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
