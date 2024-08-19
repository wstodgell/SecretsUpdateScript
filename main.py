import json
import os
from github_secrets_update import update_secret as update_github_secret
from terraform_secrets_update import update_terraform_variable

# Load configuration file
with open('config.json') as config_file:
    config = json.load(config_file)

# Extract the necessary values
GITHUB_REPO = config['GITHUB_REPO']
GITHUB_TOKEN = config['GITHUB_TOKEN']
TERRAFORM_API_TOKEN = config['TERRAFORM_API_TOKEN']
TERRAFORM_WORKSPACE_ID = config['TERRAFORM_WORKSPACE_ID']

def main():
    # Example usage
    github_secret_name = "AWS_ACCESS_KEY_ID"
    github_secret_value = "new-aws-access-key-id"
    update_github_secret(github_secret_name, github_secret_value)
    
    terraform_var_id = "var-abc123"
    terraform_key = "AWS_ACCESS_KEY_ID"
    terraform_value = "new-aws-access-key-id"
    update_terraform_variable(terraform_var_id, terraform_key, terraform_value, sensitive=True)

if __name__ == "__main__":
    main()
