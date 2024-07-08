import streamlit as st

from llm import ask, format_prompt, llm, prompt_template, max_acceptable_prompt_tokens
from extract_data import extract_data_from_file_list


def init_session_variables():
  if "file_size_error" not in st.session_state:
    st.session_state.file_size_error = False
  if "previous_data_files" not in st.session_state:
    st.session_state.previous_data_files = []
  if "messages" not in st.session_state:
    st.session_state.messages = [
      {"role": "assistant", "content": "How can I help you?"}
    ]
  if "data" not in st.session_state:
    st.session_state.data = ""
  if "is_processing" not in st.session_state:
    st.session_state.is_processing = False
  if "prompt" not in st.session_state:
    st.session_state.prompt = ""


init_session_variables()

st.title("Home assignment result:")

st.subheader("Upload data for the model to rely on:")


def check_file_size_error():
  max_acceptable_data_tokens = llm.n_ctx - llm.get_num_tokens(prompt_template) - max_acceptable_prompt_tokens
  if llm.get_num_tokens(st.session_state.data) >= max_acceptable_data_tokens:
    st.session_state.file_size_error = True
    st.rerun()


def reset_messages():
  # Initialize messages a sample message from the LLM
  st.session_state.messages = [
    {"role": "assistant", "content": "How can I help you?"}
  ]
  # Save data in session_state
  st.session_state.data = extract_data_from_file_list(st.session_state.data_files)

  st.session_state.file_size_error = False


def handle_file_uploading():
  # Get and format data files
  data_files = st.file_uploader(
    ":red[Important: once a new file is added or an old file is removed, all the messages would be reset.]",
    type="pdf",
    accept_multiple_files=True,
    help="Add data files for the LLM to use"
  )

  # Detect change in data_files
  # Couldn't use onChange because reset_messages uses new data_files
  st.session_state.data_files = data_files
  if st.session_state.data_files != st.session_state.previous_data_files:
    st.session_state.previous_data_files = st.session_state.data_files
    reset_messages()
    check_file_size_error()

  if st.session_state.file_size_error:
    st.error("""The new file added adds too much text to the model.\n
  Consider shortening it and adding it again.""")


handle_file_uploading()

st.subheader("Ask the model question about the data uploaded:")

# Display messages
for msg in st.session_state.messages:
  if msg["role"] == "error":
    st.error(msg["content"])
    continue
  st.chat_message(msg["role"]).write(msg["content"])


def is_input_disabled():
  return st.session_state.is_processing or st.session_state.file_size_error


def check_user_input(prompt):
  if prompt:
    st.session_state.is_processing = True
    st.session_state.prompt = prompt
    st.rerun()


def give_prompt_to_llm():
  # Format the user's prompt
  prompt = format_prompt(st.session_state.data, st.session_state.prompt)
  # If format_prompt returned exception, display and exit
  if isinstance(prompt, Exception):
    st.session_state.is_processing = False
    st.session_state.messages.append({"role": "error", "content": prompt.message})
    st.rerun()
  # Ask the LLM and display its response
  response = ask(prompt)
  st.session_state.messages.append({"role": "assistant", "content": response})
  st.chat_message("assistant").write(response)


def handle_user_input():
  prompt = st.chat_input(disabled=is_input_disabled())

  check_user_input(prompt)

  if st.session_state.is_processing:
    # Remove error if there was
    if st.session_state.messages[-1]["role"] == "error":
      st.session_state.messages.pop()

    # Display the user's message
    st.session_state.messages.append({"role": "user", "content": st.session_state.prompt})
    st.chat_message("user").write(st.session_state.prompt)

    give_prompt_to_llm()

    # Un-disable the user input
    st.session_state.is_processing = False
    st.rerun()


handle_user_input()
