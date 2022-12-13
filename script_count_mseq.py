import os, re

import pandas as pd

#### Modules that need to be installed #####
# pip install pandas
# pip install openpyxl
#### #### #### #### #### #### #### #### #### 

##Write in a .txt file
def create_log_filter(id_file, file_line, log_file):
	with open(log_file, 'a') as log_file:
		log_file.write(str(id_file) + str(file_line))

##Navigate through the folder
def navigate_folder(folder):

	#List the files
	files = os.listdir(path_to_folder_list + folder)
	
	#Iterate through the file list
	for file_to_open in files:

		#Open each file
		file_opened = open(path_to_folder_list + folder + '\\' + file_to_open, 'r')
		print('Checking File: ' + file_to_open)
		#Create an identification
		id_for_log = folder + ';' + file_to_open + ';'
		
		#Read the file lines
		try:
			file_lines = file_opened.readlines()
		except Exception as e:
			print('Problems while reading lines:  ' + str(e))

		#Check if the file is already in the log
		if check_log_file(id_for_log) == 1:

			#Iterate through the file lines looking for the "text to search"
			for text_in_line in file_lines:	
				##'Run (take)'			
				if text_to_search_1 in text_in_line:  
					text_in_line = text_in_line.replace('Run (take)', ';Run (take);')
					text_in_line = text_in_line.replace(' [dispatch_element] ', ';')
					text_in_line = re.sub("\<.*?\>",";",text_in_line)
					
					create_log_filter(id_for_log, text_in_line, log_file)

				##'Run (out)'
				elif text_to_search_2 in text_in_line:
					text_in_line = text_in_line.replace('Run (out)', ';Run (out);')
					text_in_line = text_in_line.replace(' [dispatch_element] ', ';')
					text_in_line = re.sub("\<.*?\>",";",text_in_line)

					create_log_filter(id_for_log, text_in_line, log_file)

				##'Run (stop)'
				elif text_to_search_3 in text_in_line:
					text_in_line = text_in_line.replace('Run (stop)', ';Run (stop);')
					text_in_line = text_in_line.replace(' [dispatch_element] ', ';')
					text_in_line = re.sub("\<.*?\>",";",text_in_line)

					create_log_filter(id_for_log, text_in_line, log_file)

				##'Run (read)'
				elif text_to_search_4 in text_in_line:
					text_in_line = text_in_line.replace('Run (read)', ';Run (read);')
					text_in_line = text_in_line.replace(' [dispatch_element] ', ';')
					text_in_line = re.sub("\<.*?\>",";",text_in_line)

					create_log_filter(id_for_log, text_in_line, log_file)
				
				else:
					pass

#Check if the file is already in log
def check_log_file(id_to_search):
	log_to_read = open(log_file,'r')
	try:
		log_lines = log_to_read.readlines()
	except Exception as e:
		print('Problems while reading lines: ' + str(e))
	
	##If empty can write anything
	if len(log_lines) == 0:
		print('log_file.txt is empty!')
		return 1
		
		
	else:
		for text_in_log in log_lines:
			#If text is present in  the log, you don't need to write it again
			if id_to_search in text_in_log:
				print('File already checked! : '+ id_to_search)
				return 0
			else:
				pass

		return 1		
				
		
### Variables 
### List of each Media Sequencer folder
folder_list = list()

get_current_directory = os.scandir()
for file in get_current_directory:
	#List only folders
    if file.is_dir():
        folder_list.append(file.name)

path_to_folder_list = os.getcwd() + '\\'

log_file = path_to_folder_list + 'log_file.txt'

text_to_search_1 = 'Run (take)'
text_to_search_2 = 'Run (out)'
text_to_search_3 = 'Run (stop)'
text_to_search_4 = 'Run (read)'

#Iterate through the folder list
for folder in folder_list:
	print('Checking Folder: ' + folder)
	navigate_folder(folder)

df = pd.read_table('log_file.txt', sep=';')

#Remove empty column
for column in df:
	if 'Unnamed: ' in column:
		df.drop(columns=[column], axis=1, inplace=True) 

df.columns = ['Folder','File','Hour','Channel','Command','Art']
df.to_excel('Sheet.xlsx', 'Sheet1', index=False)
print('Finished!')	