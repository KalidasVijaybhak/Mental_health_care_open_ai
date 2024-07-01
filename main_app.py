from openai import OpenAI
import streamlit as st
import openai
import json
# st.title("ChatGPT-like clone")
st.set_page_config(
        page_title="Mind Care", page_icon=":brain:", layout="wide",
    )
st.title("Mind Care GPT")

# client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
client = OpenAI(api_key="sk-proj-S1T72cS09PcdYOIgH31ET3BlbkFJiepW8yBG1HyoCoOiOe3J")


@st.cache_data
def fup(uploaded_data):  
    for msg in uploaded_data:
                st.session_state.messages.append(msg)
                st.session_state.history.append(msg)
        
    


# if "openai_model" not in st.session_state:
#     st.session_state["openai_model"] = "gpt-3.5-turbo"


if "analysis" not in st.session_state:
    st.session_state.analysis = []

#     st.session_state.analysis.append({"role": "user", "content": """You are an advanced mental health specialist scan the previous conversations Give analysis in this format 
#     Analysis: 
#     else say Not enough conversation
# """})
    # print(st.session_state.analysis)
if "download" not in st.session_state:
    st.session_state.download = []

    # st.session_state.analysis.append({"role": "user", "content": "you are a mental health therapist act like a friend for every conversation and analyse conversation and find the problem with the person ask questions to the user but must not ask always use Patient Depression Questionnaire questions but user must not seem obvious of the quesiton , i will ask for analysis as a prompt then give me the analysis"})
st.markdown("""
    <style>
    section[data-testid="stSidebar"][aria-expanded="true"]{
        width: 10% !important;
    }
    section[data-testid="stSidebar"][aria-expanded="false"]{
        width: 10% !important;
    }
    </style>""", unsafe_allow_html=True)
with st.sidebar:
        option = st.selectbox("Model",
        ("gpt-3.5-turbo", ))

        #  st.set_option('client.fileUploader.button', (200, 50))
        for i in range(1):
                uploaded_file = st.file_uploader("Upload Chat", type="json")
        
        css = '''
    <style>
    [data-testid='stFileUploader'] {
        width: 10;
    }
    [data-testid='stFileUploader'] section {
        padding: 0;
        float: none;
        display: block;
    }
    
    [data-testid='stFileUploader'] section > input + div {
        display: none;
    }
    [data-testid='stFileUploader'] section + div {
        float: none;
        display: none;
        padding-top: 10px;
    }
    [data-testid='stFileUploader'] button {
        width: 200px;  /* Increased button width */
        height: 40px;  /* Increased button height */
        font-size: 16px;  /* Increased font size */
    }
</style>
'''

        st.markdown(css, unsafe_allow_html=True)
        #  uploaded_file = st.file_uploader("Choose a JSON file", type="json")
        
        if uploaded_file:
    # Read and parse JSON file
            uploaded_data = json.load(uploaded_file)
    
    # Assuming uploaded_data is a list of messages
            # for msg in uploaded_data:
            #     st.session_state.messages.append(msg)
            #     st.session_state.history.append(msg)
            fup(uploaded_data)
            
            # Display messages
            # for msg in st.session_state.messages:
            #     with st.chat_message(msg["role"]):
            #         st.markdown(msg["content"])
        with st.popover("System Prompt"): 
            custom_css = '''
    <style>
    .element-container:has(>.stTextArea), .stTextArea {
        width: 600px !important;
    }
    .stTextArea textarea {
        height: 300px;
    }
</style>
    '''

            st.markdown(custom_css, unsafe_allow_html=True)
            system_prompt = st.text_area("Enter System Prompt",value = f"""
Prompt:

You are an empathetic and professional mental health therapist dedicated to providing exceptional care to users act like a true friend. Greet users warmly and use open-ended questions to explore their feelings. Show genuine curiosity about their life, including their profession, hobbies, and interests, and engage deeply with these topics to build rapport and understand their context. Offer supportive and practical coping strategies tailored to their specific situations. Share relatable experiences to build trust and connection.
Characteristics:
- Friendly : Try to be caring and show interest, conversations should be friendly and not professional.
- Curious : Try to know more about the user like jobs, hobbies etc. 
- Assistance : Provide steps and methods to alleviate if analysis of previous conversations show distress etc.                    
                                                                                                                                                                         
Guidelines:
- After building a rapport with user take a PHQ9 test with their permission.  
- Keep general responses to a maximum of 50 words.
- Use up to 100 words for detailed advice and personalized suggestions.
- Maintain a friendly, professional tone at all times.
- Never recommend consulting other therapists.
""")

        
        
    
        
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = option


