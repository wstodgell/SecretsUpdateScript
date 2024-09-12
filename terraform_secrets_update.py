import requests

def create_or_update_terraform_variable(terraform_api_token, terraform_workspace_id, key, value, sensitive=False):
    try:
        url = f"https://app.terraform.io/api/v2/workspaces/{terraform_workspace_id}/vars"
        headers = {
            "Authorization": f"Bearer {terraform_api_token}",
            "Content-Type": "application/vnd.api+json"
        }
        payload = {
            "data": {
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
        response = requests.post(url, headers=headers, json=payload)
        
        # If the variable already exists, the API might return an error. 
        # Therefore, check if the variable already exists and update it if needed.
        if response.status_code == 422:  # 422 Unprocessable Entity means the variable already exists.
            # Find the existing variable and update it.
            existing_var_id = get_variable_id(terraform_api_token, terraform_workspace_id, key)
            if existing_var_id:
                update_url = f"https://app.terraform.io/api/v2/vars/{existing_var_id}"
                response = requests.patch(update_url, headers=headers, json=payload)
        
        response.raise_for_status()  # Raise an error for bad responses
        print(f"Terraform variable {key} updated successfully.")
    except requests.exceptions.HTTPError as err:
        print(f"Failed to update Terraform variable {key}: {err}")
    except Exception as e:
        print(f"An error occurred: {e}")

def get_variable_id(terraform_api_token, terraform_workspace_id, key):
    try:
        url = f"https://app.terraform.io/api/v2/workspaces/{terraform_workspace_id}/vars"
        headers = {
            "Authorization": f"Bearer {terraform_api_token}",
            "Content-Type": "application/vnd.api+json"
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        variables = response.json()["data"]
        for var in variables:
            if var["attributes"]["key"] == key:
                return var["id"]
        return None
    except requests.exceptions.HTTPError as err:
        print(f"Failed to retrieve variable ID for {key}: {err}")
        return None
