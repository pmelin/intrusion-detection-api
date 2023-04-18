import os
import boto3
from pathlib import Path
import joblib
import pandas as pd
from io import BytesIO

MODEL_DISK_PATH = Path("/tmp/model.joblib")

model = None

def _get_model_from_disk():
    """
    Loads the model from disk.
    """
    if MODEL_DISK_PATH.exists():
        print("Loading model from disk...")
        return joblib.load(MODEL_DISK_PATH)
            
    return None

def _get_model_from_s3():
    """
    Downloads the model from S3 and loads it.
    """
    print("Loading latest model from s3...")
    with BytesIO() as f:
        boto3.client("s3").download_fileobj(Bucket=os.environ["DEPLOYMENT_AWS_BUCKET"], Key="production/model.joblib", Fileobj=f)
        f.seek(0)

        # loads the model
        loaded_model = joblib.load(f)

        # saves the loaded model to the disk to avoid 
        # loading it again on restart
        joblib.dump(loaded_model, MODEL_DISK_PATH)
        
        return loaded_model


def predict(json_record):
    """
    Predicts if the input metadata is an intrusion
    """
    global model

    input = pd.json_normalize(json_record) 

    if not model:
        # first we try to load the model from the disk
        # as it may have been downloaded last time the
        # the container ran
        model = _get_model_from_disk()

        if not model:
            # loads the model from the S3 bucket
            # and stores it on the disk
            model = _get_model_from_s3()
        
        print("Model loaded!")

    # performs the prediction using the model
    predictions_by_class = model.predict_proba(input)
    
    # returns if it's an intrusion or not
    return bool(predictions_by_class[0][1] == 1)


