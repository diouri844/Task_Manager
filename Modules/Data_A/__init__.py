import sqlite3
from tkinter import messagebox
from Modules.Date import *
from Modules.File_Generator import *
def create_data_A(root, id_folder):
	if is_date(root.date_get_visa.get()) == True:
		data = [
			root.update_visa.get(),
			root.update_biyi.get(),
			root.date_get_visa.get()
		]
	else:
		messagebox.showerror("Erreur D enregistrement!", "Date Non Disponible ")
		return
	try:
		connexion = sqlite3.connect("DB_Config/Tasks_DBA.db")
		cursor = connexion.cursor()
		command = "INSERT INTO Advanced_data VALUES (Null,'"+str(data[0])+"','"+str(data[1])+"','"+str(data[2])+"',"+str(id_folder)+")"
		copier_command = command
		command = cursor.execute(command)
		generate_insert_file("Advanced_data",copier_command,"INSERT_A_Data_"+str(id_folder))
		messagebox.showinfo("Info !", "Enregistrement bien terminé!")
		connexion.commit()
	except Exception as e:
		print("[Error] "+str(e))
		messagebox.showerror("Erreur D enregistrement!", e)
		connexion.rollback()
	finally:
		cursor.close()
		connexion.close()
		root.update_window.advance_window.destroy()
	return

def delet_data_A(id_folder):
	try:
		connexion = sqlite3.connect("DB_Config/Tasks_DBA.db")
		cursor = connexion.cursor()
		command = "DELETE FROM Advanced_data WHERE FolderId="+str(id_folder)
		copier_command = command
		command = cursor.execute(command)
		connexion.commit()
		generate_delet_file("Advanced_data", copier_command, "DELETE_Advanced_data_"+str(id_folder))
		messagebox.showinfo("Info !", "Supression bien terminé!")
	except Exception as e:
		messagebox.showerror("Erreur!", e)
		connexion.rollback()
	finally:
		cursor.close()
		connexion.close()
	return

def get_data_A(folder_id):
	try:
		connexion = sqlite3.connect("DB_Config/Tasks_DBA.db")
		cursor = connexion.cursor()
		command = "SELECT * FROM Advanced_data WHERE FolderId="+str(folder_id)
		command = cursor.execute(command)
		return command.fetchall()[0]
	except Exception as e:
		print("[Error] : "+str(e))
		messagebox.showerror(e, "Impossible d'ouvrir l'emplacement du fichier ")
		return []
	finally:
		cursor.close()
		connexion.close()