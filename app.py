from flask import Flask, request, render_template, redirect, url_for
import json
import os
from github_secrets_update import update_secret
from terraform_secrets_update import update_terraform_variable

app = Flask(__name__)

# Define default configuration values
DEFAULT_CONFIG = {
    "GITHUB_REPO": "your-username/your-repo",
    "GITHUB_TOKEN": "your-github-token3",
    "TERRAFORM_API_TOKEN": "your-terraform-api-token3",
    "TERRAFORM_WORKSPACE_ID": "your-workspace-id",
    "AWS_ACCESS_KEY_ID": "",
    "AWS_SECRET_ACCESS_KEY": ""
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

@app.route('/', methods=['GET'])
def index():
    config = load_config()
    return render_template('index.html', config=config)

@app.route('/update', methods=['POST'])
def update_secrets():
    aws_access_key_id = request.form['aws_access_key_id']
    aws_secret_access_key = request.form['aws_secret_access_key']

    # Get config values
    config = load_config()
    github_repo = config['GITHUB_REPO']
    github_token = config['GITHUB_TOKEN']
    terraform_api_token = config['TERRAFORM_API_TOKEN']
    terraform_workspace_id = config['TERRAFORM_WORKSPACE_ID']

    # Update GitHub secrets
    update_secret(github_repo, github_token, "AWS_ACCESS_KEY_ID", aws_access_key_id)
    update_secret(github_repo, github_token, "AWS_SECRET_ACCESS_KEY", aws_secret_access_key)

    # Update Terraform variables
    update_terraform_variable(terraform_api_token, terraform_workspace_id, "var-abc123", "AWS_ACCESS_KEY_ID", aws_access_key_id, sensitive=True)
    update_terraform_variable(terraform_api_token, terraform_workspace_id, "var-def456", "AWS_SECRET_ACCESS_KEY", aws_secret_access_key, sensitive=True)

    return redirect(url_for('index'))

@app.route('/save_config', methods=['POST'])
def save_config_route():
    print("!!saving Config")
    section = request.form['section']

    config = load_config()

    if section == 'aws':
        config['AWS_ACCESS_KEY_ID'] = request.form.get('aws_access_key_id', config['AWS_ACCESS_KEY_ID'])
        config['AWS_SECRET_ACCESS_KEY'] = request.form.get('aws_secret_access_key', config['AWS_SECRET_ACCESS_KEY'])
    elif section == 'github':
        config['GITHUB_REPO'] = request.form.get('github_repo', config['GITHUB_REPO'])
        config['GITHUB_TOKEN'] = request.form.get('github_token', config['GITHUB_TOKEN'])
    elif section == 'terraform':
        config['TERRAFORM_API_TOKEN'] = request.form.get('terraform_api_token', config['TERRAFORM_API_TOKEN'])
        config['TERRAFORM_WORKSPACE_ID'] = request.form.get('terraform_workspace_id', config['TERRAFORM_WORKSPACE_ID'])
    print("saving Config")
    save_config(config)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
