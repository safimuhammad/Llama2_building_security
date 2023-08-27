import streamlit as st
from PIL import Image
from models import weapon_detection
from main import llma_control
import os
import uuid
import time
import re
from dotenv import load_dotenv  



def save_uploaded_file(uploaded_file):
    # Generate a unique filename
    unique_filename = str(uuid.uuid4()) + "_" + uploaded_file.name

    # Save the file in the "uploads" folder
    save_path = os.path.join("uploads", unique_filename)    
    with open(save_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    return unique_filename

def main():
    st.title("DefenceIQ")
    st.write("Upload an image to decide the course of action")
    st.warning("Note: The Model might create blank or unrealistic responses or none at all due to high traffic on Clarifai")


    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

    st.sidebar.title("Strategy To Act")

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption='Uploaded Image', use_column_width=True)
        unique_filename = save_uploaded_file(uploaded_file)
      
        
        with st.spinner("Analyzing Potential Suspicion..."):
            status= weapon_detection(image=f"uploads/{unique_filename}")
            st.header(status)

    
    if uploaded_file:    
        st.sidebar.header('Verifying Detections')
        with st.spinner("Preparing Course of action..."):
            if status is None:
                st.write("No anomaly Detected")
            else:
                action_plan= llma_control(status)
                print(action_plan,"action plan")
                st.sidebar.write(action_plan)

                steps = re.split(r'\d+\.', action_plan)  # Split based on numbers followed by a period

                st.warning(steps[0].strip())  # Display the introduction

                for step in steps[1:]:
                    time.sleep(3)
                    st.warning(step.strip())  # Display each step
                    time.sleep(3)  # Pause for a few seconds between steps
                st.success("Alert sequence completed. Remember to ensure everyone's safety and stay vigilant.")

                
    
if __name__ == '__main__':
    # load_dotenv()
    if st.secrets:
        os.environ['PAT'] = st.secrets['PAT']
    if not os.path.exists("uploads"):
        os.makedirs("uploads")
    main()
