from langchain_community.llms.llamacpp import LlamaCpp
from langchain_core.callbacks import CallbackManager, StreamingStdOutCallbackHandler
from langchain_core.prompts import PromptTemplate

class MaxTokenNumberExceededError(Exception):
	message = """Maximum token number that the model can take was exceeded:\n
Maximum is {maxTokens}, and received {tokenNumber}.\n
To resolve this error, you could try to remove data files, or shorten your current request."""
	def __init__(self, maxTokens, tokenNumber) -> None:
		self.message = self.message.replace("{maxTokens}", str(maxTokens)).replace("{tokenNumber}", str(tokenNumber))
		super().__init__(self.message)

# Get question template from file
prompt_template = open("./prompt-template.txt", "r").read()

# StreamingStdOutCallbackHandler prints messages to the console when the LLM
# does an action with info to help debugging
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

max_acceptable_prompt_tokens = 30

def format_prompt(data, prompt):
	# Format the prompt from the template using the required arguments
	prompt = PromptTemplate.from_template(
		prompt_template
	).format(
		data=data,
		question=prompt
	)

	# Check that token number is less than maximum acceptable
	tokens = llm.get_num_tokens(prompt)
	if tokens > llm.n_ctx:
		return MaxTokenNumberExceededError(llm.n_ctx, tokens)

	return prompt

def ask(prompt):
	output = llm.invoke(prompt)
	return output
