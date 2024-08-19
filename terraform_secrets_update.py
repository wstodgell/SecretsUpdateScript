import requests
import json

# Load config
with open('config.json') as config_file:
    config = json.load(config_file)

TERRAFORM_API_TOKEN = config["TERRAFORM_API_TOKEN"]
TERRAFORM_WORKSPACE_ID = config["TERRAFORM_WORKSPACE_ID"]

# Function to update a variable in Terraform Cloud
def update_terraform_variable(var_id, key, value, sensitive=False):
    print("********terraform_secrets_update.py imported")

    url = f"https://app.terraform.io/api/v2/vars/{var_id}"
    headers = {
        "Authorization": f"Bearer {TERRAFORM_API_TOKEN}",
        "Content-Type": "application/vnd.api+json"
    }
    payload = {
        "data": {
            "id": var_id,
            "type": "vars",
            "attributes": {
                "key": key,
                "value": value,
                "category": "env",
                "hcl": False,
                "sensitive": sensitive
            }
        }
    }
    response = requests.patch(url, headers=headers, json=payload)
    response.raise_for_status()
    print(f"Terraform variable {key} updated successfully.")
