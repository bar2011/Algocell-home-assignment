class MaxTokenNumberExceededError(Exception):
	message = """Maximum token number that the model can take was exceeded:\n
Maximum is {maxTokens}, and received {tokenNumber}.\n
To resolve this error, you could try to remove data files, or shorten your current request."""
	def __init__(self, maxTokens, tokenNumber) -> None:
		self.message = self.message.replace("{maxTokens}", str(maxTokens)).replace("{tokenNumber}", str(tokenNumber))
		super().__init__(self.message)
