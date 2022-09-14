import sqlite3
from tkinter import messagebox
from Modules.Folder import *
from Modules.Date import *
from Modules.File_Generator import *
import csv
import os

def convertToBinaryData(filename):
    # Convert digital data to binary format
    with open(filename, 'rb') as file:
        blobData = file.read()
    return blobData

def open_file(path):
    path=os.path.realpath(path)
    os.startfile(path)
    return

def clear_widget_next_step(root):
    root.canva.destroy()
    root.label.destroy()
    root.label_avance.destroy()
    root.canva_avance.destroy()
    root.combo_avance.destroy()
    root.combo_engagement.destroy()    
    root.canva_selfi.destroy()
    root.label_selfi.destroy()
    root.entry_selfi.destroy()
    root.btn_select_selfi.destroy()
    root.canva_passport.destroy()
    root.label_passport.destroy()
    root.entry_passport.destroy()
    root.btn_select_passport.destroy()
    root.canva_cv.destroy()
    root.label_cv.destroy()
    root.entry_cv.destroy()
    root.btn_select_cv.destroy()
    root.canva_date.destroy()
    root.label_date.destroy()
    root.entry_date.destroy()
    root.btn_save.destroy()
    root.enabel_menu()
    return

def create_data(id,root):
    root.data_liste.append(id)
    root.data_liste.append(root.combo_avance.get())
    root.data_liste.append(root.combo_engagement.get())
    if is_date(root.add_date.get()) == True:
        root.data_liste.append(root.add_date.get())
    else:
        messagebox.showerror("Erreur D enregistrement!", "Date Non Disponible ")
        return
    root.data_liste.append(root.add_passport.get())
    root.data_liste.append(root.add_selfi.get())
    root.data_liste.append(root.add_cv.get())
    #>
    print(root.data_liste)
    try:
        connexion = sqlite3.connect("DB_Config/Tasks_DBA.db")
        cursor = connexion.cursor()
        command = "INSERT INTO Data VALUES ("+str(root.data_liste[0])+",'"+str(root.data_liste[1])+"','"+str(root.data_liste[2])+"','"+str(root.data_liste[3])+"','"+str(root.data_liste[4])+"','"+str(root.data_liste[5])+"','"+str(root.data_liste[6])+"')"
        copier_command = command
        command = cursor.execute(command)
        connexion.commit()
        messagebox.showinfo("Info !", "Enregistrement(partie 2) bien terminé!")
        generate_insert_file("Data",copier_command,"INSERT_Data_"+str(root.data_liste[0]))
        clear_widget_next_step(root)
    except Exception as e:
        messagebox.showerror("Erreur D enregistrement!", e)
        connexion.rollback()
    finally:
        cursor.close()
        connexion.close()
    return

def delet_data_folder(folder_id):
    try:
        connexion = sqlite3.connect("DB_Config/Tasks_DBA.db")
        cursor = connexion.cursor()
        command = "DELETE FROM Data WHERE FolderId="+str(folder_id)
        copier_command = command
        command = cursor.execute(command)
        connexion.commit()
        generate_delet_file("Data",copier_command,"DELETE_Data_"+str(folder_id))
    except Exception as e:
        print("[Error] : "+str(e))
        connexion.rollback()
    finally:
        cursor.close()
        connexion.close()
    return

def update_data_folder(folder_id,folder_avance,folder_engagement):
    try:
        connexion = sqlite3.connect("DB_Config/Tasks_DBA.db")
        cursor = connexion.cursor()
        command = "UPDATE Data SET Avance='"+str(folder_avance)+"', Engagement='"+str(folder_engagement)+"' WHERE FolderId="+str(folder_id)
        copier_command = command
        command = cursor.execute(command)
        generate_update_file("Data", copier_command,"UPDATE_Data_"+str(folder_id))
        connexion.commit()
    except Exception as e:
        print("[Error] : "+str(e))
        connexion.rollback()
    finally:
        cursor.close()
        connexion.close()
    return

def get_data_folder_by_id(folder_id):
    try:
        connexion = sqlite3.connect("DB_Config/Tasks_DBA.db")
        cursor = connexion.cursor()
        command = "SELECT * FROM Data WHERE FolderId="+str(folder_id)
        command = cursor.execute(command)
        return command.fetchone()
    except Exception as e:
        print("[Error] : "+str(e))
        return []
    finally:
        cursor.close()
        connexion.close()
    