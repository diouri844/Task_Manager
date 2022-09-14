import sqlite3
from tkinter import messagebox

def create_link_folder_offre(id_folder,id_offre, root):
	try:
		connexion = sqlite3.connect("DB_Config/Tasks_DBA.db")
		cursor = connexion.cursor()
		command = 'INSERT INTO link_folder_offre VALUES (?,?)'
		values = (str(id_folder), str(id_offre))
		command = cursor.execute(command, values)
		connexion.commit()
		massage = "Dossier "+str(id_folder)+" Bien Ajouté a l'offre "+str(id_offre)+" "
		messagebox.showinfo("Info !", massage)
		root.btn_add_to_offre.destroy()
	except Exception as e:
		messagebox.showerror("Erreur D enregistrement link folder offre !", e)
	finally:
		cursor.close()
		connexion.close()
	return

def get_liste_id_folder(id_offre):
	try:
		connexion = sqlite3.connect("DB_Config/Tasks_DBA.db")
		cursor = connexion.cursor()
		command = "SELECT * FROM link_folder_offre WHERE link_folder_offre.Id_offre="+str(id_offre)
		command = cursor.execute(command)
		return command.fetchall()
	except Exception as e:
		print("[ERROR] : "+str(e))
		return []
	finally:
		cursor.close()
		connexion.close()

def count_folder_links_to_offre(offre_id):
	try:
		connexion = sqlite3.connect("DB_Config/Tasks_DBA.db")
		cursor = connexion.cursor()
		command = "SELECT count(*) FROM link_folder_offre WHERE link_folder_offre.Id_offre="+str(offre_id)
		command = cursor.execute(command)
		return command.fetchone()
	except Exception as e:
		print("[Error] : "+str(e))
		return 0
	finally:
		cursor.close()
		connexion.close()