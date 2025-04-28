import pulumi
import pulumi_azure_native as azure_native

from typing import Optional


class KeyVault(pulumi.ComponentResource):
    def __init__(
        self,
        name: str,
        project_name: str,
        resource_group_name: str,
        location: str,
        identity: azure_native.managedidentity.UserAssignedIdentity,
        opts: Optional[pulumi.ResourceOptions] = None,
    ):
        super().__init__(f"custom:{project_name}:key-vault", name, {}, opts)

        self.resource_group_name = resource_group_name

        self.key_vault = azure_native.keyvault.Vault(
            resource_name=name,
            vault_name=name,
            resource_group_name=resource_group_name,
            location=location,
            properties=azure_native.keyvault.VaultPropertiesArgs(
                tenant_id=identity.tenant_id,
                sku=azure_native.keyvault.SkuArgs(
                    family=azure_native.keyvault.SkuFamily.A,
                    name=azure_native.keyvault.SkuName.STANDARD,
                ),
                access_policies=[
                    azure_native.keyvault.AccessPolicyEntryArgs(
                        tenant_id=identity.tenant_id,
                        object_id=identity.principal_id,
                        permissions=azure_native.keyvault.PermissionsArgs(
                            keys=["all"],
                            secrets=["all"],
                        ),
                    )
                ],
            ),
            opts=opts,
        )

        self.key_vault_url = self.key_vault.properties.vault_uri
