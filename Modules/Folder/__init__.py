import sqlite3
from tkinter import messagebox
import csv
from Modules.File_Generator import *
from Modules.Data import *
from Modules.Data_A import *

def create_folder(data):
    # etablir connexion au dba : 
    response = 0
    try:
        connexion = sqlite3.connect("DB_Config/Tasks_DBA.db")
        cursor = connexion.cursor()
        command="INSERT INTO Folder VALUES (Null,'"+str(data[0])+"','"+str(data[1])+"','"+str(data[2])+"','"+str(data[3])+"','"+str(data[4])+"','"+str(data[5])+"','"+str(data[6])+"','"+str(data[7])+"','"+str(data[8])+"','"+str(data[9])+"','"+str(data[10])+"','"+str(data[11])+"','"+str(data[12])+"','"+str(data[13])+"','"+str(data[14])+"')"
        copier_command = command
        command = cursor.execute(command)
        connexion.commit()
        messagebox.showinfo("Info !", "Enregistrement(partie 1) bien terminé!")
        response = 1
        generate_insert_file("Folder",copier_command,"INSERT_Folder_"+str(data[0]))
    except Exception as e:
        messagebox.showerror("Erreur D enregistrement!", e)
        connexion.rollback()
    finally:
        cursor.close()
        connexion.close()

    return response

def get_id_folder_by(name):
    try:
        connexion = sqlite3.connect("DB_Config/Tasks_DBA.db")
        cursor = connexion.cursor()
        command = "SELECT Folder.Id FROM Folder WHERE Folder.Name='"+str(name)+"'"
        command = cursor.execute(command)
        return command.fetchone()[0]
    except Exception as e:
        messagebox.showerror("Erreur D enregistrement!", e)
        return 0
    finally:
        cursor.close()
        connexion.close()

def get_folder_liste():
    try:
        connexion = sqlite3.connect("DB_Config/Tasks_DBA.db")
        cursor = connexion.cursor()
        command = "SELECT * FROM Folder"
        command = cursor.execute(command)
        resultat = command.fetchall()
        return resultat
    except Exception as e:
        print(e)
        return []
    finally:
        cursor.close()
        connexion.close()

#///////////////////////////////////////

def update_folder(root,id):
    data = [root.update_name.get(),
                    root.update_age.get(),
                    root.update_cin.get(),
                    root.update_job1.get(),
                    root.update_job2.get(),
                    root.update_job3.get(),
                    root.update_window.combo_avance.get(),
                    root.update_window.combo_engagement.get(),
                    root.update_phone1.get(),
                    root.update_phone2.get()]
    print("[Operation : Update Folder ] :     id :   "+str(id))
    print("[Operation : Update Folder ] :     data :   "+str(data))
    try:
        connexion = sqlite3.connect("DB_Config/Tasks_DBA.db")
        cursor = connexion.cursor()
        command = "UPDATE Folder SET name='"+str(data[0])+"', Age='"+str(data[1])+"', Cin='"+str(data[2])+"',Job1='"+str(data[3])+"',Job2='"+str(data[4])+"',Job3='"+str(data[5])+"',Phone_Number1='"+str(data[8])+"',Phone_Number2='"+str(data[9])+"' WHERE Id="+str(id)
        copier = command
        command = cursor.execute(command)
        messagebox.showinfo("Info !", "Modification bien terminé")
        connexion.commit()
        update_data_folder(id,data[6],data[7])
        generate_update_file("Folder",copier,"Update_Folder"+str(id))
        root.update_window.destroy() 
    except Exception as e:
        messagebox.showerror("Erreur De modification !", e)
        print("[Error] : "+str(e))
        connexion.rollback()
    finally:
        cursor.close()
        connexion.close()
    return

def delet_folder(root,id):
    if root.connexion[3]=="Private":
        try:
            connexion = sqlite3.connect("DB_Config/Tasks_DBA.db")
            cursor = connexion.cursor()
            command = "DELETE FROM Folder WHERE Id="+str(id)
            copier_comand = command
            command = cursor.execute(command)
            connexion.commit()
            messagebox.showinfo("Information De Supression !", "Supression Du Dossier Numero "+str(id)+" est bien Terminé")
            delet_data_folder(id)
            delet_data_A(id)
            # mise a jour du fenetre :
            root.enabel_menu()
            root.canva.destroy()
            root.label.destroy()
            root.tableau.destroy()
            root.btn_update.destroy()
            root.btn_delet.destroy()
            root.btn_cancel.destroy()
            generate_delet_file("Folder",copier_comand,"DELETE Folder"+str(id))
        except Exception as e:
            messagebox.showerror("Erreur De Supression !", e)
            connexion.rollback()
        finally:
            cursor.close()
            connexion.close()
    else:
        messagebox.showerror("Probleme de vie privé ","Le compte connecté n est pas definie comme un super utilisateur")
    return

