import requests

def update_terraform_variable(terraform_api_token, terraform_workspace_id, var_id, key, value, sensitive=False):
    url = f"https://app.terraform.io/api/v2/vars/{var_id}"
    headers = {
        "Authorization": f"Bearer {terraform_api_token}",
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
