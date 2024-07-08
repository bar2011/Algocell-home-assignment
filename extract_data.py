import pdfplumber


def extract_data_from_file(feed):
  data = []
  with pdfplumber.open(feed) as pdf:
    pages = pdf.pages
    # For each page, add its data to the data list
    for p in pages:
      data.append(p.extract_text())
  return '\n'.join(data)


def extract_data_from_file_list(pdf_file_list):
  # Extract text from file list
  pdf_files_text = ""
  for pdf_file in pdf_file_list:
    pdf_files_text += "\n------------\n" + extract_data_from_file(pdf_file)

  return pdf_files_text
