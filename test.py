from azureml.core import Workspace, Experiment
from azureml.pipeline.core import Pipeline, PipelineData
from azureml.pipeline.steps import ParallelRunStep
from azureml.train.automl import AutoMLConfig

# Load the Azure Machine Learning workspace
workspace = Workspace.from_config()

# Create an experiment
experiment_name = 'pipeline_parallel_automl'
experiment = Experiment(workspace, experiment_name)

# Define the input and output data
input_data = PipelineData('input_data', datastore=workspace.get_default_datastore())
output_data = PipelineData('output_data', datastore=workspace.get_default_datastore())

# Define the parallel run step
parallel_run_step = ParallelRunStep(
    name='parallel_run_step',
    parallel_run_config=parallel_run_config,
    inputs=[input_data],
    output=output_data,
    allow_reuse=True
)

# Define the AutoML configuration
automl_config = AutoMLConfig(
    task='classification',
    primary_metric='accuracy',
    training_data=input_data,
    label_column_name='label',
    n_cross_validations=5,
    iterations=10,
    experiment_timeout_minutes=30,
    compute_target=compute_target
)

# Create the pipeline
pipeline = Pipeline(workspace, steps=[parallel_run_step, automl_config])

# Run the pipeline
pipeline_run = experiment.submit(pipeline)
pipeline_run.wait_for_completion(show_output=True)