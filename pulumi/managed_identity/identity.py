from typing import Optional
import pulumi
import pulumi_azure_native as azure_native


class Identity(pulumi.ComponentResource):
    def __init__(
        self,
        name: str,
        identity_name: str,
        project_name: str,
        resource_group_name: str,
        location: str,
        opts: Optional[pulumi.ResourceOptions] = None,
    ):
        super().__init__(f"custom:{project_name}:managed_identity", name, {}, opts)

        self.identity = azure_native.managedidentity.UserAssignedIdentity(
            resource_name=name,
            resource_name_=identity_name,
            resource_group_name=resource_group_name,
            location=location,
            opts=opts,
        )
