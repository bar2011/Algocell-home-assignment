import streamlit as st

from llm import ask, format_question
from extract_data import extract_data_from_file_list

st.title("Homework result:")

st.subheader("Upload data for the model to rely on:")

# Get and format data files
data_files = st.file_uploader(
  ":red[Important: once a new file is added or an old file is removed, all the messages would be resetted.]",
  type=("pdf"),
  accept_multiple_files=True,
  help="Add data files for the LLM to use"
)

def reset_messages():
  # Initialize messages a sample message from the LLM
  st.session_state["messages"] = [
    {"role": "assistant", "content": "How can I help you?"}
  ]
  # Save data in session_state
  st.session_state["data"] = extract_data_from_file_list(data_files)

if "messages" not in st.session_state:
  reset_messages()
if "is_processing" not in st.session_state:
  st.session_state.is_processing = False
if "prompt" not in st.session_state:
  st.session_state.prompt = ""
# Store previous uploaded files to detect changes
if "previous_data_files" not in st.session_state:
  st.session_state["previous_data_files"] = []

# Detect change in data_files
# Couldn't use onChange because reset_messages uses new data_files
st.session_state.data_files = data_files
if st.session_state.data_files != st.session_state.previous_data_files:
  reset_messages()
  st.session_state.previous_data_files = st.session_state.data_files

st.subheader("Ask the model question about the data uploaded:")

# Display all message except the intial data message
for msg in st.session_state.messages:
  st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input(disabled=st.session_state.is_processing):
  st.session_state.is_processing = True
  st.session_state.prompt = prompt
  st.rerun()

if st.session_state.is_processing:
  prompt = st.session_state.prompt
  # Display the user's message
  st.session_state.messages.append({"role": "user", "content": st.session_state.prompt})
  st.chat_message("user").write(st.session_state.prompt)

  # Format the user's question
  prompt = format_question(st.session_state.data, st.session_state.prompt)
  if isinstance(prompt, Exception):
    st.error(prompt.message)
    exit()
  # Ask the LLM and display its response
  response = ask(prompt)
  st.session_state.messages.append({"role": "assistant", "content": response})
  st.chat_message("assistant").write(response)

  st.session_state.is_processing = False
  st.rerun()
