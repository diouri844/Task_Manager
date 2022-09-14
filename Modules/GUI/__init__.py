from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import messagebox
from tkinter import filedialog

from Modules.Folder import *
from Modules.Data import *
from Modules.Offre import *
from Modules.Link_folder_Offre import *
from Modules.Users import *
from Modules.Data_A import *
import csv
import os
import sqlite3

def open_csv_data(name):
    id = str(get_id_folder_by(name))
    try:
        connexion = sqlite3.connect("DB_Config/Tasks_DBA.db")
        cursor = connexion.cursor()
        command = "SELECT * FROM Data WHERE FolderId="+str(id)
        command = cursor.execute(command)
        return command.fetchone()
    except Exception as e:
        print("[Error] : "+str(e))
        return []
    finally:
        cursor.close()
        connexion.close()

def open_for_selfi(root, type_fi):
    actuelle = os.path.expanduser("~")
    if type_fi == 'selfi':
        root.filname = filedialog.askopenfilename(initialdir=actuelle, title="Selectionné une image ",
                                                filetypes=[('Png files', '*.png'),('jpg files', '*.jpg'), ('Pdf files', '*.pdf') ])
        root.add_selfi.set(root.filname)
        print("Selfi path : "+str(root.add_selfi.get()))
    if type_fi == 'passeport':
        root.filname = filedialog.askopenfilename(initialdir=actuelle, title="Selectionné une image ",
                                                filetypes=[('Png files', '*.png'),('jpg files', '*.jpg'), ('Pdf files', '*.pdf')])
        root.add_passport.set(root.filname)
        print("Passeport path : "+str(root.add_passport.get()))
    if type_fi =='cv':
        root.filname = filedialog.askopenfilename(initialdir=actuelle, title="Selectionné une fichier ",
                                                filetypes=[('Pdf files', '*.pdf'), ('Png files', '*.png'),('jpg files', '*.jpg')])
        root.add_cv.set(root.filname)
        print("Cv path : "+str(root.add_cv.get()))
    return

def open_for_advanced_data(root, type_fi):
    actuelle = os.path.expanduser("~")
    if type_fi == 'visa':
        root.advanced_fil_visa = filedialog.askopenfilename(initialdir=actuelle, title="Selectionné une image/fichier ",
                                                filetypes=[('Png files', '*.png'),('jpg files', '*.jpg'), ('Pdf files', '*.pdf') ])
        root.update_visa.set(root.advanced_fil_visa)
        print(str(type_fi)+"path : "+str(root.update_visa.get()))
    if type_fi == 'biyi':
        root.advanced_fil_biyi = filedialog.askopenfilename(initialdir=actuelle, title="Selectionné une image/fichier ",
                                                filetypes=[('Png files', '*.png'),('jpg files', '*.jpg'), ('Pdf files', '*.pdf') ])
        root.update_biyi.set(root.advanced_fil_biyi)
        print(str(type_fi)+" path : "+str(root.update_biyi.get()))

    return

def enabel_button(key):
    key.btn_update['state'] = 'normal'
    key.btn_delet['state'] = 'normal'
    selected = key.tableau.focus()
    key.selected_values = key.tableau.item(selected, 'values')
    return

def enabel_add_offre(key):
    try:
        key.btn_add_to_offre.destroy()
    except Exception as e:
        print("[Error] : "+str(e))
    finally:
        selected = key.selected_folder_tab.focus()
        key.selected_values_tab = key.selected_folder_tab.item(selected, 'values')
        print(key.selected_values_tab)
        id_offre = get_offre_id_by_name(key.add_offre_titel.get())
        id_folder = get_id_folder_by(key.selected_values_tab[0])
        key.btn_add_to_offre = Button(key.window, text="Ajouté a l'offre ", font="Arial-BoldMT 10 underline",
                bg=key.fg_secondary, fg=key.fg_color, bd=0, 
                command=lambda:create_link_folder_offre(id_folder, id_offre, key))
        key.btn_add_to_offre.place(relx=0.9, rely=0.65)
    return

def enabel_add_folder_to_offre(key):
    #key.enabel_menu()
    key.btn_add_new_folder['state'] = "normal"
    # retourner l element selectionné :
    selected = key.offre_liste.focus()
    key.selected_values_offre = key.offre_liste.item(selected, 'values')
    try:
        key.tableau_folder.destroy()
    except Exception as e:
        print("[Error ] : "+str(e))
    finally:
        tete = ("Nom & Prenom", "Cin")
        key.tableau_folder = ttk.Treeview(key.window, height=18, show="headings", column=tete)
        key.tableau_folder.column("Nom & Prenom", width="200", anchor=CENTER)
        key.tableau_folder.column("Cin", width="200", anchor=CENTER)
        key.tableau_folder.heading("Nom & Prenom", text="Nom & Prenom")
        key.tableau_folder.heading("Cin", text="Cin")
        # remplissage du tableau des dossier liée a cette offre :
        id_offre = get_offre_id_by_name(str(key.selected_values_offre[0]))
        liste_id_dossier = get_liste_id_folder(id_offre)
        print(liste_id_dossier)
        for element in liste_id_dossier:
            id_dossier = element[0]
            dossier_current = get_folder_by_id(id_dossier)
            key.tableau_folder.insert('',END, values=(str(dossier_current[1]), str(dossier_current[3])))
        # emplacer les elements dans la fenetre 
        key.tableau_folder.place(relx=0.53, rely=0.2)
    return

def select_folder_to_add(root):
    root.window_select_folder = Toplevel(bg=root.fg_color, bd=0)
    root.window_select_folder.geometry("700x550")
    root.window_select_folder.resizable(0,0)
    root.window_select_folder.iconbitmap("Images/logo2.ico")
    root.window_select_folder.title(' Ajouté Dossier a l offre  : '+str(root.selected_values_offre[0]))
    my_image = Image.open('Images/icons8-dossier-de-documents-50.png')
    my_icon = ImageTk.PhotoImage(my_image)
    root.window_select_folder.canva = Label(root.window_select_folder, image=my_icon, height=50, width=50, bg=root.fg_color)
    root.window_select_folder.canva.image = my_icon
    root.window_select_folder.label_titre = Label(root.window_select_folder, text="Ajouté Dossier a cette offre ",
        font="Arial-BoldMT 20 underline", bd=0, bg=root.fg_color, fg=root.fg_secondary)
    # tableau des dossier disponible a l operation d ajoute :
    colones = ("Nom & Prenom", "Cin")
    root.window_select_folder.tab_folders = ttk.Treeview(root.window_select_folder, height=15, show="headings", column=colones)
    root.window_select_folder.tab_folders.column("Nom & Prenom", width="200", anchor=CENTER)
    root.window_select_folder.tab_folders.column("Cin", width="200", anchor=CENTER)
    root.window_select_folder.tab_folders.heading("Nom & Prenom", text="Nom & Prenom")
    root.window_select_folder.tab_folders.heading("Cin", text="Cin")
    # implementation du body du tableau :
    # liste des id des dossier liée a cette offre : 
    id_offre = get_offre_id_by_name(str(root.selected_values_offre[0]))

    id_folders = get_liste_id_folder(id_offre)

    folders = get_folder_liste()
    
    for offre in get_offre_liste():
        if offre[0] == id_offre:
            job = offre[5]
    ids = []
    for id in id_folders:
        ids.append(id[0])

    for folder in folders:
        if not folder[0] in ids and (folder[8]== job or folder[9]== job or folder[10]== job) :
            root.window_select_folder.tab_folders.insert('', END, values=(str(folder[1]), str(folder[3])))
    #btn d ajouté le dossier selectionné:
    root.window_select_folder.btn_add = Button(root.window_select_folder, text="Ajouté a l'offre ",
        font="Arial-BoldMT 9 underline", bg=root.fg_secondary, fg=root.fg_color, bd=0, state="disabled")
    # emplacer les widgets dans la fenetre :
    root.window_select_folder.canva.place(relx=0.05, rely=0.1)
    root.window_select_folder.label_titre.place(relx=0.15, rely=0.12)
    root.window_select_folder.tab_folders.place(relx=0.15, rely=0.2)
    root.window_select_folder.btn_add.place(relx=0.6, rely=0.8)
    return

def advanced_updating(root):
    # Strings Var to Use : 
    root.update_visa = StringVar()
    root.update_biyi = StringVar()
    root.date_get_visa = StringVar()
    # create a top level window for advaced updating data : 
    root.update_window.advance_window = Toplevel(bg=root.fg_color)
    root.update_window.advance_window.geometry("400x550")
    root.update_window.advance_window.resizable(0,0)
    root.update_window.advance_window.iconbitmap("Images/logo2.ico")
    root.update_window.advance_window.title(' Modifications avancé sur:'+str(root.selected_values[0]))
    id = get_id_folder_by(root.selected_values[0])
    data = get_data_A(id)
    if len(data)!=0:
        root.update_visa.set(str(data[1]))
        root.update_biyi.set(str(data[2]))
        root.date_get_visa.set(str(data[3]))
    my_image = Image.open('Images/icons8-options-64.png')
    my_icon = ImageTk.PhotoImage(my_image)
    root.update_window.advance_window.canva = Label(root.update_window.advance_window, image=my_icon, height=64, width=64, bg=root.fg_color)
    root.update_window.advance_window.canva.image = my_icon
    root.update_window.advance_window.label_titel = Label(root.update_window.advance_window, text="Options Avancé...",
        font="Arial-BoldMT 13 underline", bg=root.fg_color, fg=root.fg_secondary, bd=0)
    # outils entrer des données : 
    my_image = Image.open('Images/TextBox_Bg.png')
    my_icon = ImageTk.PhotoImage(my_image)
    
    root.update_window.advance_window.canva_visa_path = Label(root.update_window.advance_window, image=my_icon, height=65, width=340, bg=root.fg_color)
    root.update_window.advance_window.canva_visa_path.image = my_icon
    root.update_window.advance_window.label_visa_path = Label(root.update_window.advance_window, text="Visa  ", font="Arial-BoldMT 13",
                                bg="#F6F7F9", fg=root.fg_secondary)
    root.update_window.advance_window.entry_visa_path = Entry(root.update_window.advance_window, textvariable=root.update_visa, font="Arial-BoldMT 10",  fg="black",
                                bg="#F6F7F9", width=37, bd=0)
    root.update_window.advance_window.btn_open_visa_file = Button(root.update_window.advance_window, text="Ouvrir",
        font="Arial-BoldMT 8 underline", bd=0, fg=root.fg_secondary, bg="#F6F7F9", command=lambda:open_for_advanced_data(root,'visa'))

    
    root.update_window.advance_window.canva_bille_path = Label(root.update_window.advance_window, image=my_icon, height=65, width=340, bg=root.fg_color)
    root.update_window.advance_window.canva_bille_path.image = my_icon
    root.update_window.advance_window.label_bille_path = Label(root.update_window.advance_window, text="Billet  ", font="Arial-BoldMT 13",
                                bg="#F6F7F9", fg=root.fg_secondary)
    root.update_window.advance_window.entry_bille_path = Entry(root.update_window.advance_window, textvariable=root.update_biyi, font="Arial-BoldMT 10",  fg="black",
                                bg="#F6F7F9", width=37, bd=0)
    root.update_window.advance_window.btn_open_bille_file = Button(root.update_window.advance_window, text="Ouvrir",
        font="Arial-BoldMT 8 underline", bd=0, fg=root.fg_secondary, bg="#F6F7F9", command=lambda:open_for_advanced_data(root,'biyi'))


    root.update_window.advance_window.canva_bille_date = Label(root.update_window.advance_window, image=my_icon, height=65, width=340, bg=root.fg_color)
    root.update_window.advance_window.canva_bille_date.image = my_icon
    root.update_window.advance_window.label_bille_date = Label(root.update_window.advance_window, text="Date  ", font="Arial-BoldMT 13",
                                bg="#F6F7F9", fg=root.fg_secondary)
    root.update_window.advance_window.entry_bille_date = Entry(root.update_window.advance_window, textvariable=root.date_get_visa, font="Arial-BoldMT 10",  fg="black",
                                bg="#F6F7F9", width=37, bd=0)
    id = get_id_folder_by(root.selected_values[0])
    root.update_window.advance_window.btn_save = Button(root.update_window.advance_window, text="Enregistré",
        font="Arial-BoldMT 9 underline", bd=0, bg=root.fg_secondary, fg=root.fg_color, command=lambda:create_data_A(root,id))


    root.update_window.advance_window.entry_bille_date.focus()
    # emplacer les elements dans la fenetres : 
    root.update_window.advance_window.canva.place(relx=0.15, rely=0.05)
    root.update_window.advance_window.label_titel.place(relx=0.3, rely=0.12)
    root.update_window.advance_window.canva_visa_path.place(relx=0.05, rely=0.2)
    root.update_window.advance_window.label_visa_path.place(relx=0.05, rely=0.21)
    root.update_window.advance_window.entry_visa_path.place(relx=0.05, rely=0.245)
    root.update_window.advance_window.btn_open_visa_file.place(relx=0.75, rely=0.26)
    
    root.update_window.advance_window.canva_bille_path.place(relx=0.05, rely=0.3)
    root.update_window.advance_window.label_bille_path.place(relx=0.05, rely=0.31)
    root.update_window.advance_window.entry_bille_path.place(relx=0.05, rely=0.345)
    root.update_window.advance_window.btn_open_bille_file.place(relx=0.75, rely=0.36)

    root.update_window.advance_window.canva_bille_date.place(relx=0.05, rely=0.4)
    root.update_window.advance_window.label_bille_date.place(relx=0.05, rely=0.41)
    root.update_window.advance_window.entry_bille_date.place(relx=0.05, rely=0.445)
    
    root.update_window.advance_window.btn_save.place(relx=0.75, rely=0.55)
    return

