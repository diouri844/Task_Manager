import sqlite3
from tkinter import messagebox

def User_connect(user_name, user_password):
	try:
		connexion = sqlite3.connect("DB_Config/Tasks_DBA.db")
		cursor = connexion.cursor()
		command = "SELECT * FROM User WHERE User.Name='"+str(user_name)+"' AND User.Password='"+str(user_password)+"'"
		command = cursor.execute(command)
		result = command.fetchall()
	except Exception as e:
		messagebox.showerror("Connexion Error!", e)
	finally:
		cursor.close()
		connexion.close()
		result.append([])
	return result[0]

def Update_User(user_id,user_name,user_password,root):
	try:
		connexion = sqlite3.connect("DB_Config/Tasks_DBA.db")
		cursor = connexion.cursor()
		command = "UPDATE User SET Name='"+str(user_name)+"', Password='"+str(user_password)+"' WHERE Id="+str(user_id)
		command = cursor.execute(command)
		connexion.commit()
		messagebox.showinfo("Info !", "Modification bien terminé!")
		root.clear_widget_update()
	except Exception as e:
		messagebox.showerror("Erreur De Modification !", e)
		connexion.rollback()
	finally:
		cursor.close()
		connexion.close()
	return

def count_users():
	try:
		connexion = sqlite3.connect("DB_Config/Tasks_DBA.db")
		cursor = connexion.cursor()
		command = "SELECT count(*) FROM User"
		command = cursor.execute(command)
		return command.fetchone()[0]
	except Exception as e:
		print("[Error] : "+str(e))
		return 0
	finally:
		cursor.close()
		connexion.close()

def update_last_connexion(user_id, last_connexion):
	try:
		connexion = sqlite3.connect("DB_Config/Tasks_DBA.db")
		cursor = connexion.cursor()
		command = "UPDATE User SET LastConnexion='"+str(last_connexion)+"' WHERE Id="+str(user_id


			)
		command = cursor.execute(command)
		connexion.commit()
	except Exception as e:
		print("[Error] "+str(e))
		connexion.rollback()
	finally:
		cursor.close()
		connexion.close()
	return

def get_users():
	try:
		connexion = sqlite3.connect("DB_Config/Tasks_DBA.db")
		cursor = connexion.cursor()
		command = "SELECT * FROM User"
		command = cursor.execute(command)
		return command.fetchall()
	except Exception as e:
		print("[Error] "+str(e))
		return []
	finally:
		cursor.close()
		connexion.close()

def get_user_id_by_name(name):
	try:
		connexion = sqlite3.connect("DB_Config/Tasks_DBA.db")
		cursor = connexion.cursor()
		command = "SELECT Id FROM User WHERE Name='"+str(name)+"'"
		command = cursor.execute(command)
		return command.fetchone()[0]
	except Exception as e:
		print("[Error] "+str(e))
		return 0
	finally:
		cursor.close()
		connexion.close()

def create_user(root):
	data = [
		root.admin_space.entry_user_name.get(),
		root.admin_space.entry_user_password.get(),
		root.admin_space.combo_order.get()
	]
	try:
		connexion = sqlite3.connect("DB_Config/Tasks_DBA.db")
		cursor = connexion.cursor()
		command = "INSERT INTO User VALUES (Null,'"+str(data[0])+"','"+str(data[1])+"','"+str(data[2])+"',Null)"
		command = cursor.execute(command)
		messagebox.showinfo("Info !", "Enregistrement bien terminé!")
		connexion.commit()
	except Exception as e:
		messagebox.showerror("Erreur D enregistrement!", e)
		connexion.rollback()
	finally:
		cursor.close()
		connexion.close()
	return

def update_user_by_id(id_user, root):
	try:
		connexion = sqlite3.connect("DB_Config/Tasks_DBA.db")
		cursor = connexion.cursor()
		data_user = [
    		str(root.update_user_name.get()),
    		str(root.update_user_pswd.get()),
    		str(root.admin_window.combo_order.get())
    	]
		command = "UPDATE User SET Name='"+str(data_user[0])+"', Password='"+str(data_user[1])+"', Access='"+str(data_user[2])+"' WHERE Id="+str(id_user)
		command = cursor.execute(command)
		connexion.commit()
		messagebox.showinfo("Info !", "Modification bien terminé!")
	except Exception as e:
		messagebox.showerror("Erreur De Modification !", e)
		connexion.rollback()
	finally:
		cursor.close()
		connexion.close()
	return

def delet_user_by_admin(root):
	id_user_to_delet = root.admin_space.selcted_users_to_delet[0]
	name_user_to_delet = root.admin_space.selcted_users_to_delet[1]
	askyesno = messagebox.askyesno("Supprimer Utilisateur", "Voulez-vous vraiment Supprimer "+str(name_user_to_delet))
	if askyesno == True:
		try:
			connexion = sqlite3.connect("DB_Config/Tasks_DBA.db")
			cursor = connexion.cursor()
			command = "DELETE FROM User WHERE Id="+str(id_user_to_delet)
			command = cursor.execute(command)
			messagebox.showinfo("Info !", "l Utilisateur "+str(name_user_to_delet)+" est bien Supprimer")
			connexion.commit()		
		except Exception as e:
			messagebox.showerror("Erreur!", e)
			connexion.rollback()
		else:
			cursor.close()
			connexion.close()
	return