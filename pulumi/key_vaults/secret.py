from typing import Optional
import pulumi_azure_native as azure_native
import pulumi
from key_vaults.key_vault import KeyVault


def create_secret(
    resource_group_name: str,
    secret_name: str,
    key: str,
    environment: str,
    keyvault: KeyVault,
    opts: Optional[pulumi.ResourceOptions] = None,
):
    combined_opts = pulumi.ResourceOptions.merge(
        opts,
        pulumi.ResourceOptions(
            ignore_changes=["properties.value", "properties.content_type"]
        ),
    )

    secret = azure_native.keyvault.Secret(
        f"secret-{secret_name}-{environment}",
        secret_name=secret_name,
        resource_group_name=resource_group_name,
        vault_name=keyvault.key_vault.name,
        properties=azure_native.keyvault.SecretPropertiesArgs(
            value=key,
            content_type="text/plain",
        ),
        opts=combined_opts,
    )

    return secret