def get_selected_to_update(root):
    # create a seconde window for update :
    root.update_name = StringVar()
    root.update_age = StringVar()
    root.update_cin = StringVar()
    root.update_job1 = StringVar()
    root.update_job2 = StringVar()
    root.update_job3 = StringVar()
    root.update_phone1 = StringVar()
    root.update_phone2 = StringVar()
    
    # initialisation des input : 
    root.update_name.set(root.selected_values[0])
    root.update_age.set(root.selected_values[1])
    root.update_cin.set(root.selected_values[2])
    root.update_job1.set(root.selected_values[6])
    root.update_job2.set(root.selected_values[7])
    root.update_job3.set(root.selected_values[8])
    root.update_phone1.set(root.selected_values[9])
    root.update_phone2.set(root.selected_values[10])
    root.update_window = Toplevel(bg=root.fg_color, bd=0)
    root.update_window.geometry("400x700")
    root.update_window.resizable(0,0)
    root.update_window.iconbitmap("Images/logo2.ico")
    root.update_window.title(' Mettre a jour Dossier : '+str(root.selected_values[0]))
    my_image = Image.open('Images/icons8-dossier-ouvert-50.png')
    my_icon = ImageTk.PhotoImage(my_image)
    root.update_window.canva = Label(root.update_window, image=my_icon, height=50, width=50, bg=root.fg_color)
    root.update_window.canva.image = my_icon
    # input update system :
    my_image = Image.open('Images/TextBox_Bg.png')
    my_icon = ImageTk.PhotoImage(my_image)
    root.update_window.canva_name = Label(root.update_window, image=my_icon, height=65, width=340, bg=root.fg_color)
    root.update_window.canva_name.image = my_icon
    root.update_window.label_name = Label(root.update_window, text="Nom & Prenom ", font="Arial-BoldMT 13",
                                bg="#F6F7F9", fg=root.fg_secondary)
    root.update_window.entry_name = Entry(root.update_window, textvariable=root.update_name, font="Arial-BoldMT 13",  fg="black",
                                bg="#F6F7F9", width=37, bd=0)
    
    root.update_window.canva_age = Label(root.update_window, image=my_icon, height=65, width=340, bg=root.fg_color)
    root.update_window.canva_age.image = my_icon
    root.update_window.label_age = Label(root.update_window, text="Age ", font="Arial-BoldMT 13",
                                bg="#F6F7F9", fg=root.fg_secondary)
    root.update_window.entry_age = Entry(root.update_window, textvariable=root.update_age, font="Arial-BoldMT 13",  fg="black",
                                bg="#F6F7F9", width=37, bd=0)

    root.update_window.canva_cin = Label(root.update_window, image=my_icon, height=65, width=340, bg=root.fg_color)
    root.update_window.canva_cin.image = my_icon
    root.update_window.label_cin = Label(root.update_window, text="Cin ", font="Arial-BoldMT 13",
                                bg="#F6F7F9", fg=root.fg_secondary)
    root.update_window.entry_cin = Entry(root.update_window, textvariable=root.update_cin, font="Arial-BoldMT 13",  fg="black",
                                bg="#F6F7F9", width=37, bd=0)

    root.update_window.canva_job = Label(root.update_window, image=my_icon, height=99, width=340, bg=root.fg_color)
    root.update_window.canva_job.image = my_icon
    root.update_window.label_job = Label(root.update_window, text="Occupation ", font="Arial-BoldMT 13",
                                bg="#F6F7F9", fg=root.fg_secondary)

    root.update_window.entry_job1 = Entry(root.update_window, textvariable=root.update_job1, font="Arial-BoldMT 13",  fg="black",
                                bg="#F6F7F9", width=37, bd=0)
    root.update_window.entry_job2 = Entry(root.update_window, textvariable=root.update_job2, font="Arial-BoldMT 13",  fg="black",
                                bg="#F6F7F9", width=37, bd=0)
    root.update_window.entry_job3 = Entry(root.update_window, textvariable=root.update_job3, font="Arial-BoldMT 13",  fg="black",
                                bg="#F6F7F9", width=37, bd=0)

    root.update_window.canva_avance = Label(root.update_window, image=my_icon, height=65, width=340, bg=root.fg_color)
    root.update_window.label_avance = Label(root.update_window, text="Avance & Engagement ", font="Arial-BoldMT 13",
                                    bg="#F6F7F9", fg=root.fg_secondary)
    root.update_window.combo_avance = ttk.Combobox(root.update_window,value=['Oui', 'Non'], state='readonly', width=20, height=0)
    root.update_window.combo_engagement = ttk.Combobox(root.update_window,value=['Oui', 'Non'], state='readonly', width=20, height=0)
    
    root.update_window.canva_phone = Label(root.update_window, image=my_icon, height=99, width=340, bg=root.fg_color)
    root.update_window.canva_phone.image = my_icon
    root.update_window.label_phone = Label(root.update_window, text="N° Télé ", font="Arial-BoldMT 13",
                                bg="#F6F7F9", fg=root.fg_secondary)
    root.update_window.entry_phone1 = Entry(root.update_window, textvariable=root.update_phone1, font="Arial-BoldMT 13",  fg="black",
                                bg="#F6F7F9", width=37, bd=0)
    root.update_window.entry_phone2 = Entry(root.update_window, textvariable=root.update_phone2, font="Arial-BoldMT 13",  fg="black",
                                bg="#F6F7F9", width=37, bd=0)


    element = open_csv_data(str(root.selected_values[0]))
    id = get_id_folder_by(root.selected_values[0])
    print("id folder :     "+str(id))
    root.update_window.combo_avance.current(1)
    root.update_window.combo_engagement.current(1)
    root.update_window.title = Label(root.update_window, text=str(element[3]), font="Arial-BoldMT 15 underline",
                                bg=root.fg_color, fg=root.fg_secondary)
    
    if str(element[1]) == 'Oui':
        root.update_window.combo_avance.current(0)
    if str(element[2]) == 'Oui':
        root.update_window.combo_engagement.current(0)
    
    root.update_window.open_selfi = Button(root.update_window, text="Ouvrir Photo Personnelle", 
        font="Arial-BoldMT 8 underline", bg=root.fg_color, fg= root.fg_secondary, bd=0, command=lambda:open_file(element[4]))
    root.update_window.open_passport = Button(root.update_window, text="Ouvrir Passport", 
        font="Arial-BoldMT 8 underline", bg=root.fg_color, fg= root.fg_secondary, bd=0, command=lambda:open_file(element[5]))
    root.update_window.open_cv = Button(root.update_window, text="Ouvrir Cv", 
        font="Arial-BoldMT 8 underline", bg=root.fg_color, fg= root.fg_secondary, bd=0, command=lambda:open_file(element[6]))
    root.update_window.advance_update = Button(root.update_window, text="Modifications Avancé ", 
        font="Arial-BoldMT 8 underline", bg=root.fg_color, fg= root.fg_secondary, bd=0, command=lambda:advanced_updating(root))

    root.update_window.btn_save = Button(root.update_window, text="Enregistré", font="Arial-BoldMT 10 underline",
                                    bg=root.bg_color, fg=root.fg_color, bd=0, command=lambda:update_folder(root,id))

    root.update_window.btn_cancel = Button(root.update_window, text="Annuler", font="Arial-BoldMT 10 underline",
                                bg=root.fg_secondary, fg=root.fg_color, bd=0, command=lambda:root.update_window.destroy())

    
    # placed widget in windwo :
    root.update_window.canva.place(relx=0.15, rely=0.05)
    root.update_window.title.place(relx=0.3, rely=0.08)
    root.update_window.canva_name.place(relx=0.05, rely=0.15)
    root.update_window.label_name.place(relx=0.05, rely=0.15)
    root.update_window.entry_name.place(relx=0.05, rely=0.2)

    root.update_window.canva_age.place(relx=0.05, rely=0.25)
    root.update_window.label_age.place(relx=0.05, rely=0.25)
    root.update_window.entry_age.place(relx=0.05, rely=0.29)

    root.update_window.canva_cin.place(relx=0.05, rely=0.34)
    root.update_window.label_cin.place(relx=0.05, rely=0.34)
    root.update_window.entry_cin.place(relx=0.05, rely=0.39)

    root.update_window.canva_job.place(relx=0.05, rely=0.44)
    root.update_window.label_job.place(relx=0.05, rely=0.44)
    root.update_window.entry_job1.place(relx=0.05, rely=0.47)
    root.update_window.entry_job2.place(relx=0.05, rely=0.5)
    root.update_window.entry_job3.place(relx=0.05, rely=0.53)

    root.update_window.canva_avance.place(relx=0.05, rely=0.58)
    root.update_window.label_avance.place(relx=0.05, rely=0.58)
    root.update_window.combo_avance.place(relx=0.05, rely=0.62)
    root.update_window.combo_engagement.place(relx=0.44, rely=0.62)

    root.update_window.canva_phone.place(relx=0.05, rely=0.67)
    root.update_window.label_phone.place(relx=0.05, rely=0.67)
    root.update_window.entry_phone1.place(relx=0.05, rely=0.71)
    root.update_window.entry_phone2.place(relx=0.05, rely=0.74)
    
    root.update_window.open_selfi.place(relx=0.66, rely=0.8)
    root.update_window.open_passport.place(relx=0.66, rely=0.83)
    root.update_window.open_cv.place(relx=0.66, rely=0.86)
    root.update_window.advance_update.place(relx=0.66, rely=0.89)

    root.update_window.btn_save.place(relx=0.6, rely=0.95)
    root.update_window.btn_cancel.place(relx=0.79, rely=0.95)
    return

def selected_to_delet(key):
    selected = key.offre_liste.focus()
    key.selected_values_offre = key.offre_liste.item(selected, 'values')
    response = messagebox.askyesno("Confirmé L'operation ", "Voulez vous vraiment Supprimer L offre : "+str(key.selected_values_offre[0]))
    if response:
        print(response)
        remove_offre(key.selected_values_offre[0])
        clear_widget_offre_delet(key)
        delet_offre(key)                
    return

def enabel_button_admin(key):
    key.admin_window.btn_update['state'] = "normal"
    selected = key.admin_window.liste_user.focus()
    key.admin_window.admin_selected_values = key.admin_window.liste_user.item(selected, 'values')
    return

