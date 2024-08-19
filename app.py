from flask import Flask, request, render_template, redirect, url_for, jsonify
import json
from github_secrets_update import update_secret
from terraform_secrets_update import update_terraform_variable

app = Flask(__name__)

# Load config
def load_config():
    with open('config.json') as config_file:
        return json.load(config_file)

def save_config(config):
    with open('config.json', 'w') as config_file:
        json.dump(config, config_file, indent=4)

@app.route('/', methods=['GET'])
def index():
    config = load_config()
    return render_template('index.html', config=config)

@app.route('/update', methods=['POST'])
def update_secrets():
    aws_access_key_id = request.form['aws_access_key_id']
    aws_secret_access_key = request.form['aws_secret_access_key']

    # Update GitHub secrets
    update_secret("AWS_ACCESS_KEY_ID", aws_access_key_id)
    update_secret("AWS_SECRET_ACCESS_KEY", aws_secret_access_key)

    # Update Terraform variables
    update_terraform_variable("var-abc123", "AWS_ACCESS_KEY_ID", aws_access_key_id, sensitive=True)
    update_terraform_variable("var-def456", "AWS_SECRET_ACCESS_KEY", aws_secret_access_key, sensitive=True)

    return redirect(url_for('index'))

@app.route('/save_config', methods=['POST'])
def save_config_route():
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

    save_config(config)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
