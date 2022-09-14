def generate_update_file(tableau,command,file_name):
	try:
		with open('Temp/Update/'+str(file_name)+'.txt', 'w+', encoding="UTF8", newline='') as file:
			file.write(command)
	except Exception as e:
		print("[Error] : "+str(e))
	return

def generate_insert_file(tableau,command,file_name):
	try:
		with open('Temp/Insert/'+str(file_name)+'.txt', 'w+', encoding="UTF8", newline='') as file:
			file.write(command)
	except Exception as e:
		print("[Error] : "+str(e))
	return

def generate_delet_file(tableau,command,file_name):
	try:
		with open('Temp/Delet/'+str(file_name)+'.txt', 'w+', encoding="UTF8", newline='') as file:
			file.write(command)
	except Exception as e:
		print("[Error] : "+str(e))
	return