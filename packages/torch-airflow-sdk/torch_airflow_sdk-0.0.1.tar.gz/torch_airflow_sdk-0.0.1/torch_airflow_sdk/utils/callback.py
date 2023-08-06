from torch_sdk.models.pipeline import PipelineRunResult, PipelineRunStatus
from torch_airflow_sdk.utils.torch_client import TorchDAGClient


# update pipeline with success status
def on_dag_failure_callback(context):
    pipeline_uid = context['dag'].__dict__['pipeline_uid']
    client = TorchDAGClient()
    pipeline_run = client.get_latest_pipeline_run(pipeline_uid)
    pipeline_run.update_pipeline_run(
        context_data={'status': 'failure', 'dag': 'torch_dag', 'context': str(context)},
        result=PipelineRunResult.FAILURE,
        status=PipelineRunStatus.FAILED
    )


# update pipeline with failed status
def on_dag_success_callback(context):
    pipeline_uid = context['dag'].__dict__['pipeline_uid']
    client = TorchDAGClient()
    pipeline_run = client.get_latest_pipeline_run(pipeline_uid)
    pipeline_run.update_pipeline_run(
        context_data={'status': 'success', 'dag': 'torch_dag', 'context': str(context)},
        result=PipelineRunResult.SUCCESS,
        status=PipelineRunStatus.COMPLETED
    )
