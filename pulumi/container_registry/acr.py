from typing import Optional
import pulumi
import pulumi_azure_native as azure_native


class ContainerRegistry(pulumi.ComponentResource):
    def __init__(
        self,
        name: str,
        registry_name: str,
        project_name: str,
        resource_group_name: str,
        location: str,
        opts: Optional[pulumi.ResourceOptions] = None,
    ):
        super().__init__(f"custom:{project_name}:acr", name, {}, opts)

        self.registry = azure_native.containerregistry.Registry(
            resource_name=name,
            args=azure_native.containerregistry.RegistryArgs(
                registry_name=registry_name,
                resource_group_name=resource_group_name,
                admin_user_enabled=True,
                sku=azure_native.containerregistry.SkuArgs(
                    name=azure_native.containerregistry.SkuName.BASIC,
                ),
                location=location,
            ),
            opts=opts,
        )

        credentials = azure_native.containerregistry.list_registry_credentials_output(
            resource_group_name=resource_group_name,
            registry_name=self.registry.name,
            opts=pulumi.InvokeOptions(provider=opts.provider) if opts else None,
        )

        self.registry_username = credentials.apply(lambda creds: creds.username)
        self.registry_password = credentials.apply(
            lambda creds: creds.passwords[0].value  # type: ignore
        )
