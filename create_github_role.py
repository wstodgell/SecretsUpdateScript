import boto3
import json
from file_tools import *

# Initialize a session using Boto3
session = boto3.Session(profile_name='sandbox1')
iam_client = session.client('iam')


config = load_config()
aws_account_id = config['AWS_ACCOUNT_ID']

answer = input(f"Using Account ID {aws_account_id} is this okay?")
if(answer == "y" or answer == "yes"):
    print("Continuing...")
else:
    print("Exiting...")
    exit()

# Define the OIDC provider URL and audience
oidc_provider_url = "https://token.actions.githubusercontent.com"
audience = "sts.amazonaws.com"

# Check if the OIDC provider already exists
existing_providers = iam_client.list_open_id_connect_providers()['OpenIDConnectProviderList']
oidc_provider_arn = f"arn:aws:iam::{aws_account_id}:oidc-provider/{oidc_provider_url.split('https://')[1]}"

if oidc_provider_arn not in [provider['Arn'] for provider in existing_providers]:
    # Create the OIDC provider
    oidc_provider_response = iam_client.create_open_id_connect_provider(
        Url=oidc_provider_url,
        ClientIDList=[audience],
        ThumbprintList=['A031C46782E6E6C662C2C87C76DA9AA62CCABD8E']  # GitHub's OIDC thumbprint
    )
    print(f"OIDC provider created: {oidc_provider_response['OpenIDConnectProviderArn']}")
else:
    print(f"OIDC provider already exists: {oidc_provider_arn}")

# Define the role name
role_name = "GitHubActionsAdminRole"

# Define the trust relationship policy document
assume_role_policy_document = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "Federated": oidc_provider_arn
            },
            "Action": "sts:AssumeRoleWithWebIdentity",
            "Condition": {
                "StringEquals": {
                    f"token.actions.githubusercontent.com:aud": audience,
                    f"token.actions.githubusercontent.com:sub": "repo:wstodgell/WildlifeHealthSurveilance:ref:refs/heads/master"
                }
            }
        }
    ]
}

# Create the IAM role
response = iam_client.create_role(
    RoleName=role_name,
    AssumeRolePolicyDocument=json.dumps(assume_role_policy_document),
    Description="Role for GitHub Actions with full administrative permissions"
)

print(f"Role {role_name} created successfully.")

# Attach the AdministratorAccess policy
iam_client.attach_role_policy(
    RoleName=role_name,
    PolicyArn="arn:aws:iam::aws:policy/AdministratorAccess"
)

print("AdministratorAccess policy attached successfully.")
