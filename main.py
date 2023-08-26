from langchain.llms import Clarifai
from langchain import PromptTemplate, LLMChain
from models import weapon_detection



def llma_control(response):
    llm= Clarifai(clarifai_pat_key='b5ffeaa73b19476d94e8c481107583e7',user_id='meta',app_id='Llama-2',model_id='llama2-70b-chat')
    template = """ Title: Building Security Response Protocol

        Prompt:

        You are the security manager of a prominent multi-story building. Your responsibility includes monitoring and ensuring the safety of all occupants. You receive a call from the CCTV watchman reporting a potential suspicious activity on one of the floors. The watchman describes a situation where an individual is behaving unusually and appears to be acting in a way that raises suspicion.

        As the security manager, you must use your expertise to assess the situation and determine the appropriate course of action. Your goal is to decide whether the reported activity is indeed suspicious and, if so, initiate the necessary security protocols.

        In a few-shot inference, please provide a response instructing the CCTV watchman on the actions to take. If the reported activity is indeed suspicious, outline the steps to follow, such as sealing off the floor, contacting emergency services (911), and notifying the building security team. If the activity is deemed non-suspicious, advise the watchman to continue routine monitoring while remaining vigilant.

        Remember, your response should be clear, concise, and effective in addressing the potential security threat.

        Example Response 1 (Suspicious Activity):
        PROMPT: ['ammunition', 'long-gun'] detected in the building Entrance.

        Response: 
            Thank you for reporting the suspicious activity. Your vigilance is crucial for maintaining building security. Please follow these steps:
            1. Isolate and seal off the floor where the activity is occurring to prevent movement.
            2. Contact emergency services immediately by dialing 911 and provide them with all necessary information.
            3. Notify the building security team and provide them with the details of the situation.
            4. Continue to monitor the situation discreetly from the CCTV control room.
            Stay alert and prioritize safety at all times.

        Example Response 2 (Non-Suspicious Activity):
        PROMPT: NONE
        Response: 
        Thank you for your report. While it's essential to be cautious, it seems that the activity you observed might not be suspicious. Please continue monitoring the situation discreetly from the CCTV control room. Maintain your vigilance and report any further developments. Safety is our top priority.

        NOTE: PLEASE JUST PROVIDE A SINGLE RESPONSE AND A SINGLE COURSE OF ACTION
        
        PROMPT: {response} this is the response from CCTV watchman you just received act on it."""

    prompt = PromptTemplate(template=template, input_variables=["response"])
    # prompt.format(response='An armed man with hand gun detected at the floor 1')

    llm_chain = LLMChain(prompt=prompt, llm=llm)
    return llm_chain.run(response)



if __name__ == "__main__":
    response = weapon_detection()
    print(response,'response')
    print(llma_control(response))