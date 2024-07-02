import pdfplumber
from langchain_core.prompts import PromptTemplate

def extract_data(feed):
  data = []
  with pdfplumber.open(feed) as pdf:
    pages = pdf.pages
    # For each page, add its data to the data list
    for p in pages:
      data.append(p.extract_text())
  return '\n'.join(data)

# Get data template from file
data_template = open("./llm-templates/data-template.txt").read()

def extract_formatted_data(pdf_file_list):
  # Extract text from file list
  pdf_files_text = ""
  for pdf_file in pdf_file_list:
    pdf_files_text += "\n------------\n" + extract_data(pdf_file)
  
  # Format text
  formatted_data = PromptTemplate.from_template(data_template).format(data=pdf_files_text)
  return formatted_data
