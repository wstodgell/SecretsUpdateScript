import os
import configparser
from flask import Flask, request, render_template, redirect, url_for
from file_tools import *
from github_secrets_update import update_secret
from terraform_secrets_update import create_or_update_terraform_variable

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    config = load_config()
    return render_template('index.html', config=config)

# make all necessary calls to respective platforms and update the secrets there
@app.route('/update', methods=['POST'])
def update_secrets():
    aws_access_key_id = request.form['aws_access_key_id']
    aws_secret_access_key = request.form['aws_secret_access_key']
    aws_account_id = request.form['aws_account_id']

    # Get config values
    config = load_config()
    github_repo = config['GITHUB_REPO']
    github_token = config['GITHUB_TOKEN']
    terraform_api_token = config['TERRAFORM_API_TOKEN']
    terraform_workspace_id = config['TERRAFORM_WORKSPACE_ID']

    # Update GitHub secrets
    update_secret(github_repo, github_token, "AWS_ACCESS_KEY_ID", aws_access_key_id)
    update_secret(github_repo, github_token, "AWS_SECRET_ACCESS_KEY", aws_secret_access_key)
    update_secret(github_repo, github_token, "AWS_ACCOUNT_ID", aws_account_id)

    # Update Terraform variables
    #create_or_update_terraform_variable(terraform_api_token, terraform_workspace_id, "AWS_ACCESS_KEY_ID", aws_access_key_id, sensitive=True)
    #create_or_update_terraform_variable(terraform_api_token, terraform_workspace_id, "AWS_SECRET_ACCESS_KEY", aws_secret_access_key, sensitive=True)


    return redirect(url_for('index'))

@app.route('/save_config', methods=['POST'])
def save_config_route():
    print("!!saving Config")
    section = request.form['section']

    config = load_config()

    if section == 'aws':
        aws_access_key_id = request.form.get('aws_access_key_id', config['AWS_ACCESS_KEY_ID'])
        aws_secret_access_key = request.form.get('aws_secret_access_key', config['AWS_SECRET_ACCESS_KEY'])
        aws_account_id = request.form.get('aws_account_id', config['AWS_ACCOUNT_ID'])
        profile = request.form.get('profile_select', 'default')  # Get the selected profile, default to 'default'
        print(f"Profile selected for saving: {profile}")

        config['AWS_ACCESS_KEY_ID'] = aws_access_key_id
        config['AWS_SECRET_ACCESS_KEY'] = aws_secret_access_key
        config['AWS_ACCOUNT_ID'] = aws_account_id

        # Update the credentials file with the selected profile
        update_aws_credentials(profile, aws_access_key_id, aws_secret_access_key)

    elif section == 'github':
        config['GITHUB_REPO'] = request.form.get('github_repo', config['GITHUB_REPO'])
        config['GITHUB_TOKEN'] = request.form.get('github_token', config['GITHUB_TOKEN'])
    elif section == 'terraform':
        config['TERRAFORM_API_TOKEN'] = request.form.get('terraform_api_token', config['TERRAFORM_API_TOKEN'])
        config['TERRAFORM_WORKSPACE_ID'] = request.form.get('terraform_workspace_id', config['TERRAFORM_WORKSPACE_ID'])
    print("saving Config")
    # save_config(config)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)



@app.route('/save_config', methods=['POST'])
def save_config_route():
    print("!!saving Config")
    section = request.form['section']

    config = load_config()

    if section == 'aws':
        aws_access_key_id = request.form.get('aws_access_key_id', config['AWS_ACCESS_KEY_ID'])
        aws_secret_access_key = request.form.get('aws_secret_access_key', config['AWS_SECRET_ACCESS_KEY'])
        aws_account_id = request.form.get('aws_account_id', config['AWS_ACCOUNT_ID'])
        profile = request.form.get('profile_select')  # Get the selected profile, no default here
        print(f"Profile selected for saving: {profile}")  # Debug the profile
        
        config['AWS_ACCESS_KEY_ID'] = aws_access_key_id
        config['AWS_SECRET_ACCESS_KEY'] = aws_secret_access_key
        config['AWS_ACCOUNT_ID'] = aws_account_id

        # Update the credentials file with the selected profile
        update_aws_credentials(profile, aws_access_key_id, aws_secret_access_key)

    elif section == 'github':
        config['GITHUB_REPO'] = request.form.get('github_repo', config['GITHUB_REPO'])
        config['GITHUB_TOKEN'] = request.form.get('github_token', config['GITHUB_TOKEN'])

    elif section == 'terraform':
        config['TERRAFORM_API_TOKEN'] = request.form.get('terraform_api_token', config['TERRAFORM_API_TOKEN'])
        config['TERRAFORM_WORKSPACE_ID'] = request.form.get('terraform_workspace_id', config['TERRAFORM_WORKSPACE_ID'])

    print("saving Config")
    save_config(config)
    return redirect(url_for('index'))
