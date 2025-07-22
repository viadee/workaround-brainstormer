import pulumi
import pulumi_azure_native as azure_native


def create_action_group(
    name: str,
    rg_name: str,
    location: str,
    group_short_name: str,
    opts: pulumi.ResourceOptions | None = None,
) -> azure_native.monitor.ActionGroup:
    return azure_native.monitor.ActionGroup(
        name,
        resource_group_name=rg_name,
        location=location,
        enabled=True,
        group_short_name=group_short_name,
        email_receivers=[
            azure_native.monitor.EmailReceiverArgs(
                name="default", email_address="marten.jostmann@viadee.de"
            )
        ],
        opts=opts,
    )


def create_cpu_usage_alert(
    name: str,
    rg_name: str,
    location: str,
    threshold: float,
    scopes: list[str],
    action_group: azure_native.monitor.ActionGroup,
    opts: pulumi.ResourceOptions | None = None,
):
    azure_native.monitor.MetricAlert(
        name,
        resource_group_name=rg_name,
        location=location,
        enabled=True,
        evaluation_frequency="PT15M",
        rule_name=name,
        scopes=scopes,
        severity=2,
        window_size="PT30M",
        actions=[
            azure_native.monitor.MetricAlertActionArgs(action_group_id=action_group.id)
        ],
        criteria=azure_native.monitor.MetricAlertSingleResourceMultipleMetricCriteriaArgs(
            odata_type="Microsoft.Azure.Monitor.SingleResourceMultipleMetricCriteria",
            all_of=[
                azure_native.monitor.MetricCriteriaArgs(
                    criterion_type=azure_native.monitor.CriterionType.STATIC_THRESHOLD_CRITERION,
                    metric_name="UsageNanoCores",
                    name="CPU Usage Alert",
                    threshold=threshold,
                    time_aggregation=azure_native.monitor.TimeAggregationType.AVERAGE,
                    operator=azure_native.monitor.ComparisonOperationType.GREATER_THAN,
                ),
            ],
        ),
        opts=opts,
    )


def create_requests_alert(
    name: str,
    rg_name: str,
    location: str,
    threshold: float,
    scopes: list[str],
    action_group: azure_native.monitor.ActionGroup,
    opts: pulumi.ResourceOptions | None = None,
):
    azure_native.monitor.MetricAlert(
        name,
        resource_group_name=rg_name,
        location=location,
        enabled=True,
        evaluation_frequency="PT5M",
        rule_name=name,
        scopes=scopes,
        severity=2,
        window_size="PT15M",
        actions=[
            azure_native.monitor.MetricAlertActionArgs(action_group_id=action_group.id)
        ],
        criteria=azure_native.monitor.MetricAlertSingleResourceMultipleMetricCriteriaArgs(
            odata_type="Microsoft.Azure.Monitor.SingleResourceMultipleMetricCriteria",
            all_of=[
                azure_native.monitor.MetricCriteriaArgs(
                    criterion_type=azure_native.monitor.CriterionType.STATIC_THRESHOLD_CRITERION,
                    metric_name="Requests",
                    name="Max Requests Alert",
                    threshold=threshold,
                    time_aggregation=azure_native.monitor.TimeAggregationType.TOTAL,
                    operator=azure_native.monitor.ComparisonOperationType.GREATER_THAN,
                ),
            ],
        ),
        opts=opts,
    )
