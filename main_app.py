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
            system_prompt = st.text_area("Enter multiline text",value = """You are a highly empathetic and supportive virtual mental health therapist. Your goal is to provide a safe, compassionate, and non-judgmental space for users to explore their feelings and thoughts. Use active listening skills, ask open-ended questions, and provide thoughtful reflections and coping strategies. Ensure your responses are concise, within a limit of 150 tokens per response. If you receive a question or request that is outside the scope of mental health support, kindly redirect the user back to the topic of mental health or inform them that you can only provide mental health-related assistance.
            Example response to non-context questions: "I'm here to support you with your mental health. Could we talk more about how you're feeling?"
            Token limit per response: 150 tokens""")

          
         
       
         
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = option


col1, col2, col3 = st.columns([1, 2, 7.5])
with col1:
    if st.button('New Chat'):
        st.session_state.messages = []
        st.session_state.history = []
        st.session_state.history.append({"role": "user", "content": system_prompt})
        st.session_state.analysis = []

    #     st.session_state.analysis.append({"role": "user", "content": """Scan the previous conversations Give analysis in this format 
    #     Analysis: 
    # else say Not enough conversation"""})
        st.session_state.download = []
        st.rerun()
with col2:
   with st.popover("Conversation Analysis"):
    x = st.session_state.download.copy()
    if x :
        del x[0]
    msg = str(x)
    st.session_state.analysis.append({"role": "user", "content": f"""You are a professional mental therapist Scan the previous conversations {msg} Give detailed 3rd person perspective analysis of what the user is feeling or suffering from in this format 
        Analysis: 
    else if conversations are not enugh to give an analysis say Not enough conversation """})
    print('\n\n\nMessages')
    print(msg)
    stream2 = client.chat.completions.create(
    model=st.session_state["openai_model"],
    messages=[
        {"role": m["role"], "content": m["content"]}
        for m in st.session_state.analysis
    ],
    
)   
    print(st.session_state.analysis)
    assistant_response = stream2.choices[0].message.content.strip()
    st.markdown(assistant_response)
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