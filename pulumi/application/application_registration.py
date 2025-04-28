from typing import Optional
import pulumi
import pulumi_azuread as azuread


class ApplicationRegistration(pulumi.ComponentResource):
    def __init__(
        self,
        name: str,
        project_name: str,
        opts: Optional[pulumi.ResourceOptions] = None,
    ):
        super().__init__(
            f"custom:{project_name}:application-registration", name, {}, opts
        )

        marten = azuread.get_user(user_principal_name="marten.jostmann@viadee.de")
        daniel = azuread.get_user(user_principal_name="daniel.alile@viadee.de")

        combined_opts = pulumi.ResourceOptions.merge(
            opts, pulumi.ResourceOptions(protect=True)
        )
        self.app_registration = azuread.ApplicationRegistration(
            name,
            display_name=name,
            implicit_access_token_issuance_enabled=True,
            implicit_id_token_issuance_enabled=True,
            opts=combined_opts,
        )

        azuread.ApplicationOwner(
            f"{name}-{daniel.id}",
            application_id=self.app_registration.id,
            owner_object_id=daniel.object_id,
        )

        self.service_principal = azuread.ServicePrincipal(
            name,
            client_id=self.app_registration.client_id,
            app_role_assignment_required=False,
            owners=[marten.object_id, daniel.object_id],
            feature_tags=[
                {
                    "enterprise": True,
                    "gallery": True,
                }
            ],
            opts=opts,
        )
