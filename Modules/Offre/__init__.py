import sqlite3
from tkinter import messagebox
from tkinter import END
from Modules.Folder import get_folder_liste
from Modules.Date import *

def create_offre(root):
	if is_greater(root.add_debut_date_offre.get(),root.add_fin_date_offre.get()) == True:
		data = [root.entry_titel.get(),
		root.add_debut_date_offre.get(),
		root.add_fin_date_offre.get(),
		root.combo_offre_pay.get(),
		root.combo_offre_job.get()
		]
	else:
		messagebox.showerror("Erreur D enregistrement!", "Date Non Disponible ")
		return
	try:
		connexion = sqlite3.connect("DB_Config/Tasks_DBA.db")
		cursor = connexion.cursor()
		command = "INSERT INTO Offre VALUES (Null,'"+str(data[0])+"','"+str(data[1])+"','"+str(data[2])+"','"+str(data[3])+"','"+str(data[4])+"')"
		command = cursor.execute(command)
		connexion.commit()
		messagebox.showinfo("Info !", "Enregistrement bien terminé!")
		folders = get_folder_liste()
		for element in folders:
			if element[8] == root.combo_offre_job.get() or element[9] == root.combo_offre_job.get() or element[10] == root.combo_offre_job.get():
				root.selected_folder_tab.insert('',END, values=(str(element[1]), str(element[3]), str(element[4])))
		root.btn_offre_save['state'] = "disabled"
	except Exception as e:
		messagebox.showerror("Erreur D enregistrement!", e)
		connexion.rollback()
	finally:
		cursor.close()
		connexion.close()
	return

def  get_offre_id_by_name(name):
	try:
		connexion = sqlite3.connect("DB_Config/Tasks_DBA.db")
		cursor = connexion.cursor()
		command = "SELECT Offre.Id FROM Offre WHERE Offre.Titel='"+str(name)+"'"
		command = cursor.execute(command)
		return command.fetchone()[0]
	except Exception as e:
		print("[Error ]:    "+str(e))
		return 0
	finally:
		cursor.close()
		connexion.close()

def get_offre_liste():
	try:
		connexion = sqlite3.connect("DB_Config/Tasks_DBA.db")
		cursor = connexion.cursor()
		command = "SELECT * FROM Offre"
		command = cursor.execute(command)
		return command.fetchall()
	except Exception as e:
		print("[Error] : "+str(e))
		return []
	finally:
		cursor.close()
		connexion.close()

def count_offre():
	try:
		connexion = sqlite3.connect("DB_Config/Tasks_DBA.db")
		cursor = connexion.cursor()
		command = "SELECT count(*) FROM Offre"
		command = cursor.execute(command)
		return command.fetchone()[0]
	except Exception as e:
		print("[Error] "+str(e))
		return 0
	finally:
		cursor.close()
		connexion.close()

def remove_offre(name_offre):
	try:
		connexion = sqlite3.connect("DB_Config/Tasks_DBA.db")
		cursor = connexion.cursor()
		cursor_seconde = connexion.cursor()
		id_offre = get_offre_id_by_name(name_offre)
		command = "DELETE FROM link_folder_offre WHERE link_folder_offre.Id_offre="+str(id_offre)
		command = cursor.execute(command)
		connexion.commit()
		command_seconde = "DELETE FROM Offre WHERE Offre.Id="+str(id_offre)
		command_seconde = cursor_seconde.execute(command_seconde)
		connexion.commit()
		messagebox.showinfo("Info !", "Operation bien Terminé")
	except Exception as e:
		print("[Error] : "+str(e))
		connexion.rollback()
	finally:
		cursor_seconde.close()
		cursor.close()
		connexion.close()
	return

def get_all_offre_by(date_t):
	try:
		connexion = sqlite3.connect("DB_Config/Tasks_DBA.db")
		cursor = connexion.cursor()
		command = "SELECT Offre.Id,Offre.Titel,Offre.Pay,Offre.job,count(link_folder_offre.Id_offre) FROM Offre,link_folder_offre WHERE link_folder_offre.Id_offre=Id AND Offre.Date_D='"+str(date_t)+"' OR Offre.Date_F='"+str(date_t)+"'"
		command = cursor.execute(command)
		return command.fetchall()
	except Exception as e:
		print("[Error] : "+str(e))
		return []
	finally:
		cursor.close()
		connexion.close()

def get_offre_by_critaire(text):
	try:
		connexion = sqlite3.connect("DB_Config/Tasks_DBA.db")
		cursor = connexion.cursor()
		command = "SELECT * FROM Offre WHERE Titel='"+str(text)+"' OR Pay='"+str(text)+"' OR job='"+str(text)+"'"
		command = cursor.execute(command)
		return command.fetchall()
	except Exception as e:
		print("[Error] "+str(e))
		return []
	finally:
		cursor.close()
		connexion.close()