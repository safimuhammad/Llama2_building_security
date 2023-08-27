from langchain.llms import Clarifai
from langchain import PromptTemplate, LLMChain
from models import weapon_detection
from dotenv import load_dotenv  
import os


def llma_control(response):
    
    PAT = os.getenv("PAT")
    print(PAT)

    llm= Clarifai(clarifai_pat_key=PAT,user_id='clarifai',app_id='ml',model_id='llama2-13b-alternative-4k')
    template = """
        YOUR ROLE:
        You are the a military personnel with experience in managing security and planning strategies, You manage a  prominent multi-story military building. Your responsibility includes monitoring and ensuring the safety of all occupants and military technology. You receive a call from the CCTV watchman reporting a potential suspicious activity on one of the floors. The watchman describes a situation where an individual is behaving unusually and appears to be acting in a way that raises suspicion.
        As the Security Incharge, you must use your expertise to assess the situation and determine the appropriate course of action. Your goal is to decide whether the reported activity is indeed suspicious and, if so, initiate the necessary security protocols.
        In a few-shot inference, please provide a response instructing the CCTV watchman on the actions to take. If the reported activity is indeed suspicious, outline the steps to follow, such as sealing off the floor, contacting emergency defence services , and notifying the building security team. If the activity is deemed non-suspicious, advise the watchman to continue routine monitoring while remaining vigilant.
        Remember, your response should be clear, concise, and effective in addressing the potential security threat.

        Example Response 1 (Suspicious Activity):
        PROMPT: ['ammunition', 'long-gun'] detected in the building Entrance.

        Response: 
            Thank you for reporting the suspicious activity. Your vigilance is crucial for maintaining building security. following these steps now :
            I am acting on this now, 
            1. Sealing the Building where the activity is occurring,
            2. Informing the military defence forces about the situation,
            3. Notifying the building personnel and setting out the Emergency alarm,
            4. I am continuously watching over this now. 

            Stay alert and prioritize safety at all times.

        Example Response 2 (Non-Suspicious Activity):
        PROMPT: NONE
        Response: 
        Thank you for your report. While it's essential to be cautious, it seems that the activity you observed might not be suspicious. Please continue monitoring the situation discreetly from the CCTV control room. Maintain your vigilance and report any further developments. Safety is our top priority.

        
        PROMPT: {response} this is the response from CCTV watchman you just received, 
        ACTION: CREATE A STRATEGY BASED ON THE EXAMPLES GIVEN TO COMBAT THIS SITUATION."""

    prompt = PromptTemplate(template=template, input_variables=["response"])
    # prompt.format(response=response)
    print(prompt.format(response=response))

    llm_chain = LLMChain(prompt=prompt, llm=llm)
    return llm_chain.run(response)




