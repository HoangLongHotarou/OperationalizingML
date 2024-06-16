import json
import numpy as np
import onnxruntime as ort

def init():
    global model
    # Load the model
    model_path = os.path.join(os.getenv('AZUREML_MODEL_DIR'), 'model.onnx')
    model = ort.InferenceSession(model_path)

def run(data):
    try:
        # Parse input data
        input_data = np.array(json.loads(data)['data'])
        
        # Prepare input for the model
        input_name = model.get_inputs()[0].name
        result = model.run(None, {input_name: input_data})

        # Return the result
        return json.dumps({"result": result})
    except Exception as e:
        error = str(e)
        return json.dumps({"error": error})
