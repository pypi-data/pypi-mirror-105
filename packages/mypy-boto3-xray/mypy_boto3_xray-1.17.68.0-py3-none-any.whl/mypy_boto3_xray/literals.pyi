"""
Type annotations for xray service literal definitions.

[Open documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_xray/literals.html)

Usage::

    ```python
    from mypy_boto3_xray.literals import BatchGetTracesPaginatorName

    data: BatchGetTracesPaginatorName = "batch_get_traces"
    ```
"""
import sys

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal

__all__ = (
    "BatchGetTracesPaginatorName",
    "EncryptionStatus",
    "EncryptionType",
    "GetGroupsPaginatorName",
    "GetSamplingRulesPaginatorName",
    "GetSamplingStatisticSummariesPaginatorName",
    "GetServiceGraphPaginatorName",
    "GetTimeSeriesServiceStatisticsPaginatorName",
    "GetTraceGraphPaginatorName",
    "GetTraceSummariesPaginatorName",
    "InsightCategory",
    "InsightState",
    "SamplingStrategyName",
    "TimeRangeType",
)

BatchGetTracesPaginatorName = Literal["batch_get_traces"]
EncryptionStatus = Literal["ACTIVE", "UPDATING"]
EncryptionType = Literal["KMS", "NONE"]
GetGroupsPaginatorName = Literal["get_groups"]
GetSamplingRulesPaginatorName = Literal["get_sampling_rules"]
GetSamplingStatisticSummariesPaginatorName = Literal["get_sampling_statistic_summaries"]
GetServiceGraphPaginatorName = Literal["get_service_graph"]
GetTimeSeriesServiceStatisticsPaginatorName = Literal["get_time_series_service_statistics"]
GetTraceGraphPaginatorName = Literal["get_trace_graph"]
GetTraceSummariesPaginatorName = Literal["get_trace_summaries"]
InsightCategory = Literal["FAULT"]
InsightState = Literal["ACTIVE", "CLOSED"]
SamplingStrategyName = Literal["FixedRate", "PartialScan"]
TimeRangeType = Literal["Event", "TraceId"]
