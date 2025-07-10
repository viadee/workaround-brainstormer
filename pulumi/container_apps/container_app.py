import pulumi
import pulumi_azure_native as azure_native
from typing import Optional, List
import subprocess


def get_latest_image(acr_name: str, repository: str, login_server: str) -> str:
    # Run the Azure CLI command to get the latest tag
    command = f"az acr repository show-tags --name {acr_name} --repository {repository} --orderby time_desc --top 1 --query [0] --output tsv"

    result = subprocess.run(
        command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True
    )

    latest_tag = result.stdout.strip()

    # If there is a latest tag, return the full image name
    if latest_tag:
        full_image_name = f"{login_server}/{repository}:{latest_tag}"
    else:
        # If there is no tag, return a default image
        full_image_name = "nginx:latest"

    return full_image_name


class ContainerApp(pulumi.ComponentResource):
    def __init__(
        self,
        name: str,
        project_name: str,
        resource_group_name: str,
        location: str,
        environment_id: pulumi.Input[str],
        external: bool,
        target_port: int,
        acr_login_server: pulumi.Input[str],
        acr_name: pulumi.Input[str],
        acr_username: Optional[pulumi.Input[str]],
        acr_password: Optional[pulumi.Input[str]],
        repository: str,
        container_name: str,
        identity: azure_native.managedidentity.UserAssignedIdentity,
        environment_variables: Optional[
            List[azure_native.app.EnvironmentVarArgs]
        ] = None,
        host_name: Optional[str] = None,
        certificate_id: Optional[str] = None,
        secrets: Optional[List[azure_native.app.SecretArgs]] = None,
        exposed_port: Optional[bool] = None,
        opts: Optional[pulumi.ResourceOptions] = None,
        min_replicas: int = 0,
        max_replicas: int = 1,
        cpu: int = 1,
        memory: str = "2Gi",
    ):
        super().__init__(f"custom:{project_name}:container-app", name, {}, opts)

        latest_image = pulumi.Output.all(acr_name, acr_login_server).apply(
            lambda args: get_latest_image(
                acr_name=args[0], repository=repository, login_server=args[1]
            )
        )

        _secrets = [
            azure_native.app.SecretArgs(name="registry-pwd", value=acr_password)
        ]

        if secrets:
            _secrets.extend(secrets)

        self.container_app = azure_native.app.ContainerApp(
            name,
            container_app_name=name,
            location=location,
            resource_group_name=resource_group_name,
            environment_id=environment_id,
            identity=azure_native.app.ManagedServiceIdentityArgs(
                type=azure_native.app.ManagedServiceIdentityType.USER_ASSIGNED,
                user_assigned_identities=[identity.id],
            ),
            configuration=azure_native.app.ConfigurationArgs(
                ingress=azure_native.app.IngressArgs(
                    allow_insecure=False,
                    exposed_port=exposed_port,
                    target_port=target_port,
                    external=external,
                    custom_domains=[
                        azure_native.app.CustomDomainArgs(
                            binding_type=azure_native.app.BindingType.SNI_ENABLED,
                            certificate_id=certificate_id,
                            name=host_name,
                        )
                    ]
                    if host_name and certificate_id
                    else None,
                    cors_policy=azure_native.app.CorsPolicyArgs(
                        allow_credentials=True,
                        allowed_origins=["*"],
                        allowed_headers=["*"],
                    ),
                ),
                registries=[
                    azure_native.app.RegistryCredentialsArgs(
                        server=acr_login_server,
                        username=acr_username,
                        password_secret_ref="registry-pwd",
                    )
                ],
                secrets=_secrets,
            ),
            template=azure_native.app.TemplateArgs(
                containers=[
                    azure_native.app.ContainerArgs(
                        name=container_name,
                        image=latest_image,
                        resources=azure_native.app.ContainerResourcesArgs(
                            cpu=cpu, memory=memory
                        ),
                        env=environment_variables,
                    )
                ],
                scale=azure_native.app.ScaleArgs(
                    min_replicas=min_replicas,
                    max_replicas=max_replicas,
                    rules=[
                        azure_native.app.ScaleRuleArgs(
                            name="http-scaler",
                            custom=azure_native.app.CustomScaleRuleArgs(
                                metadata={"concurrentRequests": "4"}, type="http"
                            ),
                        )
                    ],
                ),
            ),
            opts=opts,
        )