def Add_folder(root):
    root.disabled_menu()
    root.add_name = StringVar()
    root.add_age = StringVar()
    root.add_cin = StringVar()
    root.add_city = StringVar()
    root.add_educate = StringVar()
    root.add_phone1 = StringVar()
    root.add_phone2 = StringVar()
    root.add_job1 = StringVar()
    root.add_job2 = StringVar()
    root.add_job3 = StringVar()

    my_image = Image.open('Images/icons8-ajouter-le-dossier-50.png')
    my_icon = ImageTk.PhotoImage(my_image)
    root.canva = Label(root.window, image=my_icon, height=70, width=70, bg=root.fg_color)
    root.canva.image = my_icon
    root.label = Label(root.window, text="Ajouter Dossier :" , font="Arial-BoldMT 20 underline",
            bg=root.fg_color, fg=root.fg_secondary, bd=0)
    # input system:
    my_image = Image.open('Images/TextBox_Bg.png')
    my_icon = ImageTk.PhotoImage(my_image)
    # ----------------------------------------------------------------------------------------------------------
    # Folder Name : 
    
    root.canva_user = Label(root.window, image=my_icon, height=65, width=340, bg=root.fg_color)
    root.canva_user.image = my_icon
    root.label_user = Label(root.window, text="Nom & Prenom ", font="Arial-BoldMT 13",
                                bg="#F6F7F9", fg=root.fg_secondary)
    root.entry_user = Entry(root.window, textvariable=root.add_name, font="Arial-BoldMT 13",  fg="black",
                                bg="#F6F7F9", width=37, bd=0)
    # Folder Age : 

    root.canva_age = Label(root.window, image=my_icon, height=65, width=340, bg=root.fg_color)
    root.canva_age.image = my_icon
    root.label_age = Label(root.window, text="Age  ", font="Arial-BoldMT 13",
                                bg="#F6F7F9", fg=root.fg_secondary)
    root.entry_age = Entry(root.window, textvariable=root.add_age, font="Arial-BoldMT 13",  fg="black",
                                bg="#F6F7F9", width=37, bd=0)

    # Folder Cin : 

    root.canva_cin = Label(root.window, image=my_icon, height=65, width=340, bg=root.fg_color)
    root.canva_cin.image = my_icon
    root.label_cin = Label(root.window, text="CIN  ", font="Arial-BoldMT 13",
                                bg="#F6F7F9", fg=root.fg_secondary)
    root.entry_cin = Entry(root.window, textvariable=root.add_cin, font="Arial-BoldMT 13",  fg="black",
                                bg="#F6F7F9", width=37, bd=0) 
    
    # Folder City : 

    root.canva_city = Label(root.window, image=my_icon, height=65, width=340, bg=root.fg_color)
    root.canva_city.image = my_icon
    root.label_city = Label(root.window, text="Ville  ", font="Arial-BoldMT 13",
                                bg="#F6F7F9", fg=root.fg_secondary)
    root.entry_city = Entry(root.window, textvariable=root.add_city, font="Arial-BoldMT 13",  fg="black",
                                bg="#F6F7F9", width=37, bd=0)

    # Folder Sex : 
    root.canva_sex = Label(root.window, image=my_icon, height=65, width=340, bg=root.fg_color)
    root.canva_sex.image = my_icon
    root.label_sex = Label(root.window, text="Sex & Diplome ", font="Arial-BoldMT 13",
                                bg="#F6F7F9", fg=root.fg_secondary)

    root.combo_sex = ttk.Combobox(root.window,value=['Homme', 'Femme'], state='readonly', width=20, height=1)
    root.combo_diplom = ttk.Combobox(root.window,value=['Oui', 'Non'], state='readonly', width=10, height=0)


    # Folder educate level :

    root.canva_educate = Label(root.window, image=my_icon, height=65, width=340, bg=root.fg_color)
    root.canva_educate.image = my_icon
    root.label_educate = Label(root.window, text="Niveau D'etude ", font="Arial-BoldMT 13",
                                bg="#F6F7F9", fg=root.fg_secondary)

    root.entry_educate = Entry(root.window, textvariable=root.add_educate, font="Arial-BoldMT 13",  fg="black",
                                bg="#F6F7F9", width=37, bd=0)

    # Folder Phone Number : 

    root.canva_phone = Label(root.window, image=my_icon, height=99, width=340, bg=root.fg_color)
    root.canva_phone.image = my_icon
    root.label_phone = Label(root.window, text="N° Télé  ", font="Arial-BoldMT 13",
                                bg="#F6F7F9", fg=root.fg_secondary)    

    root.entry_phone1 = Entry(root.window, textvariable=root.add_phone1, font="Arial-BoldMT 13",  fg="black",
                                bg="#F6F7F9", width=37, bd=0)
    root.entry_phone2 = Entry(root.window, textvariable=root.add_phone2, font="Arial-BoldMT 13",  fg="black",
                                bg="#F6F7F9", width=37, bd=0)

    # Folder Job : 

    root.canva_job = Label(root.window, image=my_icon, height=99, width=340, bg=root.fg_color)
    root.canva_job.image = my_icon
    root.label_job = Label(root.window, text="Occupation ", font="Arial-BoldMT 13",
                                bg="#F6F7F9", fg=root.fg_secondary)

    root.entry_job1 = Entry(root.window, textvariable=root.add_job1, font="Arial-BoldMT 13",  fg="black",
                                bg="#F6F7F9", width=37, bd=0)
    root.entry_job2 = Entry(root.window, textvariable=root.add_job2, font="Arial-BoldMT 13",  fg="black",
                                bg="#F6F7F9", width=37, bd=0)
    root.entry_job3 = Entry(root.window, textvariable=root.add_job3, font="Arial-BoldMT 13",  fg="black",
                                bg="#F6F7F9", width=37, bd=0)


    # Folder Pay :

    root.canva_pay = Label(root.window, image=my_icon, height=140, width=340, bg=root.fg_color)
    root.canva_pay.image = my_icon
    root.label_pay = Label(root.window, text="Pays ", font="Arial-BoldMT 13", bg="#F6F7F9", fg=root.fg_secondary)
    pays =["عمان" , "سلطنة عمان ", " الامارات" , "السعودية" , " البحرين" , "قطر" , "الكويت"]
    root.entry_pay1 = ttk.Combobox(root.window,value=pays, state='readonly', width=50, height=0)
    root.entry_pay2 = ttk.Combobox(root.window,value=pays, state='readonly', width=50, height=0)
    root.entry_pay3 = ttk.Combobox(root.window,value=pays, state='readonly', width=50, height=0)

    root.btn_next = Button(root.window, text="Suivant ", font="Arial-BoldMT 13", fg=root.fg_color, bg=root.fg_secondary
        , bd=0, command= lambda:next_step_folder(root))
    root.btn_cancel = Button(root.window, text="Annuler ", font="Arial-BoldMT 13", bg=root.bg_color, fg=root.fg_color,
        bd=0, command= lambda:clear_widget_folder(root))

    root.entry_user.focus()
    root.combo_sex.current(0)
    root.combo_diplom.current(0)
    root.entry_pay1.current(0)
    root.entry_pay2.current(0)
    root.entry_pay3.current(0)
    # Emplacement des widget en fenetre :
    root.canva.place(relx=0.1, rely=0.06)
    root.label.place(relx=0.2, rely=0.1)
    
    root.label_user.place(relx=0.12, rely=0.2)
    root.canva_user.place(relx=0.12, rely=0.2)
    root.entry_user.place(relx=0.12, rely=0.25)

    root.canva_age.place(relx=0.12, rely=0.33)
    root.label_age.place(relx=0.12, rely=0.33)
    root.entry_age.place(relx=0.12, rely=0.38)

    root.canva_cin.place(relx=0.12, rely=0.46)
    root.label_cin.place(relx=0.12, rely=0.46)
    root.entry_cin.place(relx=0.12, rely=0.51)

    root.canva_city.place(relx=0.12, rely=0.57)
    root.label_city.place(relx=0.12, rely=0.57)
    root.entry_city.place(relx=0.12, rely=0.62)

    root.canva_sex.place(relx=0.12, rely=0.68)
    root.label_sex.place(relx=0.12, rely=0.68)
    root.combo_sex.place(relx=0.12, rely=0.73)
    root.combo_diplom.place(relx=0.3, rely=0.73)

    root.canva_educate.place(relx=0.5, rely=0.1)
    root.label_educate.place(relx=0.5, rely=0.1)
    root.entry_educate.place(relx=0.5, rely=0.15)

    root.canva_phone.place(relx=0.5, rely=0.23)
    root.label_phone.place(relx=0.5, rely=0.23)
    root.entry_phone1.place(relx=0.5, rely=0.28)
    root.entry_phone2.place(relx=0.5, rely=0.34)

    root.canva_job.place(relx=0.5, rely=0.42)
    root.label_job.place(relx=0.5, rely=0.42)
    root.entry_job1.place(relx=0.5, rely=0.47)
    root.entry_job2.place(relx=0.5, rely=0.5)
    root.entry_job3.place(relx=0.5, rely=0.53)


    root.canva_pay.place(relx=0.5, rely=0.6)
    root.label_pay.place(relx=0.5, rely=0.6)
    root.entry_pay1.place(relx=0.5, rely=0.65)
    root.entry_pay2.place(relx=0.5, rely=0.7)
    root.entry_pay3.place(relx=0.5, rely=0.75)

    root.btn_next.place(relx=0.75, rely=0.93)
    root.btn_cancel.place(relx=0.85, rely=0.93)
    return

def next_step_folder(root):
    if not len(root.add_name.get())==0 and not  len(root.add_age.get())==0 and not len(root.add_cin.get())==0 and not len(root.add_city.get())==0 and not len(root.add_educate.get())==0 and not len(root.add_phone1.get())==0 and not len(root.add_phone2.get())==0 and not len(root.add_job1.get())==0 and not len(root.add_job2.get())==0 and not len(root.add_job3.get())==0 :
        data = [root.add_name.get(),root.add_age.get(),root.add_cin.get(), root.add_city.get(),root.combo_sex.get(),root.add_educate.get(), root.combo_diplom.get(),root.add_job1.get(),root.add_job2.get(),root.add_job3.get(),root.entry_pay1.get(),root.entry_pay2.get(),root.entry_pay3.get(), root.add_phone1.get(),root.add_phone2.get()]
        response = create_folder(data)
        if response==1:
            clear_widget_folder(root)
            root.disabled_menu()
            my_image = Image.open('Images/icons8-ajouter-le-dossier-50.png')
            my_icon = ImageTk.PhotoImage(my_image)
            root.canva = Label(root.window, image=my_icon, height=70, width=70, bg=root.fg_color)
            root.canva.image = my_icon
            root.label = Label(root.window, text="Ajouter Dossier :" , font="Arial-BoldMT 20 underline",
                    bg=root.fg_color, fg=root.fg_secondary, bd=0)
            root.add_selfi = StringVar()
            root.add_passport = StringVar()
            root.add_cv = StringVar()
            root.add_date = StringVar()
            # input system:
            my_image = Image.open('Images/TextBox_Bg.png')
            my_icon = ImageTk.PhotoImage(my_image)

            # Data Avance & Engagement: 
            
            root.canva_avance = Label(root.window, image=my_icon, height=65, width=340, bg=root.fg_color)
            root.canva_avance.image = my_icon
            root.label_avance = Label(root.window, text="Avance & Engagement ", font="Arial-BoldMT 13",
                                    bg="#F6F7F9", fg=root.fg_secondary)
            root.combo_avance = ttk.Combobox(root.window,value=['Oui', 'Non'], state='readonly', width=20, height=0)
            root.combo_engagement = ttk.Combobox(root.window,value=['Oui', 'Non'], state='readonly', width=20, height=0)

            # Data blob (selfi,passport,cv): 

            root.canva_selfi = Label(root.window, image=my_icon, height=65, width=340, bg=root.fg_color)
            root.canva_selfi.image = my_icon
            root.label_selfi = Label(root.window, text="Photo personnelle ", font="Arial-BoldMT 13",
                                    bg="#F6F7F9", fg=root.fg_secondary)

            root.entry_selfi= Entry(root.window, textvariable=root.add_selfi, font="Arial-BoldMT 8",  fg="black",
                                    bg="#F6F7F9", width=37, bd=0)
            root.btn_select_selfi = Button(root.window, text="Ouvrir", font="Arial-BoldMT 8 underline",
                                    fg=root.fg_secondary, bg="#F6F7F9", bd=0, command=lambda:open_for_selfi(root,'selfi'))

            root.canva_passport = Label(root.window, image=my_icon, height=65, width=340, bg=root.fg_color)
            root.canva_passport.image = my_icon
            root.label_passport = Label(root.window, text="Passeport ", font="Arial-BoldMT 13",
                                    bg="#F6F7F9", fg=root.fg_secondary)
            root.entry_passport= Entry(root.window, textvariable=root.add_passport, font="Arial-BoldMT 8",  fg="black",
                                    bg="#F6F7F9", width=37, bd=0)
            root.btn_select_passport = Button(root.window, text="Ouvrir", font="Arial-BoldMT 8 underline",
                                    fg=root.fg_secondary, bg="#F6F7F9", bd=0, command=lambda:open_for_selfi(root,'passeport'))

            root.canva_cv = Label(root.window, image=my_icon, height=65, width=340, bg=root.fg_color)
            root.canva_cv.image = my_icon
            root.label_cv = Label(root.window, text="Cv ", font="Arial-BoldMT 13",
                                    bg="#F6F7F9", fg=root.fg_secondary)
            root.entry_cv= Entry(root.window, textvariable=root.add_cv, font="Arial-BoldMT 8",  fg="black",
                                    bg="#F6F7F9", width=37, bd=0)

            root.canva_date = Label(root.window, image=my_icon, height=65, width=340, bg=root.fg_color)
            root.canva_date.image = my_icon
            root.label_date = Label(root.window, text="Date(jj/mm/yyyy) ", font="Arial-BoldMT 13",
                                    bg="#F6F7F9", fg=root.fg_secondary)
            root.entry_date= Entry(root.window, textvariable=root.add_date, font="Arial-BoldMT 8",  fg="black",
                                    bg="#F6F7F9", width=37, bd=0)        


            root.btn_select_cv = Button(root.window, text="Ouvrir", font="Arial-BoldMT 8 underline",
                                    fg=root.fg_secondary, bg="#F6F7F9", bd=0, command=lambda:open_for_selfi(root,'cv'))        
            
            root.data_liste = []
            id_result = get_id_folder_by(root.add_name.get())
            root.btn_save = Button(root.window, text="Enregistré ", font="Arial-BoldMT 13", bg=root.bg_color, fg=root.fg_color,
                                    bd=0,command=lambda:create_data(id_result,root))
            root.combo_avance.current(0)
            root.combo_engagement.current(0)
            root.entry_date.focus()
            # Emplacer les widget dans la fenetre :
            root.canva.place(relx=0.1, rely=0.06)
            root.label.place(relx=0.2, rely=0.1)
            root.label_avance.place(relx=0.12, rely=0.2)
            root.canva_avance.place(relx=0.12, rely=0.2)
            root.combo_avance.place(relx=0.12, rely=0.25)
            root.combo_engagement.place(relx=0.3, rely=0.25)

            root.canva_selfi.place(relx=0.12, rely=0.33)
            root.label_selfi.place(relx=0.12, rely=0.33)
            root.entry_selfi.place(relx=0.12, rely=0.38)
            root.btn_select_selfi.place(relx=0.39, rely=0.42)

            root.canva_passport.place(relx=0.12, rely=0.5)
            root.label_passport.place(relx=0.12, rely=0.5)
            root.entry_passport.place(relx=0.12, rely=0.55)
            root.btn_select_passport.place(relx=0.39, rely=0.59)

            root.canva_cv.place(relx=0.12, rely=0.67)
            root.label_cv.place(relx=0.12, rely=0.67)
            root.entry_cv.place(relx=0.12, rely=0.72)
            root.btn_select_cv.place(relx=0.39, rely=0.76)

            root.canva_date.place(relx=0.12, rely=0.84)
            root.label_date.place(relx=0.12, rely=0.84)
            root.entry_date.place(relx=0.12, rely=0.89)

            root.btn_save.place(relx=0.85, rely=0.93)        
    else:
        messagebox.showerror("Erreur!", "Les informations utilisées ne sont pas complètement incluses")
    return

