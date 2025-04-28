from typing import Optional
import pulumi
import pulumi_azure_native as azure_native


class AnalyticsWorkspace(pulumi.ComponentResource):
    def __init__(
        self,
        name: str,
        project_name: str,
        workspace_name: str,
        resource_group_name: str,
        location: str,
        opts: Optional[pulumi.ResourceOptions] = None,
    ):
        super().__init__(f"custom:{project_name}:analytics-workspace", name, {}, opts)

        self.workspace = azure_native.operationalinsights.Workspace(
            name,
            location=location,
            resource_group_name=resource_group_name,
            retention_in_days=30,
            sku={
                "name": azure_native.operationalinsights.WorkspaceSkuNameEnum.PER_GB2018,
            },
            workspace_name=workspace_name,
            opts=opts,
        )

        shared_keys = pulumi.Output.all(self.workspace.name).apply(
            lambda name: azure_native.operationalinsights.get_shared_keys_output(
                resource_group_name=resource_group_name,
                workspace_name=name[0],
                opts=pulumi.InvokeOptions(provider=opts.provider) if opts else None,
            )
        )

        self.primary_shared_workspace_key = shared_keys.apply(
            lambda keys: keys.primary_shared_key
        )
