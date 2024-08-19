import requests
from base64 import b64decode, b64encode
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
import json

# Load config
with open('config.json') as config_file:
    config = json.load(config_file)

GITHUB_REPO = config["GITHUB_REPO"]
GITHUB_TOKEN = config["GITHUB_TOKEN"]

# Function to get the public key for encrypting secrets
def get_public_key():
    url = f"https://api.github.com/repos/{GITHUB_REPO}/actions/secrets/public-key"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

# Function to create or update a secret
def update_secret(secret_name, secret_value):
    public_key = get_public_key()
    public_key_id = public_key["key_id"]
    public_key_data = public_key["key"]

    # Encrypt the secret using the public key
    public_key_bytes = b64decode(public_key_data)
    public_key = serialization.load_der_public_key(public_key_bytes)
    encrypted_value = public_key.encrypt(
        secret_value.encode("utf-8"),
        padding.PKCS1v15()
    )
    encrypted_value_b64 = b64encode(encrypted_value).decode("utf-8")

    # Update the secret using the GitHub API
    url = f"https://api.github.com/repos/{GITHUB_REPO}/actions/secrets/{secret_name}"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    data = {
        "encrypted_value": encrypted_value_b64,
        "key_id": public_key_id,
    }
    response = requests.put(url, headers=headers, json=data)
    response.raise_for_status()
    print(f"Secret {secret_name} updated successfully.")