def clear_widget_folder(root):
    root.canva.destroy()
    root.label.destroy()
    
    root.label_user.destroy()
    root.canva_user.destroy()
    root.entry_user.destroy()

    root.canva_age.destroy()
    root.label_age.destroy()
    root.entry_age.destroy()

    root.canva_cin.destroy()
    root.label_cin.destroy()
    root.entry_cin.destroy()

    root.canva_city.destroy()
    root.label_city.destroy()
    root.entry_city.destroy()

    root.canva_sex.destroy()
    root.label_sex.destroy()
    root.combo_sex.destroy()
    root.combo_diplom.destroy()

    root.canva_educate.destroy()
    root.label_educate.destroy()
    root.entry_educate.destroy()

    root.canva_phone.destroy()
    root.label_phone.destroy()
    root.entry_phone1.destroy()
    root.entry_phone2.destroy()

    root.canva_job.destroy()
    root.label_job.destroy()
    root.entry_job1.destroy()
    root.entry_job2.destroy()
    root.entry_job3.destroy()


    root.canva_pay.destroy()
    root.label_pay.destroy()
    root.entry_pay1.destroy()
    root.entry_pay2.destroy()
    root.entry_pay3.destroy()

    root.btn_next.destroy()
    root.btn_cancel.destroy()
    root.enabel_menu()

    return

def clear_widget_folder_liste(root):
    root.canva.destroy()
    root.label.destroy()
    root.tableau.destroy()
    root.btn_update.destroy()
    root.btn_delet.destroy()
    root.btn_cancel.destroy()
    root.enabel_menu()
    return

def clear_widget_folder_find(root):
    root.find_folder_frame.destroy()
    root.canva.destroy()
    root.label_title_find.destroy()
    root.canva_find_job.destroy()
    root.label_find_job.destroy()
    root.combo_find_job.destroy()
    root.canva_find_avance.destroy()
    root.label_find_avance.destroy()
    root.combo_find_avance.destroy()
    root.combo_find_engagement.destroy()
    root.canva_find_ville_sex.destroy()
    root.label_find_ville_sex.destroy()
    root.combo_find_sex.destroy()
    root.combo_find_ville.destroy()
    root.btn_search_find.destroy()
    root.btn_cancel_find.destroy()
    root.enabel_menu()
    return

def clear_widget_offre(root):
    root.canva.destroy()
    root.label.destroy()
    root.canva_titel.destroy()
    root.label_titel.destroy()
    root.entry_titel.destroy()
    root.canva_date_debut.destroy()
    root.label_date_debut.destroy()
    root.entry_date_debut.destroy()
    root.canva_date_fin.destroy()
    root.label_date_fin.destroy()
    root.entry_date_fin.destroy()
    root.canva_offre_pay.destroy()
    root.label_offre_pay.destroy()
    root.combo_offre_pay.destroy()
    root.btn_offre_save.destroy()
    root.btn_offre_cancel.destroy()
    root.selected_folder_tab.destroy()
    root.canva_offre_job.destroy()
    root.label_offre_job.destroy()
    root.combo_offre_job.destroy()
    root.enabel_menu()
    return

def clear_widget_offre_liste(root):
    try:
        root.tableau_folder.destroy()
    except Exception as e:
        print("[Error] : "+str(e))
    finally:
        root.canva.destroy()
        root.label.destroy()
        root.offre_liste.destroy()
        root.btn_add_new_folder.destroy()
        root.btn_cancel.destroy()
        root.enabel_menu()
    return

def clear_widget_offre_delet(root):
    root.canva.destroy()
    root.label.destroy()
    root.offre_liste.destroy()
    root.btn_cancel.destroy()
    root.enabel_menu()
    return

def update_user(root):
    try:
        root.admin_window.canva_user_name.destroy()
        root.admin_window.label_user_name.destroy()
        root.admin_window.entry_user_name.destroy()
        root.admin_window.canva_user_pswd.destroy()
        root.admin_window.label_user_pswd.destroy()
        root.admin_window.entry_user_pswd.destroy()
        root.admin_window.canva_user_order.destroy()
        root.admin_window.label_user_order.destroy()
        root.admin_window.combo_order.destroy()                                
        root.admin_window.btn_save.destroy()
    except Exception as e:
        print("[ Warrning ] "+str(e))

    # String vars what we need : 
    root.update_user_name = StringVar()
    root.update_user_name.set(str(root.admin_window.admin_selected_values[0]))
    root.update_user_pswd = StringVar()
    root.update_user_pswd.set(str(root.admin_window.admin_selected_values[1]))
    # disabled btn : 
    root.admin_window.btn_update['state'] = "disabled"
    my_image = Image.open('Images/TextBox_Bg.png')
    my_icon = ImageTk.PhotoImage(my_image)
    # User Name Update Outils :
    
    root.admin_window.canva_user_name = Label(root.admin_window, image=my_icon, height=65, width=340, bg=root.fg_color)
    root.admin_window.canva_user_name.image = my_icon
    root.admin_window.label_user_name = Label(root.admin_window, text="Nom Utilisateur : ", font="Arial-BoldMT 13",
                                bg="#F6F7F9", fg=root.fg_secondary)
    root.admin_window.entry_user_name = Entry(root.admin_window, textvariable=root.update_user_name, font="Arial-BoldMT 13",  fg="black",
                                bg="#F6F7F9", width=37, bd=0)
    # User Passsword Update Outils :
    root.admin_window.canva_user_pswd = Label(root.admin_window, image=my_icon, height=65, width=340, bg=root.fg_color)
    root.admin_window.canva_user_pswd.image = my_icon
    root.admin_window.label_user_pswd = Label(root.admin_window, text="Mot De pass Utilisateur : ", font="Arial-BoldMT 13",
                                bg="#F6F7F9", fg=root.fg_secondary)
    root.admin_window.entry_user_pswd = Entry(root.admin_window, textvariable=root.update_user_pswd, font="Arial-BoldMT 13",  fg="black",
                                bg="#F6F7F9", width=37, bd=0)
    # User permission : 
    root.admin_window.canva_user_order = Label(root.admin_window, image=my_icon, height=65, width=340, bg=root.fg_color)
    root.admin_window.canva_user_order.image = my_icon
    root.admin_window.label_user_order = Label(root.admin_window, text="Mode d acce utilisateur : ", font="Arial-BoldMT 13",
                                bg="#F6F7F9", fg=root.fg_secondary)
    root.admin_window.combo_order = ttk.Combobox(root.admin_window, value=['Private','Public'], state='readonly', width=30, height=2)
    user_id = get_user_id_by_name(root.admin_window.admin_selected_values[0])
    # btn save change : 
    root.admin_window.btn_save = Button(root.admin_window, text="Enregistré", font="Arial-BoldMT 9 underline",
        bg=root.fg_secondary, fg=root.fg_color, bd=0, command=lambda:update_user_by_id(user_id,root))     
    root.admin_window.combo_order.current(0)
    root.admin_window.entry_user_name.focus()
    # emplacer les elements dans la fenetre : 
    root.admin_window.canva_user_name.place(relx=0.1, rely=0.6)
    root.admin_window.label_user_name.place(relx=0.1, rely=0.62)
    root.admin_window.entry_user_name.place(relx=0.1, rely=0.67)

    root.admin_window.canva_user_pswd.place(relx=0.5, rely=0.6)
    root.admin_window.label_user_pswd.place(relx=0.5, rely=0.62)
    root.admin_window.entry_user_pswd.place(relx=0.5, rely=0.67)

    root.admin_window.canva_user_order.place(relx=0.1, rely=0.8)
    root.admin_window.label_user_order.place(relx=0.1, rely=0.82)
    root.admin_window.combo_order.place(relx=0.1, rely=0.87)    

    root.admin_window.btn_save.place(relx=0.7, rely=0.87)
    return

def Liste_folder(root):
    root.disabled_menu()
    my_image = Image.open('Images/icons8-liste-64.png')
    my_icon = ImageTk.PhotoImage(my_image)
    root.canva = Label(root.window, image=my_icon, height=70, width=70, bg=root.fg_color)
    root.canva.image = my_icon
    root.label = Label(root.window, text="Liste Dossiers :" , font="Arial-BoldMT 20 underline",
            bg=root.fg_color, fg=root.fg_secondary, bd=0)
    tete_colone = ('Nom', 'Age', 'Cin', 'Ville', 'Niveau d etude', 'Diplôme', 'Occupation-1', 'Occupation-2',
        'Occupation-3', 'N° Télé 1', 'N° Télé 2')
    root.tableau = ttk.Treeview(root.window, height=10, show="headings", column=tete_colone)
    # ------> Creation des colones :
    root.tableau.column("Nom", width="120", anchor=CENTER)
    root.tableau.column("Age", width="30", anchor=CENTER)
    root.tableau.column("Cin", width="100", anchor=CENTER)
    root.tableau.column("Ville", width="120", anchor=CENTER)
    root.tableau.column("Niveau d etude", width=120, anchor=CENTER)
    root.tableau.column("Diplôme", width=50, anchor=CENTER)
    root.tableau.column("Occupation-1", width=100, anchor=CENTER)
    root.tableau.column("Occupation-2", width=100, anchor=CENTER)
    root.tableau.column("Occupation-3", width=100, anchor=CENTER)
    root.tableau.column("N° Télé 1", width=100, anchor=CENTER)
    root.tableau.column("N° Télé 2", width=100, anchor=CENTER)
    # ----> Ajoute des entete au colones du tableau :
    root.tableau.heading("Nom", text="Nom")
    root.tableau.heading("Age", text="Age")
    root.tableau.heading("Cin", text="Cin")
    root.tableau.heading("Ville", text="Ville")
    root.tableau.heading("Niveau d etude", text="Niveau d etude")
    root.tableau.heading("Diplôme", text="Diplôme")
    root.tableau.heading("Occupation-1", text="Occupation-1")
    root.tableau.heading("Occupation-2", text="Occupation-2")
    root.tableau.heading("Occupation-3", text="Occupation-3")
    root.tableau.heading("N° Télé 1", text="N° Télé 1")
    root.tableau.heading("N° Télé 2", text="N° Télé 2")
    liste = get_folder_liste()
    for element in liste:
        root.tableau.insert('',END, values=(str(element[1]), str(element[2]),str(element[3]),str(element[4]),
        str(element[6]), str(element[7]), str(element[8]),str(element[9]),str(element[10]),str(element[14]),str(element[15])))
    # Les buttons des services : 
    
    root.btn_update = Button(root.window, text="Modifié" , font="Arial-BoldMT 9", bd=0, bg=root.secondary_color,
        fg=root.fg_color, state="disabled", command=lambda:get_selected_to_update(root))

    root.btn_delet = Button(root.window, text="Supprimer" , font="Arial-BoldMT 9", bd=0, bg=root.bg_color,
        fg=root.fg_color, state="disabled", command=lambda:delet_folder(root,get_id_folder_by(root.selected_values[0])))
    root.tableau.bind("<Double-1>", lambda event: enabel_button(key=root))
    
    root.btn_cancel = Button(root.window, text="Annuler" , font="Arial-BoldMT 9", bd=0, bg=root.fg_secondary,
        fg=root.fg_color, command = lambda:clear_widget_folder_liste(root))

    # emplacer les widget dans fenetre : 
    root.canva.place(relx=0.1, rely=0.06)
    root.label.place(relx=0.2, rely=0.1)
    root.tableau.place(relx=0.01, rely=0.2)
    root.btn_cancel.place(relx=0.9, rely=0.65)
    root.btn_delet.place(relx=0.83, rely=0.65)
    root.btn_update.place(relx=0.78, rely=0.65)
    return

