import json
import os
import configparser

# Define default configuration values
DEFAULT_CONFIG = {
    "GITHUB_REPO": "your-username/your-repo",
    "GITHUB_TOKEN": "your-github-token3",
    "TERRAFORM_API_TOKEN": "your-terraform-api-token3",
    "TERRAFORM_WORKSPACE_ID": "your-workspace-id",
    "AWS_ACCESS_KEY_ID": "",
    "AWS_SECRET_ACCESS_KEY": "",
    "AWS_ACCOUNT_ID": "",
    "CREDENTIAL_FILE": ""
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
    # It opens the file located at CONFIG_FILE_PATH (presumably a path to the configuration file) in write mode ('w').
    with open(CONFIG_FILE_PATH, 'w') as config_file:
        print("Saving the following config:")
        print(json.dumps(config, indent=4))  # Prints the config in a pretty JSON format
        # converts the config object (a Python dictionary)
        json.dump(config, config_file, indent=4)


def update_aws_credentials(profile, aws_access_key_id, aws_secret_access_key):
    print(f"Updating AWS credentials for profile: {profile}")
    config_file_path = load_config().get('CREDENTIAL_FILE')
    
    # Create a ConfigParser object to work with the INI-like AWS credentials file
    config = configparser.ConfigParser()

    # Read the AWS credentials file
    config.read(config_file_path)

    # Check if the profile exists in the credentials file
    if profile in config:
        print(f"Profile {profile} found in credentials file.")
        # Update the access key and secret access key for the selected profile
        config[profile]['aws_access_key_id'] = aws_access_key_id
        config[profile]['aws_secret_access_key'] = aws_secret_access_key
    else:
        print(f"Profile {profile} not found. Creating a new section.")
        # If the profile doesn't exist, create a new section
        config[profile] = {
            'aws_access_key_id': aws_access_key_id,
            'aws_secret_access_key': aws_secret_access_key
        }

    # Write the updated credentials back to the file
    with open(config_file_path, 'w') as configfile:
        config.write(configfile)

    print(f"AWS credentials for profile {profile} updated successfully.")