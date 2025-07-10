import pulumi_azure_native as azure_native
from analytics_workspace.alerts import (
    create_action_group,
    create_cpu_usage_alert,
    create_requests_alert,
)
from analytics_workspace.workspace import AnalyticsWorkspace
from application.application_registration import ApplicationRegistration
from container_apps.container_app import ContainerApp
from container_apps.environment import ContainerAppEnvironment
from container_registry.acr import ContainerRegistry
from key_vaults.key_vault import KeyVault
from key_vaults.secret import create_secret
from managed_identity.identity import Identity

import pulumi

HOSTNAME = "brainstormer.cwa.viadee.cloud"


class ProdDeployment:
    def __init__(
        self,
        project_name: str,
        rg_name: str,
        subscription_id: str,
        location: str,
        opts: pulumi.ResourceOptions,
    ) -> None:
        self.project_name = project_name
        self.rg_name = rg_name
        self.subscription_id = subscription_id
        self.location = location
        self.opts = opts

        self.environment = "prod"

    def build(self) -> None:
        config = pulumi.Config()

        openai_key = config.require_secret("AZURE-API-KEY")
        openai_url = config.require("AZURE-API-URL")
        openai_version = config.get("AZURE-API-VERSION")
        app_secret_key = config.require_secret("APP-SECRET-KEY")
        wa_password_hash = config.require_secret("WA-PASSWORD-HASH")
        wa_username = config.require("WA-USERNAME")
        admin_password_hash = config.require_secret("ADMIN-PASSWORD-HASH")
        daily_cost_threshold = config.require("DAILY-COST-THRESHOLD")
        chat_model = config.require("AZURE_OPENAI_CHAT_MODEL")
        embedding_model = config.require("AZURE_OPENAI_EMBEDDING_MODEL")
        login_required = config.require("AUTH_LOGIN_REQUIRED")
        qdrant_url = config.require("QDRANT-URL")
        qdrant_workarounds_read_key = config.require_secret(
            "QDRANT-WORKAROUNDS-READ-KEY"
        )
        qdrant_full_access_key = config.require_secret("QDRANT-FULL-ACCESS-KEY")

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

        qdrant_workarounds_read_key_name = "qdrant-workarounds-read-key"
        qdrant_workarounds_read_key_secret = create_secret(
            resource_group_name=self.rg_name,
            secret_name=qdrant_workarounds_read_key_name,
            key=qdrant_workarounds_read_key,
            environment=self.environment,
            keyvault=keyvault,
            opts=self.opts,
        )

        qdrant_full_access_key_name = "qdrant-full-access-key"
        qdrant_full_access_key_secret = create_secret(
            resource_group_name=self.rg_name,
            secret_name=qdrant_full_access_key_name,
            key=qdrant_full_access_key,
            environment=self.environment,
            keyvault=keyvault,
            opts=self.opts,
        )

        secrets = [
            azure_native.app.SecretArgs(
                name=openai_key_secret_name,
                key_vault_url=openai_key_secret.properties.secret_uri,
                identity=managed_identity.identity.id,
            ),
            azure_native.app.SecretArgs(
                name=app_secret_key_name,
                key_vault_url=app_secret_key_secret.properties.secret_uri,
                identity=managed_identity.identity.id,
            ),
            azure_native.app.SecretArgs(
                name=wa_password_hash_name,
                key_vault_url=wa_password_hash_secret.properties.secret_uri,
                identity=managed_identity.identity.id,
            ),
            azure_native.app.SecretArgs(
                name=admin_password_hash_name,
                key_vault_url=admin_password_hash_secret.properties.secret_uri,
                identity=managed_identity.identity.id,
            ),
            azure_native.app.SecretArgs(
                name=qdrant_workarounds_read_key_name,
                key_vault_url=qdrant_workarounds_read_key_secret.properties.secret_uri,
                identity=managed_identity.identity.id,
            ),
            azure_native.app.SecretArgs(
                name=qdrant_full_access_key_name,
                key_vault_url=qdrant_full_access_key_secret.properties.secret_uri,
                identity=managed_identity.identity.id,
            ),
        ]

        environment_variables = [
            azure_native.app.EnvironmentVarArgs(
                name="AZURE_OPENAI_API_KEY", secret_ref=openai_key_secret_name
            ),
            azure_native.app.EnvironmentVarArgs(
                name="APPSECRETKEY", secret_ref=app_secret_key_name
            ),
            azure_native.app.EnvironmentVarArgs(
                name="WAPASSWORDHASH", secret_ref=wa_password_hash_name
            ),
            azure_native.app.EnvironmentVarArgs(
                name="ADMINPASSWORDHASH", secret_ref=admin_password_hash_name
            ),
            azure_native.app.EnvironmentVarArgs(
                name="QDRANT_WORKAROUNDS_READ_KEY",
                secret_ref=qdrant_workarounds_read_key_name,
            ),
            azure_native.app.EnvironmentVarArgs(
                name="QDRANT_FULL_ACCESS_KEY",
                secret_ref=qdrant_full_access_key_name,
            ),
            azure_native.app.EnvironmentVarArgs(
                name="AZURE_OPENAI_API_URL", value=openai_url
            ),
            azure_native.app.EnvironmentVarArgs(name="WAUSERNAME", value=wa_username),
            azure_native.app.EnvironmentVarArgs(
                name="DAILYCOSTTHRESHOLD", value=daily_cost_threshold
            ),
            azure_native.app.EnvironmentVarArgs(name="QDRANT_URL", value=qdrant_url),
            azure_native.app.EnvironmentVarArgs(
                name="AZURE_OPENAI_API_VERSION",
                value=openai_version if openai_version else "v1",
            ),
            azure_native.app.EnvironmentVarArgs(
                name="AZURE_OPENAI_CHAT_MODEL",
                value=chat_model,
            ),
            azure_native.app.EnvironmentVarArgs(
                name="AZURE_OPENAI_EMBEDDING_MODEL",
                value=embedding_model,
            ),
            azure_native.app.EnvironmentVarArgs(
                name="AUTH_LOGIN_REQUIRED",
                value=login_required,
            ),
        ]

        container_app = ContainerApp(
            name=f"{self.project_name}-{self.environment}",
            project_name=self.project_name,
            resource_group_name=self.rg_name,
            location=self.location,
            environment_id=container_app_environment.container_app_environment.id,
            external=True,
            target_port=5000,
            acr_login_server=container_registry.registry.login_server,
            acr_name=container_registry.registry.name,
            acr_username=container_registry.registry_username,  # type: ignore
            acr_password=container_registry.registry_password,  # type: ignore
            repository=f"{self.environment}/brainstormer",
            container_name="wa-brainstormer",
            identity=managed_identity.identity,
            host_name=HOSTNAME,
            certificate_id=f"/subscriptions/{self.subscription_id}/resourceGroups/{self.rg_name}/providers/Microsoft.App/managedEnvironments/wa-brainstormer-container-app-environment-prod/managedCertificates/brainstormer.cwa.viadee.clou-wa-brain-250429061001",
            environment_variables=environment_variables,
            secrets=secrets,
            opts=self.opts,
        )

        action_group = create_action_group(
            name=f"{self.project_name}-{self.environment}-action-group",
            rg_name=self.rg_name,
            location="germanywestcentral",
            group_short_name="bs-ag",
            opts=self.opts,
        )

        create_cpu_usage_alert(
            name=f"{self.project_name}-{self.environment}-cpu-usage-alert",
            rg_name=self.rg_name,
            location="global",
            threshold=150000000,
            scopes=[container_app.container_app.id],
            action_group=action_group,
            opts=self.opts,
        )

        create_requests_alert(
            name=f"{self.project_name}-{self.environment}-requests-alert",
            rg_name=self.rg_name,
            location="global",
            threshold=500,
            scopes=[container_app.container_app.id],
            action_group=action_group,
            opts=self.opts,
        )
