import pulumi
import pulumi_azure_native as azure_native
from typing import Optional


class ContainerAppEnvironment(pulumi.ComponentResource):
    def __init__(
        self,
        name: str,
        project_name: str,
        resource_group_name: pulumi.Input[str],
        location: pulumi.Input[str],
        log_analytics_workspace_customer_id: pulumi.Input[str],
        log_analytics_workspace_shared_key: pulumi.Input[str],
        opts: Optional[pulumi.ResourceOptions] = None,
    ) -> None:
        super().__init__(
            f"custom:{project_name}:container-app-environment", name, {}, opts
        )

        self.resource_group_name = resource_group_name
        self.location = location

        self.container_app_environment = azure_native.app.ManagedEnvironment(
            resource_name=name,
            environment_name=name,
            resource_group_name=resource_group_name,
            location=location,
            app_logs_configuration=azure_native.app.AppLogsConfigurationArgs(
                destination="log-analytics",
                log_analytics_configuration=azure_native.app.LogAnalyticsConfigurationArgs(
                    customer_id=log_analytics_workspace_customer_id,
                    shared_key=log_analytics_workspace_shared_key,
                ),
            ),
            opts=opts,
        )