def open_exploral(file_type,id_folder):
    file_path = ''
    if file_type == "Passport":
        folder = get_data_folder_by_id(id_folder)
        file_path = folder[4]
    if file_type =="selfi":
        folder = get_data_folder_by_id(id_folder)
        file_path = folder[5]
    if file_type == "cv":
        folder = get_data_folder_by_id(id_folder)
        file_path = folder[6]
    if file_type == "vissa":
        folder = get_data_A(id_folder)
        if not len(folder) == 0: 
            file_path = folder[1]
    if file_type == "billet":
        folder = get_data_A(id_folder)
        if not len(folder) == 0:
            file_path = folder[2]
    try:
        print(file_path)
        if file_path != '':
            arr_path = file_path.split('/')
            arr_path = arr_path[:-1]
            path_result = arr_path[0]+'/'
            arr_path.pop(0)
            for e in arr_path:
                path_result = path_result+str(e)+"/"
            path=os.path.realpath(path_result)
            os.startfile(path)
    except Exception as e:
        print("[Error] : "+str(e))
        messagebox.showerror("Erreur! ", "Impossible d'ouvrir l'emplacement du fichier ")
    return

def get_btn_see_data_folder(key):
    selected = key.table_results.focus()
    key.selected_folder = key.table_results.item(selected, 'values')
    print(key.selected_folder)
    id = get_id_folder_by(key.selected_folder[0])
    try:
        key.bnt_see_passport.destroy()
        key.btn_see_selfi.destroy()
        key.btn_see_cv.destroy()
        key.btn_see_visa.destroy()
        key.btn_see_billet.destroy()
    except Exception as e:
        print("[Error] : "+str(e))
    key.bnt_see_passport = Button(key.find_folder_frame, text="Passport", font="Arial-BoldMT 9 underline",
        bg="#F6F7F9", fg=key.fg_secondary, bd=0, command=lambda:open_exploral("Passport",id))
    key.btn_see_selfi = Button(key.find_folder_frame, text=" Photo ", font="Arial-BoldMT 9 underline",
        bg="#F6F7F9", fg=key.fg_secondary, bd=0, command=lambda:open_exploral("selfi",id))
    key.btn_see_cv = Button(key.find_folder_frame, text="  CV  ", font="Arial-BoldMT 9 underline",
        bg="#F6F7F9", fg=key.fg_secondary, bd=0, command=lambda:open_exploral("cv",id))
    key.btn_see_visa = Button(key.find_folder_frame, text=" Visa ", font="Arial-BoldMT 9 underline",
        bg="#F6F7F9", fg=key.fg_secondary, bd=0, command=lambda:open_exploral("vissa",id))
    key.btn_see_billet = Button(key.find_folder_frame, text="Billet", font="Arial-BoldMT 9 underline",
        bg="#F6F7F9", fg=key.fg_secondary, bd=0, command=lambda:open_exploral("billet",id))

    # emplacer les bouttons dans la fenetre :
    key.bnt_see_passport.place(relx=0.1, rely=0.53)
    key.btn_see_selfi.place(relx=0.2, rely=0.53)
    key.btn_see_cv.place(relx=0.3, rely=0.53)
    key.btn_see_visa.place(relx=0.4, rely=0.53)
    key.btn_see_billet.place(relx=0.5, rely=0.53)
    return

def find_folder_by(root):
    try:
        root.label_titel_resultat.destroy()
        root.canva_find.destroy()
        root.table_results.destroy()
    except Exception as e:
        print("[Error] : "+str(e))
    # appelle a la fonction du recherche :
    liste_resultat = find_folders_by(root.combo_find_job.get(),
                                root.combo_find_sex.get(),
                                root.combo_find_ville.get(),
                                root.combo_find_avance.get(),
                                root.combo_find_engagement.get()
                                )
    if len(liste_resultat) > 0:
        # teste sur les resultat de recerche : 
        my_image = Image.open('Images/icons8-research-58.png')
        my_icon = ImageTk.PhotoImage(my_image)
        root.canva_find = Label(root.find_folder_frame, image=my_icon, height=58, width=58, bg="#F6F7F9")
        root.canva_find.image = my_icon
        root.label_titel_resultat = Label(root.find_folder_frame,text="Resultats : ", 
            font="Arial-BoldMT 20 underline", bg="#F6F7F9", fg=root.fg_secondary, bd=0)
        tete_colone = ('Dossier', 'Cin', 'Télé1', 'Télé2')
        root.table_results = ttk.Treeview(root.find_folder_frame,height=12, show="headings", column=tete_colone)
        root.table_results.column("Dossier", width="200", anchor=CENTER)    
        root.table_results.column("Cin", width="100", anchor=CENTER)
        root.table_results.column("Télé1", width="150", anchor=CENTER)
        root.table_results.column("Télé2", width="150", anchor=CENTER)
        root.table_results.heading("Dossier", text="Dossier")
        root.table_results.heading("Cin", text="Cin")
        root.table_results.heading("Télé1", text="Télé1")
        root.table_results.heading("Télé2", text="Télé2")
        # insertion des resultats dans le tableau :
        for element in liste_resultat:
            root.table_results.insert('',END ,values=(element[1], element[3], element[14], element[15]))
        # ajouté evenement au tableau : 
        root.table_results.bind("<Double-1>", lambda event:get_btn_see_data_folder(key=root))
        # emplacer les elements dans le frame :
        root.canva_find.place(relx=0.1, rely=0.035)
        root.label_titel_resultat.place(relx=0.2, rely=0.07)
        root.table_results.place(relx=0.05, rely=0.13)
    else:
        messagebox.showinfo("Info !", "Aucune Resultat Disponible")
    return

def Find_folder(root):
    root.disabled_menu()
    root.folder_job = StringVar()
    root.find_folder_frame = Frame(root.window, bg="#F6F7F9", width=715, height=700, bd=0)
    # titel and canva : 
    my_image = Image.open('Images/icons8-search-file-content-and-find-results-on-system-25.png')
    my_icon = ImageTk.PhotoImage(my_image)
    root.canva = Label(root.window, image=my_icon, height=25, width=25, bg=root.fg_color)
    root.canva.image = my_icon    
    root.label_title_find = Label(root.window, text="Chercher ",
                                font="Arial-BoldMT 15", bg=root.fg_color, 
                                fg=root.fg_secondary, bd=0)
    # Outils :

    my_image = Image.open('Images/TextBox_Bg.png')
    my_icon = ImageTk.PhotoImage(my_image)
    root.canva_find_job = Label(root.window, image=my_icon, height=65, width=340, bg=root.fg_color)
    root.canva_find_job.image = my_icon
    root.label_find_job = Label(root.window, text="Occupation  ", font="Arial-BoldMT 13",
                                bg="#F6F7F9", fg=root.fg_secondary)
    # Job --------------------------------------------------------
    liste_job =[] 
    for element in get_job_liste():
        for seconde in element:
            liste_job.append(str(seconde))
    root.combo_find_job = ttk.Combobox(root.window,value=liste_job, state='readonly', width=40, height=1)
    if not len(liste_job)==0:
        root.combo_find_job.current(0)
    # avance & Engagement ------------------------------------------
    root.canva_find_avance = Label(root.window, image=my_icon, height=65, width=340, bg=root.fg_color)
    root.canva_find_avance.image = my_icon
    root.label_find_avance = Label(root.window, text="Avance & Engagement ", font="Arial-BoldMT 13",
                                    bg="#F6F7F9", fg=root.fg_secondary)
    root.combo_find_avance = ttk.Combobox(root.window,value=['Oui', 'Non'], state='readonly', width=20, height=0)
    root.combo_find_engagement = ttk.Combobox(root.window,value=['Oui', 'Non'], state='readonly', width=20, height=0)
    root.combo_find_avance.current(0)
    root.combo_find_engagement.current(0)

    # sex & ville ------------------------------------------------------------------------------------ 
    root.canva_find_ville_sex = Label(root.window, image=my_icon, height=65, width=340, bg=root.fg_color)
    root.canva_find_ville_sex.image = my_icon
    root.label_find_ville_sex = Label(root.window, text="Sex & Ville ", font="Arial-BoldMT 13",
                                    bg="#F6F7F9", fg=root.fg_secondary)
    liste_ville = []
    for element in get_city_liste():
        liste_ville.append(str(element[0]))
    root.combo_find_sex = ttk.Combobox(root.window,value=['Homme', 'Femme'], state='readonly', width=20, height=0)
    root.combo_find_ville = ttk.Combobox(root.window,value=liste_ville, state='readonly', width=20, height=0)
    root.combo_find_sex.current(0)
    if not len(liste_ville)==0:
        root.combo_find_ville.current(0)    
    # Btn cancel ans search ---------------------------------------------------------------------------------------
    root.btn_cancel_find = Button(root.window, text="Annuler", font="Arial-BoldMT 9 underline",
        bg=root.fg_secondary, fg=root.fg_color, bd=0, command=lambda:clear_widget_folder_find(root))
    root.btn_search_find = Button(root.window, text="Chercher", font="Arial-BoldMT 9 underline",
        bg=root.bg_color, fg=root.fg_color, bd=0, command=lambda:find_folder_by(root))
    # emplacer les widget en fenetre : 
    root.find_folder_frame.place(relx=0.35, rely=0.0)
    root.canva.place(relx=0.02, rely=0.06)
    root.label_title_find.place(relx=0.06, rely=0.07)

    root.canva_find_job.place(relx=0.0, rely=0.2)
    root.label_find_job.place(relx=0.0, rely=0.21)
    root.combo_find_job.place(relx=0.0, rely=0.25)

    root.canva_find_avance.place(relx=0.0, rely=0.43)
    root.label_find_avance.place(relx=0.0, rely=0.44)
    root.combo_find_avance.place(relx=0.0, rely=0.48)
    root.combo_find_engagement.place(relx=0.15, rely=0.48)

    root.canva_find_ville_sex.place(relx=0.0, rely=0.66)
    root.label_find_ville_sex.place(relx=0.0, rely=0.67)
    root.combo_find_sex.place(relx=0.0, rely=0.71)
    root.combo_find_ville.place(relx=0.15, rely=0.71)

    root.btn_search_find.place(relx=0.17, rely=0.95)
    root.btn_cancel_find.place(relx=0.24, rely=0.95)
    return

