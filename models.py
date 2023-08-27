from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
from clarifai_grpc.grpc.api import resources_pb2, service_pb2, service_pb2_grpc
from clarifai_grpc.grpc.api.status import status_code_pb2
import time
import json
from dotenv import load_dotenv  
import os
import streamlit as st

def weapon_detection(image):
    if st.secrets:
        os.environ['PAT'] = st.secrets['PAT']
        os.environ['USER_ID'] = st.secrets['USER_ID']
        os.environ['WORKFLOW_ID'] = st.secrets['WORKFLOW_ID']
        os.environ['APP_ID'] = st.secrets['APP_ID']

    # load_dotenv()
    USER_ID = os.getenv("USER_ID")
    PAT = os.getenv("PAT")
    WORKFLOW_ID = os.getenv("WORKFLOW_ID")
    APP_ID = os.getenv("APP_ID")
    IMAGE_FILE_LOCATION = image
    channel = ClarifaiChannel.get_grpc_channel()
    stub = service_pb2_grpc.V2Stub(channel)

    metadata = (('authorization', 'Key ' + PAT),)

    userDataObject = resources_pb2.UserAppIDSet(user_id=USER_ID, app_id=APP_ID) # The userDataObject is required when using a PAT

    with open(IMAGE_FILE_LOCATION, "rb") as f:
        file_bytes = f.read()

    post_workflow_results_response = stub.PostWorkflowResults(
        service_pb2.PostWorkflowResultsRequest(
            user_app_id=userDataObject,  
            workflow_id=WORKFLOW_ID,
            inputs=[
                resources_pb2.Input(
                    data=resources_pb2.Data(
                        image=resources_pb2.Image(
                            base64=file_bytes
                        )
                    )
                )
            ]
        ),
        metadata=metadata
    )
    if post_workflow_results_response.status.code != status_code_pb2.SUCCESS:
        print(post_workflow_results_response.status)
        raise Exception("Post workflow results failed, status: " + post_workflow_results_response.status.description)

    # We'll get one WorkflowResult for each input we used above. Because of one input, we have here one WorkflowResult
    results = post_workflow_results_response.results[0]
    detections=[]
    for result in results.outputs[0].data.regions:
        for concept in result.data.concepts:
            if concept.value > 0.60:
                detections.append(concept.name)
                print(f"Name: {concept.name} , Value: {concept.value}")
              
    return f"{detections} detected in the building." if len(detections) >0 else None

