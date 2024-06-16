# Operationalizing AzureML
<p>This project is part of the Udacity Azure ML Nanodegree.</p>

The target of project is to help understand the pipeline process for releasing the model endpoint. Using AutoML to find the best model and create the AzureML Pipeline that can be reused and triggered by webhook. Once the ML endpoint is realeased, I will enable the application insight for the application to monitor and diagnostic the model endpoint. Using swagger-ui app to show documentation based on the swagger.json. Finally, we will consume the model endpoint to predict whether clients will subcribe to a bank term deposit.

## Architectural Diagram
![alt text](./img/image-7.png)

## Improve the project in the future
Using the AzureML Pipeline Parallel to improve the AzureML pipeline

## Key Steps
### Create a new AutoML run
1. Already registered dataset, it appears in the  Data assets of AzureML portal.
    ![alt text](./img/image.png)

1. Run the AutoML pipeline find the best models
    ![alt text](./img/image-10.png)

1. The best model: Voting Ensemble
    ![alt text](./img/image-13.png)
    ![alt text](./img/image-12.png)
    ![alt text](./img/image-11.png)

### Deploy a model and consume a model endpoint via an HTTP API
1. Deploy the model endpoint
    ![alt text](./img/image-14.png)

1. Enable the application insights
    - Before:
    ![alt text](./img/image-15.png)
    ![alt text](./img/image-16.png)

    - After:
    ![alt text](./img/image-17.png)
    ![alt text](./img/image-18.png)

1. Consume the model endpoint by using endpoint.py
    ![alt text](./img/image-19.png)
    ![alt text](./img/image-20.png)

1. Documentation for model endpoint (using swagger)
    - Download the swagger.json and store in swagger folder
    ![alt text](./img/image-23.png)
    - Run swaggerapi/swagger-ui container in docker
    ![alt text](./img/image-24.png)
    - Run the server.py and expose the swagger using swaggerapi/swagger-ui
    ![alt text](./img/image-25.png)
    ![alt text](./img/image-21.png)

1. Apache Benchmark (ab) runs against the HTTP API using authentication keys to retrieve performance results.
    ![alt text](./img/image-26.png)
    ![alt text](./img/image-22.png)

### Publish an ML Pipeline
1. Create and publish a pipeline
    ![alt text](./img/image-30.png)

1. Use a REST endpoint to interact with a Pipeline
    ![alt text](./img/image-27.png)
    ![alt text](./img/image-28.png)

1. Pipeline completed run
    ![alt text](./img/image-31.png)
    The duration is has the short time (just 2s) because in AutoMLStep enable allow_reuse
    ![alt text](./img/image-33.png)
    ![alt text](./img/image-32.png)

## Screen Recording
https://youtu.be/1wiR52wcl4k?si=Yy20EGZuKRubUM1Y

## Standout Suggestions
Expose the ONNX best model:
``` py
from azureml.train.automl.run import AutoMLRun

for step in pipeline_run.get_steps():
    if step.properties.get("StepType") == "AutoMLStep":
        automl_run = AutoMLRun(experiment, step.id)
        break

best_run = automl_run.get_best_child()
best_run_metrics = best_run.get_metrics()
print("---------------------------------------------------------")
print(f'Run Id: {best_run.id}')
print(f'Accuracy: {best_run_metrics["accuracy"]}')
print("---------------------------------------------------------")
print("the onnx model is saved in the outputs directory")
os.makedirs("./outputs", exist_ok = True)
best_run.download_file("outputs/model.onnx", "./outputs/automl_model.onnx")

```
![alt text](./img/image-34.png)