def get_job_liste():
    try:
        connexion = sqlite3.connect("DB_Config/Tasks_DBA.db")
        cursor = connexion.cursor()
        command = "SELECT Job1,job2,Job3 FROM Folder"
        command = cursor.execute(command)
        resultat = command.fetchall()
    except Exception as e:
        print("[Error ] : "+str(e))
        resultat = []
    finally:
        cursor.close()
        connexion.close()
    return resultat

def get_city_liste():
    try:
        connexion = sqlite3.connect("DB_Config/Tasks_DBA.db")
        cursor = connexion.cursor()
        command = "SELECT City FROM Folder"
        command = cursor.execute(command)
        resultat = command.fetchall()
    except Exception as e:
        print("[Error ] : "+str(e))
        resultat = []
    finally:
        cursor.close()
        connexion.close()
    return resultat

def get_folder_by_id(id):
    try:
        connexion = sqlite3.connect("DB_Config/Tasks_DBA.db")
        cursor = connexion.cursor()
        command = "SELECT * FROM Folder WHERE Folder.Id="+str(id)
        command = cursor.execute(command)
        return command.fetchall()[0]
    except Exception as e:
        print("[ERROR ] : "+str(e))
        return []
    finally:
        cursor.close()
        connexion.close()

def count_folders():
    try:
        connexion = sqlite3.connect("DB_Config/Tasks_DBA.db")
        cursor = connexion.cursor()
        command = "SELECT count(*) FROM folder"
        command = cursor.execute(command)
        return command.fetchone()[0]
    except Exception as e:
        print("[ERROR] : "+str(e))
        return 0
    finally:
        cursor.close()
        connexion.close()

def find_folders_by(job,sex,city,avance,engagement):
    try:
        connexion = sqlite3.connect("DB_Config/Tasks_DBA.db")
        cursor = connexion.cursor()
        command = "SELECT * FROM Folder WHERE Sex='"+str(sex)+"'AND City='"+str(city)+"' AND Job1='"+str(job)+"' OR Job2='"+str(job)+"' OR Job3='"+str(job)+"'"
        command = cursor.execute(command)
        primary_resultat = command.fetchall()
        secondary_result = []
        for element in primary_resultat:
            res_element = get_data_folder_by_id(element[0])
            if res_element[1] == avance and res_element[2] == engagement:
                secondary_result.append(element)
        return secondary_result
    except Exception as e:
        messagebox.showerror("Erreur !", e)
        return []
    finally:
        cursor.close()
        connexion.close()

def get_all_folders_by(date_t):
    try:
        connexion = sqlite3.connect("DB_Config/Tasks_DBA.db")
        cursor = connexion.cursor()
        command = "SELECT Folder.Name,Folder.Education_Leve,Data.Avance,Data.Engagement FROM Folder,Data WHERE Data.FolderId = Folder.Id AND Data.Date='"+str(date_t)+"'"
        command = cursor.execute(command)
        return command.fetchall()
    except Exception as e:
        print("[Error] : "+str(e))
        return []
    finally:
        cursor.close()
        connexion.close()

def get_folder_by_critaire(text):
    try:
        connexion = sqlite3.connect("DB_Config/Tasks_DBA.db")
        cursor = connexion.cursor()
        command = "SELECT * FROM Folder WHERE Name='"+str(text)+"' OR Cin='"+str(text)+"' OR Education_Leve='"+str(text)+"' OR Age='"+str(text)+"' OR City='"+str(text)+"' OR Sex='"+str(text)+"' OR Phone_Number1='"+str(text)+"' OR Phone_Number2='"+str(text)+"' OR Pay1='"+str(text)+"' OR Pay2='"+str(text)+"' OR Pay3='"+str(text)+"' OR Job1='"+str(text)+"' OR Job2='"+str(text)+"' OR Job3='"+str(text)+"'"                               
        command = cursor.execute(command)
        return command.fetchall()
    except Exception as e:
        print("[Error] :"+str(e))
        return []
    finally:
        cursor.close()
        connexion.close()