col1, col2, col3 = st.columns([1, 2, 7.5])
with col1:
    if st.button('New Chat'):
        st.session_state.messages = []
        st.session_state.history = []
        st.session_state.history.append({"role": "system", "content": system_prompt})
        st.session_state.analysis = []

    #     st.session_state.analysis.append({"role": "user", "content": """Scan the previous conversations Give analysis in this format 
    #     Analysis: 
    # else say Not enough conversation"""})
        st.session_state.download = []
        st.rerun()
with col2:
    with st.popover("Conversation Analysis"):
            st.session_state.analysis = []
            x = st.session_state.download.copy()
            if x :
                del x[0]
                msg = str(x)
            else :
                msg = "No conversation found"
            
            st.session_state.analysis.append({"role": "user", "content": f"""
        You are a professional mental health therapist.Your task is to Review the previous conversations between user and assistant delimited by triple backticks. '''{msg}''' and provide a detailed third-person analysis of the user's emotional state or mental health condition.If the  conversations are insufficient to form a clear analysis, state: "Not enough information from the conversations to provide an analysis. else provide the analysis with the following format:

        Analysis:
        - Conversation: [Give conversation count between 'assistant' and 'user']
        - Emotional State: [Brief description of user's emotions as points]
        - Mental Health Indicators: [Key indicators observed as points]
        - Potential Issues: [Possible underlying issues or conditions as points]
        """})
                # print('\n\n\nMessages')
                # print(msg)
            stream2 = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.analysis
            ],
            
        )   
            print('\n\n\nAnalysis')
            print(st.session_state.analysis)
            assistant_response = stream2.choices[0].message.content.strip()
            st.markdown(assistant_response)
    # st.markdown("hello")
with col3:
    data = st.session_state.download
    if data:
        del data[0]

    #  print('\nDownload session\n')
    #  print(type(data))
    #  print(st.session_state.download)
    

    
    data_json = json.dumps(data,indent = 4)

    # Create a downloadable text file
    st.download_button(
            
            label="Download Chat",
            data=data_json,
            file_name="Chat.json",
            # mime="text/plain"
        )
    


if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = option

if "messages" not in st.session_state:
    st.session_state.messages = []
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if "history" not in st.session_state:
    st.session_state.history = []

    st.session_state.history.append({"role": "system", "content": system_prompt})

# for message in st.session_state.history:



def get_openai_response(messages):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # or "gpt-3.5-turbo" depending on your model
        messages=messages
    )
    return response.choices[0].message['content']

if prompt := st.chat_input("Message.."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.history.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Mmm..."):
            stream = client.chat.completions.create(
                model=st.session_state["openai_model"],
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.history
                ],
                # stream=True,
            )
            response = stream.choices[0].message.content.strip()
            st.markdown(response)
            # usage = stream.usage
            with st.popover("Token Usage"):
                st.text(stream.usage)
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.session_state.history.append({"role": "assistant", "content": response})


# print(st.session_state.history)
# st.session_state.analysis = st.session_state.history.copy()
st.session_state.download = st.session_state.history.copy()
# print('\n')
# print(st.session_state.analysis )
