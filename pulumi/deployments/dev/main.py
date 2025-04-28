import pulumi
from analytics_workspace.workspace import AnalyticsWorkspace
from application.application_registration import ApplicationRegistration
from container_apps.container_app import ContainerApp
from container_apps.environment import ContainerAppEnvironment
from container_registry.acr import ContainerRegistry
from key_vaults.key_vault import KeyVault
from key_vaults.secret import create_secret
from managed_identity.identity import Identity
import pulumi_azure_native as azure_native


class DevDeployment:
    def __init__(
        self,
        project_name: str,
        rg_name: str,
        location: str,
        opts: pulumi.ResourceOptions,
    ) -> None:
        self.project_name = project_name
        self.rg_name = rg_name
        self.location = location
        self.opts = opts

        self.environment = "dev"

    def build(self) -> None:
        config = pulumi.Config()

        openai_key = config.require("AZURE-API-KEY")
        openai_url = config.require("AZURE-API-URL")
        app_secret_key = config.require("APP-SECRET-KEY")
        wa_password_hash = config.require("WA-PASSWORD-HASH")
        wa_username = config.require("WA-USERNAME")
        admin_password_hash = config.require("ADMIN-PASSWORD-HASH")
        daily_cost_threshold = config.require("DAILY-COST-THRESHOLD")

        ApplicationRegistration(
            name=f"{self.project_name}-{self.environment}",
            project_name=self.project_name,
            opts=self.opts,
        )

        managed_identity = Identity(
            name=f"{self.environment}-identity",
            identity_name=f"{self.project_name}-identity",
            project_name=self.project_name,
            resource_group_name=self.rg_name,
            location=self.location,
            opts=self.opts,
        )

        analytics_workspace = AnalyticsWorkspace(
            name=f"{self.environment}-analytics-workspace",
            project_name=self.project_name,
            workspace_name=f"{self.project_name}-analytics",
            resource_group_name=self.rg_name,
            location=self.location,
            opts=self.opts,
        )

        registry_name = "".join(
            word.capitalize() for word in self.project_name.split("-")
        )

        container_registry = ContainerRegistry(
            name=f"{self.environment}-container-registry",
            project_name=self.project_name,
            registry_name=f"{registry_name}ContainerRegistry{self.environment.capitalize()}",
            resource_group_name=self.rg_name,
            location=self.location,
            opts=self.opts,
        )

        container_app_environment = ContainerAppEnvironment(
            name=f"{self.project_name}-container-app-environment-{self.environment}",
            project_name=self.project_name,
            location=self.location,
            resource_group_name=self.rg_name,
            log_analytics_workspace_customer_id=analytics_workspace.workspace.customer_id,
            log_analytics_workspace_shared_key=analytics_workspace.primary_shared_workspace_key,  # type: ignore
            opts=self.opts,
        )

        # Create Key Vault and secrets

        keyvault = KeyVault(
            name=f"{self.project_name}-kv-{self.environment}",
            project_name=self.project_name,
            resource_group_name=self.rg_name,
            location=self.location,
            identity=managed_identity.identity,
            opts=self.opts,
        )

        openai_key_secret_name = "openai-key"
        openai_key_secret = create_secret(
            resource_group_name=self.rg_name,
            secret_name=openai_key_secret_name,
            key=openai_key,
            environment=self.environment,
            keyvault=keyvault,
            opts=self.opts,
        )

        app_secret_key_name = "app-secret-key"
        app_secret_key_secret = create_secret(
            resource_group_name=self.rg_name,
            secret_name=app_secret_key_name,
            key=app_secret_key,
            environment=self.environment,
            keyvault=keyvault,
            opts=self.opts,
        )

        wa_password_hash_name = "wa-password-hash"
        wa_password_hash_secret = create_secret(
            resource_group_name=self.rg_name,
            secret_name=wa_password_hash_name,
            key=wa_password_hash,
            environment=self.environment,
            keyvault=keyvault,
            opts=self.opts,
        )

        admin_password_hash_name = "admin-password-hash"
        admin_password_hash_secret = create_secret(
            resource_group_name=self.rg_name,
            secret_name=admin_password_hash_name,
            key=admin_password_hash,
            environment=self.environment,
            keyvault=keyvault,
            opts=self.opts,
        )

        secrets = [
            azure_native.app.v20230501.SecretArgs(
                name=openai_key_secret_name,
                key_vault_url=openai_key_secret.properties.secret_uri,
                identity=managed_identity.identity.id,
            ),
            azure_native.app.v20230501.SecretArgs(
                name=app_secret_key_name,
                key_vault_url=app_secret_key_secret.properties.secret_uri,
                identity=managed_identity.identity.id,
            ),
            azure_native.app.v20230501.SecretArgs(
                name=wa_password_hash_name,
                key_vault_url=wa_password_hash_secret.properties.secret_uri,
                identity=managed_identity.identity.id,
            ),
            azure_native.app.v20230501.SecretArgs(
                name=admin_password_hash_name,
                key_vault_url=admin_password_hash_secret.properties.secret_uri,
                identity=managed_identity.identity.id,
            ),
        ]

        environment_variables = [
            azure_native.app.v20230501.EnvironmentVarArgs(
                name="AZURE-API-KEY", secret_ref=openai_key_secret_name
            ),
            azure_native.app.v20230501.EnvironmentVarArgs(
                name="APP-SECRET-KEY", secret_ref=app_secret_key_name
            ),
            azure_native.app.v20230501.EnvironmentVarArgs(
                name="WA-PASSWORD-HASH", secret_ref=wa_password_hash_name
            ),
            azure_native.app.v20230501.EnvironmentVarArgs(
                name="ADMIN-PASSWORD-HASH", secret_ref=admin_password_hash_name
            ),
            azure_native.app.v20230501.EnvironmentVarArgs(
                name="AZURE-API-URL", value=openai_url
            ),
            azure_native.app.v20230501.EnvironmentVarArgs(
                name="WA-USERNAME", value=wa_username
            ),
            azure_native.app.v20230501.EnvironmentVarArgs(
                name="DAILY-COST-THRESHOLD", value=daily_cost_threshold
            ),
        ]

        ContainerApp(
            name=f"{self.project_name}-{self.environment}",
            project_name=self.project_name,
            resource_group_name=self.rg_name,
            location=self.location,
            environment_id=container_app_environment.container_app_environment.id,
            external=True,
            target_port=80,
            acr_login_server=container_registry.registry.login_server,
            acr_name=container_registry.registry.name,
            acr_username=container_registry.registry_username,  # type: ignore
            acr_password=container_registry.registry_password,  # type: ignore
            repository=f"{self.environment}/wa-brainstormer",
            container_name="wa-brainstormer",
            identity=managed_identity.identity,
            environment_variables=environment_variables,
            secrets=secrets,
            opts=self.opts,
        )
