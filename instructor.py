if __name__ == "main":
	exit()

import os, io


class Instructor:
	def __init__(self):
		self.instruction_name = []
		self.instruction_text = {}
		self.instruction_photo = {}
		self.instruction_document = {}
		self.path_instruction = "instruction"
		self.files_to_instruction()

	def files_to_instruction(self):
		for namedir_instruction in os.listdir(self.path_instruction):
			self.instruction_name.append(namedir_instruction)
			self.instruction_text[namedir_instruction] = []
			self.instruction_photo[namedir_instruction] = []
			self.instruction_document[namedir_instruction] = []

			instruction_files = os.listdir(self.path_instruction+"/"+namedir_instruction)
			instruction_files.sort()

			for i in instruction_files:
				pathfile = self.path_instruction+"/"+namedir_instruction+"/"+i

				if i[-3:] == "txt":
					with open(pathfile, 'r', encoding="utf-8") as text_instruction:
						self.instruction_text[namedir_instruction].append(text_instruction.read())
				elif i[-3:] == "png":
					with open(pathfile, 'rb') as photo_instruction:
						self.instruction_photo[namedir_instruction].append(photo_instruction.read())
				else:
					with open(pathfile, 'rb') as document_instruction:
						doc = document_instruction.read()
						file_doc = io.BytesIO(doc)
						file_doc.name = "Подключение к удаленному рабочему столу.docx"
						self.instruction_document[namedir_instruction].append(file_doc)
	def update_instruction(self):	
		self.files_to_instruction()
	
	def get_instruction_names(self):
		return self.instruction_name
	
	def get_instruction_text(self, name_instruction):
		return self.instruction_text[name_instruction]

	def get_instruction_photo(self, name_instruction):
		return self.instruction_photo[name_instruction]

	def get_instruction_document(self, name_instruction):
		return self.instruction_document[name_instruction]
