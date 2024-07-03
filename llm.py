from langchain_community.llms.llamacpp import LlamaCpp
from langchain_core.callbacks import CallbackManager, StreamingStdOutCallbackHandler
from langchain_core.prompts import PromptTemplate
import errors

# Get question template from file
question_template = open("./llm-templates/question-template.txt", "r").read()

# StreamingStdOutCallbackHandler prints messages to the console at special events
# that provide useful debugging info.
callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])

# Specified arguments so that messages will be short and non-repeating (as possible)
llm = LlamaCpp(
	model_path="/app/llama-2-7b.Q4_K_M.gguf",
	n_ctx=2048,
	max_tokens=128,
	top_p=1,
	stop=["[/ANSWER]"],
	callback_manager=callback_manager,
	verbose=True,  # Verbose is required to pass to the callback manager
)

# question-template.txt = completeley overhal the template, and remove context via previous messages
# llm.py = Change llm parameters to better match new template, and remove need for previous messages, and add check for token count
# streamlit_app.py = Remove st.session_state.messages

def format_question(data, question):
	prompt = PromptTemplate.from_template(
		question_template
	).format(
		data=data,
		question=question
	)

	# Check that tokens is less than maximum acceptable
	tokens = llm.get_num_tokens(prompt)
	if tokens > llm.n_ctx:
		return errors.MaxTokenNumberExceededError(llm.n_ctx, tokens)

	return prompt

def ask(prompt):
	output = llm.invoke(prompt)
	return output
