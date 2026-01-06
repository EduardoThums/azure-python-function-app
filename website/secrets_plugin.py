import os
import json
# from cwilog import exception as print


def _identify_provider():
    is_aws = os.getenv("LAMBDA_TASK_ROOT") is not None

    if is_aws:
        return "aws"

    # is_azure = (
    #     os.getenv("AZURE_CLIENT_ID") is not None
    #     or os.getenv("WEBSITE_INSTANCE_ID") is not None
    # )
    is_azure = os.getenv("WEBSITE_INSTANCE_ID") is not None

    if is_azure:
        return "azure"

    raise ValueError("Unable to identify the cloud provider to fetch the credentials")


def _fetch_aws_secrets(app, secret_name):
    try:
        import boto3

        client = boto3.client("secretsmanager")
        response = client.get_secret_value(SecretId=secret_name)
        if "SecretString" in response and response["SecretString"]:
            for key, value in json.loads(response["SecretString"]).items():
                app.config[key] = value
    except ImportError:
        print("boto3 not available for AWS secrets")
    except Exception as e:
        print(f"Error fetching AWS secrets: {e}")


def _fetch_azure_secrets(app):
    try:
        from azure.identity import DefaultAzureCredential
        from azure.keyvault.secrets import SecretClient

        key_vault_name = app.config.get("SECRET_NAME")
        if not key_vault_name:
            print("SECRET_NAME not configured for Azure secrets")
            return
        vault_url = f"https://{key_vault_name}.vault.azure.net"
        credential = DefaultAzureCredential()
        client = SecretClient(vault_url=vault_url, credential=credential)
        secrets = client.list_properties_of_secrets()
        for secret_prop in secrets:
            if secret_prop.name:
                secret = client.get_secret(secret_prop.name)
                if secret.name and secret.value is not None:
                    app.config[secret.name] = secret.value
    except ImportError:
        print("Azure libraries not available")
    except Exception as e:
        print(f"Error fetching Azure secrets: {e}")


def init_secret_manager(app):
    secret_name = app.config.get("SECRET_NAME")
    if secret_name is None:
        return

    provider = app.config.get("SECRET_PROVIDER")

    if provider is None:
        provider = _identify_provider()

    if provider == "aws":
        _fetch_aws_secrets(app, secret_name)

    elif provider == "azure":
        _fetch_azure_secrets(app)
