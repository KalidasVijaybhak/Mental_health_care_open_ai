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
# client = OpenAI(api_key="sk-proj-S1T72cS09PcdYOIgH31ET3BlbkFJiepW8yBG1HyoCoOiOe3J")




# if "openai_model" not in st.session_state:
#     st.session_state["openai_model"] = "gpt-3.5-turbo"


if "analysis" not in st.session_state:
    st.session_state.analysis = []

    st.session_state.analysis.append({"role": "user", "content": "you are a mental health therapist act like a friend for every conversation and analyse conversation and find the problem with the person ask questions to the user but must not ask always use Patient Depression Questionnaire questions but user must not seem obvious of the quesiton , i will ask for analysis as a prompt then give me the analysis"})
    print(st.session_state.analysis)
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
        
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = option


col1 ,col2,col3= st.columns([1, 2, 7.5])
with col1:
    if st.button('New Chat'):
        st.session_state.messages = []
        st.session_state.history = []
        st.session_state.history.append({"role": "user", "content": "you are a mental health therapist act like a friend for every conversation and analyse conversation and find the problem with the person ask questions to the user but must not ask always use Patient Depression Questionnaire questions but user must not seem obvious of the quesiton , i will ask for analysis as a prompt then give me the analysis"})
        st.session_state.analysis = []

        st.session_state.analysis.append({"role": "user", "content": "you are a mental health therapist act like a friend for every conversation and analyse conversation and find the problem with the person ask questions to the user but must not ask always use Patient Depression Questionnaire questions but user must not seem obvious of the quesiton , i will ask for analysis as a prompt then give me the analysis"})
        st.session_state.download = []
        st.rerun()
with col2:
   with st.popover("Conversation Analysis"):
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

 print('\nDownload session\n')
 print(type(data))
 print(st.session_state.download)
 

 
 data_json = json.dumps(data,indent = 4)

# Create a downloadable text file
 st.download_button(
        
        label="Download Chat",
        data=data_json,
        file_name="Chat.txt",
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

    st.session_state.history.append({"role": "user", "content": "you are a mental health therapist act like a friend for every conversation and analyse conversation and find the problem with the person ask questions to the user but must not ask always use Patient Depression Questionnaire questions but user must not seem obvious of the quesiton , i will ask for analysis as a prompt then give me the analysis"})

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
st.session_state.analysis = st.session_state.history.copy()
st.session_state.download = st.session_state.history.copy()
# print('\n')
# print(st.session_state.analysis )