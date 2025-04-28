import pulumi
import pulumi_azure_native as azure_native

from deployments.dev.main import DevDeployment
from deployments.prod.main import ProdDeployment

project_name = "wa-brainstormer"
config = pulumi.Config()
azure_config = pulumi.Config("azure-native")
project_name = config.require("project_name")
dev_resource_group_name = config.require("rg_name_dev")
prod_resource_group_name = config.require("rg_name_prod")
location = azure_config.require("location")
analytics_workspace_name = config.require("analytics_workspace_name")

subscription_id_dev = config.require("subscription_id_dev")
subscription_id_prod = config.require("subscription_id_prod")

provider_dev = azure_native.Provider("azure-dev", subscription_id=subscription_id_dev)
provider_prod = azure_native.Provider(
    "azure-prod", subscription_id=subscription_id_prod
)


DevDeployment(
    project_name=project_name,
    rg_name=dev_resource_group_name,
    location=location,
    opts=pulumi.ResourceOptions(provider=provider_dev),
).build()

ProdDeployment(
    project_name=project_name,
    rg_name=prod_resource_group_name,
    location=location,
    opts=pulumi.ResourceOptions(provider=provider_prod),
).build()
