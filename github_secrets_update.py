import requests
from base64 import b64decode, b64encode
from nacl import encoding, public

def get_public_key(github_repo, github_token):
    url = f"https://api.github.com/repos/{github_repo}/actions/secrets/public-key"
    headers = {"Authorization": f"token {github_token}"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

def encrypt_with_nacl(public_key_data, secret_value):
    public_key = public.PublicKey(public_key_data.encode("utf-8"), encoding.Base64Encoder())
    sealed_box = public.SealedBox(public_key)
    encrypted = sealed_box.encrypt(secret_value.encode("utf-8"))
    return b64encode(encrypted).decode("utf-8")

def update_secret(github_repo, github_token, secret_name, secret_value):
    public_key_response = get_public_key(github_repo, github_token)
    public_key_id = public_key_response["key_id"]
    public_key_data = public_key_response["key"]

    print("Public Key Data:", public_key_data)  # Debugging: Print public key data

    try:
        # Encrypt the secret using the NaCl public key
        encrypted_value_b64 = encrypt_with_nacl(public_key_data, secret_value)

        # Update the secret using the GitHub API
        url = f"https://api.github.com/repos/{github_repo}/actions/secrets/{secret_name}"
        headers = {
            "Authorization": f"token {github_token}",
            "Accept": "application/vnd.github.v3+json",
            "Content-Type": "application/json"
        }
        data = {
            "encrypted_value": encrypted_value_b64,
            "key_id": public_key_id,
        }
        response = requests.put(url, headers=headers, json=data)
        response.raise_for_status()
        print(f"Secret {secret_name} updated successfully.")
    except (ValueError, TypeError) as e:
        print(f"Error processing public key or encryption: {e}")
    except requests.exceptions.RequestException as e:
        print(f"HTTP error occurred: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

