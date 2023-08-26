##############################################################################
# In this section, we set the user authentication, app ID, workflow ID, and  
# image URL. Change these strings to run your own example.
##############################################################################

USER_ID = 'na00lqzr91iu'
# Your PAT (Personal Access Token) can be found in the portal under Authentification
PAT = 'b5ffeaa73b19476d94e8c481107583e7'
APP_ID = 'testproject'
# Change these to make your own predictions
WORKFLOW_ID = 'workflow-d4ebf7'
IMAGE_URL = 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQBv-SC2ANPFUaxUx6zGTeBCfJPjNUaf3Xfcg&usqp=CAUU'


from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
from clarifai_grpc.grpc.api import resources_pb2, service_pb2, service_pb2_grpc
from clarifai_grpc.grpc.api.status import status_code_pb2
import time
import json 



def weapon_detection():
    USER_ID = 'na00lqzr91iu'
    # Your PAT (Personal Access Token) can be found in the portal under Authentification
    PAT = 'b5ffeaa73b19476d94e8c481107583e7'
    APP_ID = 'testproject'
    # Change these to make your own predictions
    WORKFLOW_ID = 'workflow-d4ebf7'
    IMAGE_URL = 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQBv-SC2ANPFUaxUx6zGTeBCfJPjNUaf3Xfcg&usqp=CAUU'

    channel = ClarifaiChannel.get_grpc_channel()
    stub = service_pb2_grpc.V2Stub(channel)

    metadata = (('authorization', 'Key ' + PAT),)

    userDataObject = resources_pb2.UserAppIDSet(user_id=USER_ID, app_id=APP_ID) # The userDataObject is required when using a PAT

    post_workflow_results_response = stub.PostWorkflowResults(
        service_pb2.PostWorkflowResultsRequest(
            user_app_id=userDataObject,  
            workflow_id=WORKFLOW_ID,
            inputs=[
                resources_pb2.Input(
                    data=resources_pb2.Data(
                        image=resources_pb2.Image(
                            url=IMAGE_URL
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
                # print(f"{concept.name} detected in the building Entrance.")
    return f"{detections} detected in the building Entrance." if len(detections) >0 else None

print(weapon_detection())