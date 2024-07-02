from langchain_community.llms.llamacpp import LlamaCpp
from langchain_core.callbacks import CallbackManager, StreamingStdOutCallbackHandler
from langchain_core.prompts import PromptTemplate

# Get question template from file
question_template = open("./llm-templates/question-template.txt", "r").read()

# StreamingStdOutCallbackHandler prints messages to the console at special events
# that provide useful debugging info.
callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])

# Specified arguments so that messages will be short and non-repeating (as possible)
llm = LlamaCpp(
		model_path="/app/llama-2-7b.Q4_K_M.gguf",
		n_ctx=2048,
		max_tokens=None,
		top_p=1,
		stop=["[/Answer]", "\n"],
		callback_manager=callback_manager,
		verbose=True,  # Verbose is required to pass to the callback manager
)

def format_messages(messages):
	messagesText = ""

	for message in messages:
		roleAsWord = "Answer" if message["role"] == "assistant" else "Question"
		messagesText += f"[{roleAsWord}]\n{message["content"]}\n[/{roleAsWord}]\n"

	return messagesText

def format_question(data, previous_messages, question):
	prompt = PromptTemplate.from_template(
		question_template
	).format(
		data=data,
		previous_messages=previous_messages,
		question=question
	)
	return prompt

def ask(prompt):
	output = llm.invoke(prompt)
	return output
