import json
import os

# Define default configuration values
DEFAULT_CONFIG = {
    "GITHUB_REPO": "your-username/your-repo",
    "GITHUB_TOKEN": "your-github-token3",
    "TERRAFORM_API_TOKEN": "your-terraform-api-token3",
    "TERRAFORM_WORKSPACE_ID": "your-workspace-id",
    "AWS_ACCESS_KEY_ID": "",
    "AWS_SECRET_ACCESS_KEY": "",
    "AWS_ACCOUNT_ID": ""
}

# Path to your configuration file
CONFIG_FILE_PATH = 'config.json'

def create_default_config(file_path):
    """Create a default config.json file if it does not exist."""
    if not os.path.exists(file_path):
        with open(file_path, 'w') as config_file:
            json.dump(DEFAULT_CONFIG, config_file, indent=4)
        print(f"Created default configuration file at {file_path}")

def load_config():
    create_default_config(CONFIG_FILE_PATH)  # Ensure the config file exists
    with open(CONFIG_FILE_PATH) as config_file:
        return json.load(config_file)

def save_config(config):
    print("saving Config")
    with open(CONFIG_FILE_PATH, 'w') as config_file:
        json.dump(config, config_file, indent=4)