def Add_Offre(root):
    root.disabled_menu()
    root.add_offre_titel = StringVar()
    root.add_debut_date_offre = StringVar()
    root.add_fin_date_offre = StringVar()
    my_image = Image.open('Images/icons8-offre-prix-chaud-64.png')
    my_icon = ImageTk.PhotoImage(my_image)
    root.canva = Label(root.window, image=my_icon, height=70, width=70, bg=root.fg_color)
    root.canva.image = my_icon
    root.label = Label(root.window, text="Ajouter Offre :" , font="Arial-BoldMT 20 underline",
            bg=root.fg_color, fg=root.fg_secondary, bd=0)
    
    my_image = Image.open('Images/TextBox_Bg.png')
    my_icon = ImageTk.PhotoImage(my_image)

    # Titre Offre :
    root.canva_titel = Label(root.window, image=my_icon, height=65, width=340, bg=root.fg_color)
    root.canva_titel.image = my_icon
    root.label_titel = Label(root.window, text="Titre : ", font="Arial-BoldMT 13",
                                bg="#F6F7F9", fg=root.fg_secondary)
    root.entry_titel = Entry(root.window, textvariable=root.add_offre_titel, font="Arial-BoldMT 13",  fg="black",
                                bg="#F6F7F9", width=37, bd=0)
    # Date De debut du l offre : 
    root.canva_date_debut = Label(root.window, image=my_icon, height=65, width=340, bg=root.fg_color)
    root.canva_date_debut.image = my_icon
    root.label_date_debut = Label(root.window, text="Date De Lancement  : ", font="Arial-BoldMT 13",
                                bg="#F6F7F9", fg=root.fg_secondary)
    root.entry_date_debut = Entry(root.window, textvariable=root.add_debut_date_offre, font="Arial-BoldMT 13",  fg="black",
                                bg="#F6F7F9", width=37, bd=0)
    # Date De Fin : 
    root.canva_date_fin = Label(root.window, image=my_icon, height=65, width=340, bg=root.fg_color)
    root.canva_date_fin.image = my_icon
    root.label_date_fin = Label(root.window, text="Date D'expiration  : ", font="Arial-BoldMT 13",
                                bg="#F6F7F9", fg=root.fg_secondary)
    root.entry_date_fin = Entry(root.window, textvariable=root.add_fin_date_offre, font="Arial-BoldMT 13",  fg="black",
                                bg="#F6F7F9", width=37, bd=0)
    # Pay de l offre : 
    root.canva_offre_pay = Label(root.window, image=my_icon, height=65, width=340, bg=root.fg_color)
    root.canva_offre_pay.image = my_icon
    root.label_offre_pay = Label(root.window, text="Pays  : ", font="Arial-BoldMT 13",
                                bg="#F6F7F9", fg=root.fg_secondary)
    pays =["عمان" , "سلطنة عمان ", " الامارات" , "السعودية" , " البحرين" , "قطر" , "الكويت"]
    root.combo_offre_pay = ttk.Combobox(root.window,value=pays, state='readonly', width=50, height=3)
    
    # job d offre : 
    root.canva_offre_job = Label(root.window, image=my_icon, height=65, width=340, bg=root.fg_color)
    root.canva_offre_job.image = my_icon
    root.label_offre_job = Label(root.window, text=" Occupation : ", font="Arial-BoldMT 13",
                                bg="#F6F7F9", fg=root.fg_secondary)
    jobs = []
    for element in get_job_liste():
        for job in element:
            jobs.append(job)
    root.combo_offre_job = ttk.Combobox(root.window,value=jobs, state='readonly', width=50, height=3)
    # boutton :

    root.btn_offre_save = Button(root.window, text="Enregistré", font="Arial-BoldMT 10 underline",
        bg=root.fg_secondary, fg=root.fg_color, bd=0, command=lambda:create_offre(root))
    root.btn_offre_cancel = Button(root.window, text="Annuler", font="Arial-BoldMT 10 underline",
        bg=root.bg_color, fg=root.fg_color, bd=0, command=lambda:clear_widget_offre(root))

    root.combo_offre_pay.current(0)
    root.combo_offre_job.current(0)
    root.entry_titel.focus()

    # Part II : ajouté le tableau du selection des dossier assosiée a cette offre : 
    tete_colone = ('Nom', 'Cin', 'Ville')
    root.selected_folder_tab = ttk.Treeview(root.window, height=10, show="headings", column=tete_colone)
    root.selected_folder_tab.column("Nom", width="200", anchor=CENTER)
    root.selected_folder_tab.column("Cin", width="150", anchor=CENTER)
    root.selected_folder_tab.column("Ville", width="200", anchor=CENTER)

    root.selected_folder_tab.heading("Nom", text="Nom")
    root.selected_folder_tab.heading("Cin", text="Cin")
    root.selected_folder_tab.heading("Ville", text="Ville")
    
    # emplacer les widget dans la fenetre : 
    root.selected_folder_tab.bind("<Double-1>", lambda event:enabel_add_offre(key=root))
    root.canva.place(relx=0.1, rely=0.06)
    root.label.place(relx=0.2, rely=0.1)

    root.selected_folder_tab.place(relx=0.48, rely=0.2)
    root.canva_titel.place(relx=0.1, rely=0.2)
    root.label_titel.place(relx=0.1, rely=0.21)
    root.entry_titel.place(relx=0.1, rely=0.25)

    root.canva_date_debut.place(relx=0.1, rely=0.35)
    root.label_date_debut.place(relx=0.1, rely=0.36)
    root.entry_date_debut.place(relx=0.1, rely=0.4)

    root.canva_date_fin.place(relx=0.1, rely=0.5)
    root.label_date_fin.place(relx=0.1, rely=0.51)
    root.entry_date_fin.place(relx=0.1, rely=0.55)

    root.canva_offre_pay.place(relx=0.1, rely=0.65)
    root.label_offre_pay.place(relx=0.1, rely=0.66)
    root.combo_offre_pay.place(relx=0.1, rely=0.71)

    root.canva_offre_job.place(relx=0.1, rely=0.81)
    root.label_offre_job.place(relx=0.1, rely=0.82)
    root.combo_offre_job.place(relx=0.1, rely=0.87)

    root.btn_offre_save.place(relx=0.29, rely=0.95)
    root.btn_offre_cancel.place(relx=0.37, rely=0.95)
    
    return

def Liste_offre(root):
    root.disabled_menu()
    my_image = Image.open('Images/icons8-liste-64.png')
    my_icon = ImageTk.PhotoImage(my_image)
    root.canva = Label(root.window, image=my_icon, height=70, width=70, bg=root.fg_color)
    root.canva.image = my_icon
    root.label = Label(root.window, text="Liste Offre :" , font="Arial-BoldMT 20 underline",
            bg=root.fg_color, fg=root.fg_secondary, bd=0)
    # ajouté tableaux des offres :
    tete_colone = ("Titre", "Date")
    root.offre_liste = ttk.Treeview(root.window, height=18, show="headings", column=tete_colone)
    root.offre_liste.column("Titre", width="200", anchor=CENTER)
    root.offre_liste.column("Date", width="200", anchor=CENTER)
    root.offre_liste.heading("Titre", text="Titre")
    root.offre_liste.heading("Date", text="Date")
    root.liste_offre = get_offre_liste()
    for element in root.liste_offre:
        root.offre_liste.insert('', END, values=(str(element[1]), str(element[2])))
    root.offre_liste.bind("<Double-1>", lambda event:enabel_add_folder_to_offre(key=root))
    # ajouté des bouttons de configuration 
    root.btn_add_new_folder = Button(root.window, text="Ajouter Un Dossier a cette offre ", fon="Arial-BoldMT 9 underline",
        bg=root.bg_color, fg=root.fg_color, bd=0, state="disabled", command=lambda:select_folder_to_add(root))
    root.btn_cancel = Button(root.window, text="Annuler", fon="Arial-BoldMT 9 underline",
        bg=root.fg_secondary, fg=root.fg_color, bd=0, command=lambda:clear_widget_offre_liste(root))
    # emplacer les widgets dans la fentre :
    root.canva.place(relx=0.1, rely=0.06)
    root.label.place(relx=0.2, rely=0.1)
    root.offre_liste.place(relx=0.1, rely=0.2)
    root.btn_add_new_folder.place(relx=0.25, rely=0.94)
    root.btn_cancel.place(relx=0.42, rely=0.94)
    return

def delet_offre(root):
    if root.connexion[3]=="Private":
        root.disabled_menu()
        my_image = Image.open('Images/icons8-supprimer-la-corbeille-50.png')
        my_icon = ImageTk.PhotoImage(my_image)
        root.canva = Label(root.window, image=my_icon, height=50, width=50, bg=root.fg_color)
        root.canva.image = my_icon
        root.label = Label(root.window, text="Supprimer Offre :" , font="Arial-BoldMT 20 underline",
                bg=root.fg_color, fg=root.fg_secondary, bd=0)
        # add a table of offres : 
        tete_colone = ("Titre", "Date")
        root.offre_liste = ttk.Treeview(root.window, height=18, show="headings", column=tete_colone)
        root.offre_liste.column("Titre", width="200", anchor=CENTER)
        root.offre_liste.column("Date", width="200", anchor=CENTER)
        root.offre_liste.heading("Titre", text="Titre")
        root.offre_liste.heading("Date", text="Date")
        root.liste_offre = get_offre_liste()
        for element in root.liste_offre:
            root.offre_liste.insert('', END, values=(str(element[1]), str(element[2])))
        root.offre_liste.bind("<Double-1>",  lambda event:selected_to_delet(key=root))
        # button cancel : 
        root.btn_cancel = Button(root.window, text="Annuler", fon="Arial-BoldMT 9 underline",
            bg=root.fg_secondary, fg=root.fg_color, bd=0, command=lambda:clear_widget_offre_delet(root))

        # emplacé dans la fenetre : 
        root.canva.place(relx=0.1, rely=0.06)
        root.label.place(relx=0.2, rely=0.1)
        root.offre_liste.place(relx=0.2, rely=0.2)
        root.btn_cancel.place(relx=0.52, rely=0.94)
    else:
        messagebox.showerror("Probleme de vie privé ","Le compte connecté n est pas definie comme un super utilisateur")
    return

def see_users_by_admin(root):
    # create a seconde windwo : 
    if root.connexion[3]=="Private":
        root.admin_window = Toplevel(bg=root.fg_color, bd=0)
        root.admin_window.geometry("900x550")
        root.admin_window.resizable(0,0)
        root.admin_window.iconbitmap("Images/logo2.ico")
        root.admin_window.title(' Votre Espace utilisateur ')
        my_image = Image.open('Images/icons8-users.png')
        my_icon = ImageTk.PhotoImage(my_image)
        root.admin_window.canva = Label(root.admin_window, image=my_icon, height=65, width=65, bg=root.fg_color)
        root.admin_window.canva.image = my_icon
        root.admin_window.label_titre = Label(root.admin_window, text="Espace Utilisateur ",
            font="Arial-BoldMT 20 underline", bg=root.fg_color, fg=root.fg_secondary, bd=0)
        # listé les utilisateur : 
        tete_colone = ('Nom Utilisateur', 'Mot De Pass', 'Dernier Session', 'Type Du Compte')
        root.admin_window.liste_user = ttk.Treeview(root.admin_window, height=10, show="headings", column=tete_colone)
        root.admin_window.liste_user.column("Nom Utilisateur", width="200", anchor=CENTER)
        root.admin_window.liste_user.column("Mot De Pass", width="200", anchor=CENTER)
        root.admin_window.liste_user.column("Dernier Session", width="200", anchor=CENTER)
        root.admin_window.liste_user.column("Type Du Compte", width="200", anchor=CENTER)
        root.admin_window.liste_user.heading("Nom Utilisateur", text="Nom Utilisateur")
        root.admin_window.liste_user.heading("Mot De Pass", text="Mot De Pass")
        root.admin_window.liste_user.heading("Dernier Session", text="Dernier Session")
        root.admin_window.liste_user.heading("Type Du Compte", text="Type Du Compte")
        for user in get_users():
            root.admin_window.liste_user.insert('', END, values=(str(user[1]), str(user[2]), str(user[4]), str(user[3])))
        # btn outils : 
        root.admin_window.btn_update = Button(root.admin_window, text="Modifié", fon="Arial-BoldMT 9 underline",
            bg=root.bg_color, fg=root.fg_color, bd=0, state="disabled", command=lambda:update_user(root))
        root.admin_window.liste_user.bind("<Double-1>", lambda event: enabel_button_admin(key=root))
        #emplacé les element dans la fenetre :
        root.admin_window.canva.place(relx=0.1, rely=0.0)
        root.admin_window.label_titre.place(relx=0.21, rely=0.04)
        root.admin_window.liste_user.place(relx=0.05, rely=0.13)
        root.admin_window.btn_update.place(relx=0.87, rely=0.55)
    else:
        messagebox.showerror("Probleme de vie privé ","Le compte connecté n est pas definie comme un super utilisateur")
    return

def enabel_button_delet_admin(key):
    key.admin_space.btn_delet['state'] = "normal"
    selected = key.admin_space.tab_users.focus()
    key.admin_space.selcted_users_to_delet = key.admin_space.tab_users.item(selected, 'values')    
    print(key.admin_space.selcted_users_to_delet)
    return

