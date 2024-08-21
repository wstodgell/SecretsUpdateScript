# Secrets Update Script

## Overview

The Secrets Update Script is a web-based tool built with Flask that facilitates the updating of sensitive secrets for GitHub and Terraform. This application allows you to manage and update AWS credentials, GitHub secrets, and Terraform variables through a user-friendly web interface.

## Features

- **AWS Secrets Management**: Update AWS Access Key ID and Secret Access Key.
- **GitHub Secrets Update**: Securely update GitHub repository secrets using GitHub's API.
- **Terraform Variables Management**: Update Terraform environment variables with sensitive data.
- **Configuration Management**: Save and load configuration settings for GitHub and Terraform.

## Directory Structure

- **`app.py`**: Main Flask application file.
- **`config.json`**: Configuration file storing credentials and tokens.
- **`file_tools.py`**: Utility functions for loading and saving the configuration file.
- **`github_secrets_update.py`**: Script for updating GitHub repository secrets.
- **`terraform_secrets_update.py`**: Script for updating Terraform variables.
- **`static/`**: Directory containing static files like CSS, JavaScript, and images.
- **`templates/`**: Directory containing HTML templates.

## How It Works

1. **Configuration**: Ensure `config.json` is properly set with your GitHub and Terraform credentials.
2. **Run the Application**: Execute `app.py` to start the Flask web server.
3. **Update Secrets**:
   - Navigate to the web interface and input the new AWS credentials.
   - Click the "Update Secrets" button to apply changes.
4. **Manage Configurations**:
   - Use the provided forms to save configurations for GitHub and Terraform.
   - Changes are saved and reflected in `config.json`.

## Dependencies

- Flask
- Requests
- PyNaCl (for GitHub secret encryption)

Install dependencies via:

```bash
pip install -r requirements.txt