def Delet_user(root):
    try:
        root.admin_space.tab_users.destroy()
        root.admin_space.canva_user_name.destroy()
        root.admin_space.label_user_name.destroy()
        root.admin_space.entry_user_name.destroy()
        root.admin_space.canva_user_password.destroy()
        root.admin_space.label_user_password.destroy()
        root.admin_space.entry_user_password.destroy()
        root.admin_space.canva_user_order.destroy()
        root.admin_space.label_user_order.destroy()
        root.admin_space.combo_order.destroy()
        root.admin_space.btn_save_new.destroy()
        root.admin_space.btn_delet.destroy()                                            
    except Exception as e:
        print("[Error] "+str(e))
    # Creation du tableau des etulisateurs :

    tete_colone = ('Id', 'Nom Utilisateur', 'Type')
    root.admin_space.tab_users = ttk.Treeview(root.admin_space, height=10, show="headings", column=tete_colone)
    root.admin_space.tab_users.column("Id", width="50", anchor=CENTER)
    root.admin_space.tab_users.column("Nom Utilisateur", width="200", anchor=CENTER)
    root.admin_space.tab_users.column("Type", width="200", anchor=CENTER)
    root.admin_space.tab_users.heading("Id", text="Id")
    root.admin_space.tab_users.heading("Nom Utilisateur", text="Nom Utilisateur")
    root.admin_space.tab_users.heading("Type", text="Type")
    for user in get_users():
            root.admin_space.tab_users.insert('', END, values=(str(user[0]), str(user[1]), str(user[3])))
    root.admin_space.btn_delet = Button(root.admin_space, text="Supprimer", font="Arial-BoldMT 8 underline",
        bg=root.fg_secondary, fg=root.fg_color, bd=0, state="disabled", command=lambda: delet_user_by_admin(root))
    root.admin_space.tab_users.bind("<Double-1>", lambda event: enabel_button_delet_admin(key=root))
    # emplacer dans la fenetre : 
    root.admin_space.tab_users.place(relx=0.4, rely=0.1)
    root.admin_space.btn_delet.place(relx=0.84, rely=0.62)
    return

def Add_New_User(root):
    try:
        root.admin_space.tab_users.destroy()
        root.admin_space.canva_user_name.destroy()
        root.admin_space.label_user_name.destroy()
        root.admin_space.entry_user_name.destroy()
        root.admin_space.canva_user_password.destroy()
        root.admin_space.label_user_password.destroy()
        root.admin_space.entry_user_password.destroy()
        root.admin_space.canva_user_order.destroy()
        root.admin_space.label_user_order.destroy()
        root.admin_space.combo_order.destroy()
        root.admin_space.btn_save_new.destroy()
        root.admin_space.btn_delet.destroy()                                              
    except Exception as e:
        print("[Error] "+str(e))
    root.add_user_name = StringVar()
    root.add_user_pswd = StringVar()
    my_image = Image.open('Images/TextBox_Bg.png')
    my_icon = ImageTk.PhotoImage(my_image)
    root.admin_space.canva_user_name = Label(root.admin_space, image=my_icon, height=65, width=340, bg=root.fg_color)
    root.admin_space.canva_user_name.image = my_icon
    root.admin_space.label_user_name = Label(root.admin_space, text="Nom Utilisateur : ", font="Arial-BoldMT 13",
                                bg="#F6F7F9", fg=root.fg_secondary)
    root.admin_space.entry_user_name = Entry(root.admin_space, textvariable=root.add_user_name, font="Arial-BoldMT 13",  fg="black",
                                bg="#F6F7F9", width=37, bd=0)

    root.admin_space.canva_user_password = Label(root.admin_space, image=my_icon, height=65, width=340, bg=root.fg_color)
    root.admin_space.canva_user_password.image = my_icon
    root.admin_space.label_user_password = Label(root.admin_space, text="Mot de Pass  Utilisateur : ", font="Arial-BoldMT 13",
                                bg="#F6F7F9", fg=root.fg_secondary)
    root.admin_space.entry_user_password = Entry(root.admin_space, textvariable=root.add_user_pswd, font="Arial-BoldMT 13",  fg="black",
                                bg="#F6F7F9", width=37, bd=0)

    root.admin_space.canva_user_order = Label(root.admin_space, image=my_icon, height=65, width=340, bg=root.fg_color)
    root.admin_space.canva_user_order.image = my_icon
    root.admin_space.label_user_order = Label(root.admin_space, text="Mode d acce utilisateur : ", font="Arial-BoldMT 13",
                                bg="#F6F7F9", fg=root.fg_secondary)
    root.admin_space.combo_order = ttk.Combobox(root.admin_space, value=['Private','Public'], state='readonly', width=30, height=2)

    root.admin_space.btn_save_new = Button(root.admin_space, text="Enregistré", font="Arial-BoldMT 8 underline",
        bg=root.fg_secondary, fg=root.fg_color, bd=0, command=lambda:create_user(root))    

    root.admin_space.combo_order.current(1)
    root.admin_space.entry_user_name.focus()
    # emplacé les elements dans la fenetre : 
    root.admin_space.canva_user_name.place(relx=0.4, rely=0.1)
    root.admin_space.label_user_name.place(relx=0.4, rely=0.11)
    root.admin_space.entry_user_name.place(relx=0.4, rely=0.15)

    root.admin_space.canva_user_password.place(relx=0.4, rely=0.25)
    root.admin_space.label_user_password.place(relx=0.4, rely=0.26)
    root.admin_space.entry_user_password.place(relx=0.4, rely=0.3)

    root.admin_space.canva_user_order.place(relx=0.4, rely=0.4)
    root.admin_space.label_user_order.place(relx=0.4, rely=0.41)
    root.admin_space.combo_order.place(relx=0.4, rely=0.465)    
    root.admin_space.btn_save_new.place(relx=0.73, rely=0.57)
    return

def see_admin_space(root):
    if root.connexion[3]=="Private":
        root.admin_space = Toplevel(bg=root.fg_color, bd=0)
        root.admin_space.geometry("900x450")
        root.admin_space.resizable(0,0)
        root.admin_space.iconbitmap("Images/logo2.ico")
        root.admin_space.title(' Votre Espace administrateur ')
        root.admin_space.frame_side = Frame(root.admin_space, bg="#F6F7F9", height=550, width=270, bd=0)
        my_image = Image.open('Images/icons8-microsoft-admin-50.png')
        my_icon = ImageTk.PhotoImage(my_image)
        root.admin_space.frame_side.canva_titel = Label(root.admin_space.frame_side, image=my_icon, height=50, width=50, bg="#F6F7F9")
        root.admin_space.frame_side.canva_titel.image = my_icon
        root.admin_space.frame_side.label_titel = Label(root.admin_space.frame_side, text="Administration", font="Arial-BoldMT 13 underline",
            bg="#F6F7F9", fg=root.fg_secondary, bd=0)
        # Add btn for add new user : 
        my_image = Image.open('Images/icons8-ajouter-administrateur-35.png')
        my_icon = ImageTk.PhotoImage(my_image)
        root.admin_space.frame_side.canva_add_user = Label(root.admin_space.frame_side, image=my_icon, height=35, width=35, bg="#F6F7F9")
        root.admin_space.frame_side.canva_add_user.image = my_icon
        root.admin_space.frame_side.label_add_user = Button(root.admin_space.frame_side, text="Ajouté Utilisateur ",
            font="Arial-BoldMT 13 underline",bg="#F6F7F9", fg=root.fg_secondary, bd=0, command=lambda:Add_New_User(root))
        
        # add btn for delet user : 
        my_image = Image.open("Images/icons8-retirer-administrateur-37.png")
        my_icon = ImageTk.PhotoImage(my_image)
        root.admin_space.frame_side.canva_delet_user = Label(root.admin_space.frame_side, image=my_icon, height=35, width=35, bg="#F6F7F9")
        root.admin_space.frame_side.canva_delet_user.image = my_icon
        root.admin_space.frame_side.label_delet_user = Button(root.admin_space.frame_side, text="Supprimer Utilisateur ",
            font="Arial-BoldMT 13 underline",bg="#F6F7F9", fg=root.fg_secondary, bd=0, command=lambda:Delet_user(root))

        # emplace les widget dans la fenetre : 
        root.admin_space.frame_side.place(relx=0.0, rely=0.0)
        root.admin_space.frame_side.canva_titel.place(relx=0.1, rely=0.03)
        root.admin_space.frame_side.label_titel.place(relx=0.27, rely=0.07)
        root.admin_space.frame_side.canva_add_user.place(relx=0.03, rely=0.2)
        root.admin_space.frame_side.label_add_user.place(relx=0.17, rely=0.22)

        root.admin_space.frame_side.canva_delet_user.place(relx=0.03, rely=0.4)
        root.admin_space.frame_side.label_delet_user.place(relx=0.17, rely=0.42)

    else:
        messagebox.showerror("Probleme de vie privé ","Le compte connecté n est pas definie comme un super utilisateur")
    return

def see_more(key):
    try:
        key.window_find_results.label_titel_folder.destroy()
        key.window_find_results.tab_pays.destroy()
        key.window_find_results.tab_jobs.destroy()
        key.window_find_results.tab_nums.destroy()
        key.window_find_results.label_avance.destroy()
        key.window_find_results.label_engagement.destroy()
        key.window_find_results.label_date.destroy()
        key.window_find_results.bnt_see_passport.destroy()
        key.window_find_results.btn_see_selfi.destroy()
        key.window_find_results.btn_see_cv.destroy()
    except Exception as e:
        print("[Error] : "+str(e))
    selected = key.window_find_results.tabel_results.focus()
    key.window_find_results.selected_folder = key.window_find_results.tabel_results.item(selected, 'values')
    id = get_id_folder_by(key.window_find_results.selected_folder[1])
    current_folder = get_folder_by_id(id)
    print(current_folder)
    pay_colone = ('Pays')
    job_colone = ('Occupation')
    num_colone = ('Téléphone')
    pays_liste = [
        current_folder[11],
        current_folder[12],
        current_folder[13]
    ]
    job_liste = [
        str(current_folder[8]),
        str(current_folder[9]),
        str(current_folder[10])
    ]
    tele_liste = [
        current_folder[14],
        current_folder[15]
    ]
    key.window_find_results.label_titel_folder = Label(key.window_find_results,
        text="Plus D'information sur  "+str(key.window_find_results.selected_folder[1]),
        font="Arial-BoldMT 15", bg="#F6F7F9", fg=key.fg_secondary, bd=0)


    key.window_find_results.tab_nums = ttk.Treeview(key.window_find_results, 
        height=2, show="headings", column=num_colone)
    key.window_find_results.tab_pays = ttk.Treeview(key.window_find_results, 
        height=3, show="headings", column=pay_colone)
    key.window_find_results.tab_jobs = ttk.Treeview(key.window_find_results, 
        height=3, show="headings", column=job_colone)

    key.window_find_results.tab_pays.column("Pays", width="150", anchor=CENTER)
    key.window_find_results.tab_pays.heading("Pays", text="Pays")
    
    key.window_find_results.tab_nums.column("Téléphone", width="150", anchor=CENTER)
    key.window_find_results.tab_nums.heading("Téléphone", text="Téléphone")


    key.window_find_results.tab_jobs.column("Occupation",width="200", anchor=CENTER)
    key.window_find_results.tab_jobs.heading("Occupation", text="Occupation")

    for p in pays_liste:
        key.window_find_results.tab_pays.insert('',END,values=(p))

    for j in job_liste:
        key.window_find_results.tab_jobs.insert('',END,values=(j))

    for t in tele_liste:
        key.window_find_results.tab_nums.insert('',END,values=(t))
    # get data for current folder :
    current_data = get_data_folder_by_id(id)
    key.window_find_results.label_avance = Label(key.window_find_results,text="Avance :  "+str(current_data[1]),
        font="Arial-BoldMT 10 underline", bd=0, bg="#F6F7F9", fg=key.fg_secondary)
    key.window_find_results.label_engagement = Label(key.window_find_results,text="Engagement :  "+str(current_data[2]),
        font="Arial-BoldMT 10 underline", bd=0, bg="#F6F7F9", fg=key.fg_secondary)
    key.window_find_results.label_date = Label(key.window_find_results,text="Date :  "+str(current_data[3]),
        font="Arial-BoldMT 10 underline", bd=0, bg="#F6F7F9", fg=key.fg_secondary)
    #btn see data files for current folder : 
    key.window_find_results.bnt_see_passport = Button(key.window_find_results, text="Passport "+str(key.window_find_results.selected_folder[1]), font="Arial-BoldMT 9 underline",
        bg="#F6F7F9", fg=key.fg_secondary, bd=0, command=lambda:open_exploral("Passport",id))
    key.window_find_results.btn_see_selfi = Button(key.window_find_results, text="Photo "+str(key.window_find_results.selected_folder[1]), font="Arial-BoldMT 9 underline",
        bg="#F6F7F9", fg=key.fg_secondary, bd=0, command=lambda:open_exploral("selfi",id))
    key.window_find_results.btn_see_cv = Button(key.window_find_results, text="CV "+str(key.window_find_results.selected_folder[1]), font="Arial-BoldMT 9 underline",
        bg="#F6F7F9", fg=key.fg_secondary, bd=0, command=lambda:open_exploral("cv",id))
    # emplacer dans toplevel :
    key.window_find_results.label_titel_folder.place(relx=0.17,rely=0.415)
    key.window_find_results.tab_pays.place(relx=0.1, rely=0.45)    
    key.window_find_results.tab_jobs.place(relx=0.45, rely=0.45)
    key.window_find_results.tab_nums.place(relx=0.1, rely=0.6)
    key.window_find_results.label_avance.place(relx=0.45, rely=0.6)
    key.window_find_results.label_engagement.place(relx=0.45, rely=0.63)
    key.window_find_results.label_date.place(relx=0.45, rely=0.66)
    key.window_find_results.bnt_see_passport.place(relx=0.1, rely=0.7)
    key.window_find_results.btn_see_selfi.place(relx=0.1, rely=0.75)
    key.window_find_results.btn_see_cv.place(relx=0.1, rely=0.8)
    return

def see_folder_list(key):
    try:
        key.window_find_results.folder_liste.destroy()
        key.window_find_results.label_titel_folder.destroy()
    except Exception as e:
        print("[Error]"+str(e))
    selected = key.window_find_results.tabel_results.focus()
    key.window_find_results.selected_folder = key.window_find_results.tabel_results.item(selected, 'values')
    id = get_offre_id_by_name(key.window_find_results.selected_folder[0])
    print("id selected : "+str(id))
    liste_folder_ids = get_liste_id_folder(id)
    print("liste id liée : "+str(liste_folder_ids))
    tete_colone = ('Dossier', 'Cin', 'Age', 'Ville')
    key.window_find_results.label_titel_folder = Label(key.window_find_results,
        text="Dossiers liée a l'offre : "+str(key.window_find_results.selected_folder[0]),
        font="Arial-BoldMT 15", bg="#F6F7F9", fg=key.fg_secondary, bd=0)
    key.window_find_results.folder_liste = ttk.Treeview(key.window_find_results, 
                height=8, show="headings", column=tete_colone)
    key.window_find_results.folder_liste.column("Dossier", width="150", anchor=CENTER)
    key.window_find_results.folder_liste.column("Cin", width="100", anchor=CENTER)
    key.window_find_results.folder_liste.column("Age", width="50", anchor=CENTER)
    key.window_find_results.folder_liste.column("Ville", width="100", anchor=CENTER)
    key.window_find_results.folder_liste.heading("Dossier", text="Dossier")
    key.window_find_results.folder_liste.heading("Cin", text="Cin")
    key.window_find_results.folder_liste.heading("Age", text="Age")
    key.window_find_results.folder_liste.heading("Ville", text="Ville")
    for id_e in liste_folder_ids:
        folder = get_folder_by_id(id_e[0])
        if len(folder)==0:
            messagebox.showinfo("Info!", "Aucun Dossier disponible pour cette offre ")
            return    
        key.window_find_results.folder_liste.insert('',END,values=(
            folder[1],
            folder[3],
            folder[2],
            folder[4]))
    # ajouté le tableau au toplevel :
    key.window_find_results.label_titel_folder.place(relx=0.17, rely=0.45)
    key.window_find_results.folder_liste.place(relx=0.1, rely=0.55)
    return


def global_find(root,text,critaire):
    if text == '':
        messagebox.showinfo("Info!", "Aucune resultat disponible")
        return
    if is_date(text) == True:
        if critaire == "Dossier":
            data = get_all_folders_by(text)
            if len(data)==0:
                messagebox.showinfo("Info!", "Aucune resultat disponible")
                root.find.set('')
                return
        if critaire == "Offre":
            data = get_all_offre_by(text)
            if len(data)==0 or None in data[0]:
                messagebox.showinfo("Info!", "Aucune resultat disponible")
                root.find.set('')
                return
        root.window_find_results = Toplevel(bg="#F6F7F9", bd=0)
        root.window_find_results.geometry("800x550")
        root.window_find_results.resizable(0,0)
        root.window_find_results.iconbitmap("Images/logo2.ico")
        my_image = Image.open('Images/icons8-résultats-de-test-48.png')
        my_icon = ImageTk.PhotoImage(my_image)
        root.window_find_results.canva_find_result = Label(root.window_find_results, image=my_icon, height=48, width=48, bg="#F6F7F9")
        root.window_find_results.canva_find_result.image = my_icon
        # add label titel :
        root.window_find_results.label_titel = Label(root.window_find_results, text="Resultats sur "+str(critaire)+" : "+str(text),
            font="Arial-BoldMT 15 underline", bd=0, bg="#F6F7F9", fg=root.fg_secondary)
        # add treeview :
        if len(data[0])==4:
            # add tabel of folders : 
            tete_colone = ('Dossier', 'Niveau', 'Avance', 'Engagement')
            root.window_find_results.tabel_results = ttk.Treeview(root.window_find_results, 
                height=10, show="headings", column=tete_colone)
            root.window_find_results.tabel_results.column("Dossier", width="200", anchor=CENTER)
            root.window_find_results.tabel_results.column("Niveau", width="150", anchor=CENTER)
            root.window_find_results.tabel_results.column("Avance", width="80", anchor=CENTER)
            root.window_find_results.tabel_results.column("Engagement", width="100", anchor=CENTER)
            root.window_find_results.tabel_results.heading("Dossier", text="Dossier")
            root.window_find_results.tabel_results.heading("Niveau", text="Niveau")
            root.window_find_results.tabel_results.heading("Avance", text="Avance")
            root.window_find_results.tabel_results.heading("Engagement", text="Engagement")
            # insertion :
            for element in data:
                root.window_find_results.tabel_results.insert('', END, values=(
                element[0],element[1], element[2],element[3]))
        if len(data[0])==5:
            #add tabel of offres : 
            tete_colone = ('Offre', 'Pays', 'Dossier liée')
            root.window_find_results.tabel_results = ttk.Treeview(root.window_find_results, 
                height=10, show="headings", column=tete_colone)
            root.window_find_results.tabel_results.column("Offre", width="200", anchor=CENTER)
            root.window_find_results.tabel_results.column("Pays", width="200", anchor=CENTER)
            root.window_find_results.tabel_results.column("Dossier liée", width="100", anchor=CENTER)
            root.window_find_results.tabel_results.heading("Offre", text="Offre")
            root.window_find_results.tabel_results.heading("Pays", text="Pays")
            root.window_find_results.tabel_results.heading("Dossier liée", text="Dossier liée")
            for element in data:
                #nbr_links = count_folder_links_to_offre(element[0])
                root.window_find_results.tabel_results.insert('', END, values=(element[1],
                    element[2],element[4]))
        # emplacer les elements dans la fenetre : 
        root.window_find_results.canva_find_result.place(relx=0.1, rely=0.1)
        root.window_find_results.label_titel.place(relx=0.2, rely=0.13)
        root.window_find_results.tabel_results.place(relx=0.1, rely=0.22)
    else:
        if critaire == "Dossier":
            print("find folder ")
            data = get_folder_by_critaire(text)
            if len(data)==0:
                messagebox.showinfo("Info!", "Aucune resultat disponible")
                root.find.set('')
                return
            print(data)
            # creation du toplevel fenetre :
            root.window_find_results = Toplevel(bg="#F6F7F9", bd=0)
            root.window_find_results.geometry("500x750")
            root.window_find_results.resizable(0,0)
            root.window_find_results.iconbitmap("Images/logo2.ico")
            my_image = Image.open('Images/icons8-résultats-de-test-48.png')
            my_icon = ImageTk.PhotoImage(my_image)
            root.window_find_results.canva_find_result = Label(root.window_find_results, image=my_icon, height=48, width=48, bg="#F6F7F9")
            root.window_find_results.canva_find_result.image = my_icon
            root.window_find_results.label_titel = Label(root.window_find_results, text="Resultats sur : "+str(text),
            font="Arial-BoldMT 15 underline", bd=0, bg="#F6F7F9", fg=root.fg_secondary)
            tete_colone =('Age', 'Dossier', 'Cin', "Ville", 'N etude')
            root.window_find_results.tabel_results = ttk.Treeview(root.window_find_results, 
                height=10, show="headings", column=tete_colone)
            root.window_find_results.tabel_results.column("Age", width="35", anchor=CENTER)
            root.window_find_results.tabel_results.column("Dossier", width="150", anchor=CENTER)
            root.window_find_results.tabel_results.column("Cin", width="100", anchor=CENTER)
            root.window_find_results.tabel_results.column("Ville", width="100", anchor=CENTER)
            root.window_find_results.tabel_results.column("N etude", width="100", anchor=CENTER)
            root.window_find_results.tabel_results.heading("Age", text="Age")
            root.window_find_results.tabel_results.heading("Dossier", text="Dossier")
            root.window_find_results.tabel_results.heading("Cin", text="Cin")
            root.window_find_results.tabel_results.heading("Ville", text="Ville")
            root.window_find_results.tabel_results.heading("N etude", text="N etude")
            for element in data:
                root.window_find_results.tabel_results.insert('',END, values=(
                    element[2],
                    element[1],
                    element[3],
                    element[4],
                    element[6]
                    ))
            root.window_find_results.tabel_results.bind("<Double-1>", lambda event:see_more(key=root))
            # emplacer le tableau dans toplevel :
            root.window_find_results.canva_find_result.place(relx=0.15, rely=0.01)
            root.window_find_results.label_titel.place(relx=0.25, rely=0.04)
            root.window_find_results.tabel_results.place(relx=0.01, rely=0.1)
        if critaire == "Offre":
            print("find offre ")
            data = get_offre_by_critaire(text)
            if len(data)==0:
                messagebox.showinfo("Info!", "Aucune resultat disponible")
                root.find.set('')
                return
            # creation du toplevel fenetre :
            root.window_find_results = Toplevel(bg="#F6F7F9", bd=0)
            root.window_find_results.geometry("500x750")
            root.window_find_results.resizable(0,0)
            root.window_find_results.iconbitmap("Images/logo2.ico")
            my_image = Image.open('Images/icons8-résultats-de-test-48.png')
            my_icon = ImageTk.PhotoImage(my_image)
            root.window_find_results.canva_find_result = Label(root.window_find_results, image=my_icon, height=48, width=48, bg="#F6F7F9")
            root.window_find_results.canva_find_result.image = my_icon
            root.window_find_results.label_titel = Label(root.window_find_results, text="Resultats sur : "+str(text),
            font="Arial-BoldMT 15 underline", bd=0, bg="#F6F7F9", fg=root.fg_secondary)
            tete_colone = ('Titre', 'Pays', 'Occupation', 'Dossiers')
            root.window_find_results.tabel_results = ttk.Treeview(root.window_find_results, 
                height=10, show="headings", column=tete_colone)
            root.window_find_results.tabel_results.column("Titre", width="150", anchor=CENTER)
            root.window_find_results.tabel_results.column("Pays", width="100", anchor=CENTER)
            root.window_find_results.tabel_results.column("Occupation", width="150", anchor=CENTER)
            root.window_find_results.tabel_results.column("Dossiers", width="55", anchor=CENTER)
            root.window_find_results.tabel_results.heading("Titre", text="Titre")
            root.window_find_results.tabel_results.heading("Pays", text="Pays")
            root.window_find_results.tabel_results.heading("Occupation", text="Occupation")
            root.window_find_results.tabel_results.heading("Dossiers", text="Dossiers")            
            for d in data:
                root.window_find_results.tabel_results.insert('',END,values=(
                    d[1],
                    d[4],
                    d[5],
                    count_folder_links_to_offre(d[0])))
            root.window_find_results.tabel_results.bind("<Double-1>", lambda event:see_folder_list(key=root))
            # emplacer le tableau dans toplevel :
            root.window_find_results.canva_find_result.place(relx=0.15, rely=0.01)
            root.window_find_results.label_titel.place(relx=0.25, rely=0.04)
            root.window_find_results.tabel_results.place(relx=0.05, rely=0.1)
    return