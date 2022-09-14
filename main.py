from tkinter import *
from PIL import Image, ImageTk
from tkinter import messagebox
from datetime import date
from datetime import datetime
from Modules.Users import *
from Modules.GUI import *
from Modules.Folder import *
from Modules.Offre import *
from Modules.tkinter_custom_button.tkinter_custom_button import TkinterCustomButton
class Task_Manager():
    def __init__(self):
        self.window = Tk()
        self.bg_color = "#3A7FF6"
        self.fg_color = "white"
        self.secondary_color = "#3479D7"
        self.fg_secondary = "#515486"
        self.user_name = StringVar()
        self.user_password = StringVar()
        # config window :
        self.window.geometry("862x519")
        self.window.config(background=self.fg_color)
        self.window.resizable(0, 0)
        self.window.iconbitmap("Images/logo2.ico")
        self.window.title(' Gestionnaire de tâches Baker Asmar 1.0 ')
        self.user_name = StringVar()
        self.user_password = StringVar()
        # login system:
        self.canvas = Canvas(self.window,bg="#3A7FF6",height=519,width=862,bd=0, highlightthickness=0,relief="ridge")
        self.canvas.place(x=0,y=0)
        self.canvas.create_rectangle(431, 0, 431 + 431, 0 + 519, fill="#FCFCFC",outline="")
        self.canvas.create_rectangle(40, 160, 40 + 60, 160 + 5, fill="#FCFCFC",outline="")

        self.text_box_bg = PhotoImage(file=f"images/TextBox_Bg.png")
        
        self.token_entry_img = self.canvas.create_image(650.5,167.5,image=self.text_box_bg)
        self.URL_entry_img = self.canvas.create_image(650.5,248.5,image=self.text_box_bg)

        self.user_entry = Entry(bd=0,bg="#F6F7F9",highlightthickness=0,textvariable=self.user_name)
        self.user_entry.place(x=490.0,y=137+25,width=321.0,height=35)
        self.user_entry.focus()

        self.pswd_entry = Entry(bd=0,bg="#F6F7F9",highlightthickness=0, textvariable=self.user_password)
        self.pswd_entry.place(x=490.0,y=218+25,width=321.0,height=35)
        self.canvas.create_text(519.0,156.0,text="Nom Utilisateur ",fill="#515486",font=("Arial-BoldMT",int(13.0)))
        self.canvas.create_text(518.5,234.5,text="Mot De Pass ",fill="#515486",font=("Arial-BoldMT",int(13.0)))
        self.canvas.create_text(573.5,88.0,text="Entrez les détails.",fill="#515486",font=("Arial-BoldMT",int(22.0)))

        self.login_btn = Button(self.window, text="Connexion" , borderwidth=0, highlightthickness=0, 
            relief="flat", font="Arial-BoldMT 15", bg=self.bg_color, fg=self.fg_color, command=self.user_connexion)
        self.login_btn.place(x=700, y=401, width=100, height=30)


        self.title = Label(text="Bienvenue ", bg="#3A7FF6",fg="white",font=("Arial-BoldMT",int(20.0)))
        self.title.place(x=27.0,y=120.0)

        self.info_text = Label(text="Tkinter Designer uses the Figma API\n"
                           "to analyse a design file, then creates\n"
                           "the respective code and files needed\n"
                           "for your GUI.\n\n"
                           
                           "Even this GUI was created\n"
                           "using Tkinter Designer.",
                      bg="#3A7FF6",fg="white",justify="left",font=("Georgia",int(16.0)))

        self.info_text.place(x=27.0,y=200.0)
    
    def clear_window(self):
        self.canvas.destroy()
        self.text_box_bg.config(file='')
        self.user_entry.destroy()
        self.pswd_entry.destroy()
        self.login_btn.destroy()
        self.title.destroy()
        self.info_text.destroy()
        return
    
    def disabled_menu(self):
        self.profil.entryconfig("Montre le profil", state="disabled")
        self.profil.entryconfig("Mettre à jour le profil", state="disabled")
        self.tasks.entryconfig("Afficher les offres", state="disabled")
        self.tasks.entryconfig("Ajouter une nouvelle offre", state="disabled")
        self.tasks.entryconfig("Supprimer Offre", state="disabled")
        self.users.entryconfig("Afficher les Dossiers", state="disabled")
        self.users.entryconfig("Ajouter un Dossier", state="disabled")
        self.users.entryconfig("Lister les dossiers par critère", state="disabled")
        self.canva_logo.destroy()
        self.canva_find.destroy()
        self.canva_find_icon.destroy()
        self.label_find.destroy()
        self.entry_find.destroy()
        self.combo_critaire.destroy()
        self.btn_find.destroy()
        self.canva_statistique.destroy()
        self.canva_icon_sta.destroy()
        self.label_sta.destroy()
        self.btn_see_sta.destroy()
        self.canva_notif.destroy()
        self.canva_icon_notif.destroy()
        self.label_notif.destroy()
        self.btn_see_notif.destroy()
        self.canva_users.destroy()
        self.canva_icon_users.destroy()
        self.label_users.destroy()
        self.btn_see_users.destroy()
        self.canva_admin.destroy()
        self.canva_icon_admin.destroy()
        self.label_admin.destroy()
        self.btn_see_admin.destroy()
        return
    
    def enabel_menu(self):
        self.profil.entryconfig("Montre le profil", state="normal")
        self.profil.entryconfig("Mettre à jour le profil", state="normal")
        self.tasks.entryconfig("Afficher les offres", state="normal")
        self.tasks.entryconfig("Ajouter une nouvelle offre", state="normal")
        self.tasks.entryconfig("Supprimer Offre", state="normal")
        self.users.entryconfig("Afficher les Dossiers", state="normal")
        self.users.entryconfig("Ajouter un Dossier", state="normal")
        self.users.entryconfig("Lister les dossiers par critère", state="normal")
        #create dashbord window :
        # create a page main : 
        my_image = Image.open('Images/Logo_Bakr.png')
        my_icon = ImageTk.PhotoImage(my_image)
        self.canva_logo = Label(self.window, image=my_icon, width=452, height=200, bd=0)
        self.canva_logo.image = my_icon
        # search outils :
        # <==================================================== >
        my_image = Image.open('Images/TextBox_Bg.png')
        my_icon = ImageTk.PhotoImage(my_image)
        self.canva_find = Label(self.window, image=my_icon, height=85, width=340, bg=self.fg_color)
        self.canva_find.image = my_icon
        my_image = Image.open('Images/icons8-chercher-24.png')
        my_icon = ImageTk.PhotoImage(my_image)
        self.canva_find_icon = Label(self.window, image=my_icon, height=24, width=24, bg="#F6F7F9")
        self.canva_find_icon.image = my_icon
        
        self.label_find = Label(self.window, text="Cherche  ", font="Arial-BoldMT 13",
                                bg="#F6F7F9", fg=self.fg_secondary)
        self.entry_find = Entry(self.window, textvariable=self.find, font="Arial-BoldMT 13",  fg="black",
                                bg="#F6F7F9", width=37, bd=0)
        self.combo_critaire = ttk.Combobox(self.window,value=["Dossier","Offre"], state='readonly', width=20, 
            height=2)
        self.btn_find = Button(self.window, text="Chercher", font="Arial-BoldMT 8 underline", bg="#F6F7F9",
            fg=self.bg_color, bd=0, command=lambda:global_find(self,self.find.get(),self.combo_critaire.get()))
        self.combo_critaire.current(0)
        # <==================================================== >
        # Statictique outils : 
        my_image = Image.open('Images/TextBox_Bg.png')
        my_icon = ImageTk.PhotoImage(my_image)
        self.canva_statistique = Label(self.window, image=my_icon, height=85, width=340, bg=self.fg_color)
        self.canva_statistique.image = my_icon
        # icon statistique :
        my_image = Image.open('Images/icons8-statistiques-64.png')
        my_icon = ImageTk.PhotoImage(my_image)
        self.canva_icon_sta = Label(self.window, image=my_icon, height=64, width=64, bg="#F6F7F9")
        self.canva_icon_sta.image = my_icon

        self.label_sta = Label(self.window, text="Statistiques  ", font="Arial-BoldMT 13 underline",
                                bg="#F6F7F9", fg=self.fg_secondary)
        self.btn_see_sta = Button(self.window, text="Plus..", font="Arial-BoldMT 8 underline", bg="#F6F7F9",
            fg=self.bg_color, bd=0)
        # =========================================================== >
        # Notification outils :
        my_image = Image.open('Images/TextBox_Bg.png')
        my_icon = ImageTk.PhotoImage(my_image)
        self.canva_notif = Label(self.window, image=my_icon, height=85, width=340, bg=self.fg_color)
        self.canva_notif.image = my_icon
        # icon notification : 
        my_image = Image.open('Images/icons8-bell-64.png')
        my_icon = ImageTk.PhotoImage(my_image)
        self.canva_icon_notif = Label(self.window, image=my_icon, height=64, width=64, bg="#F6F7F9")
        self.canva_icon_notif.image = my_icon        
        self.label_notif = Label(self.window, text="Notification  ", font="Arial-BoldMT 13 underline",
                                bg="#F6F7F9", fg=self.fg_secondary)
        self.btn_see_notif = Button(self.window, text="Plus..", font="Arial-BoldMT 8 underline", bg="#F6F7F9",
            fg=self.bg_color, bd=0)
        # ==============================================================>
        # about users outils :
        my_image = Image.open('Images/TextBox_Bg.png')
        my_icon = ImageTk.PhotoImage(my_image)
        self.canva_users = Label(self.window, image=my_icon, height=85, width=340, bg=self.fg_color)
        self.canva_users.image = my_icon
        # about users icon : 
        my_image = Image.open('Images/icons8-users-64.png')
        my_icon = ImageTk.PhotoImage(my_image)
        self.canva_icon_users = Label(self.window, image=my_icon, height=64, width=64, bg="#F6F7F9")
        self.canva_icon_users.image = my_icon        
        self.label_users = Label(self.window, text="à propos de l'utilisateur ", font="Arial-BoldMT 13 underline",
                                bg="#F6F7F9", fg=self.fg_secondary)
        self.btn_see_users = Button(self.window, text="Plus..", font="Arial-BoldMT 8 underline", bg="#F6F7F9",
            fg=self.bg_color, bd=0, command=lambda:see_users_by_admin(self))
        # ========================================================================
        # Adminstrate space : 
        my_image = Image.open('Images/TextBox_Bg.png')
        my_icon = ImageTk.PhotoImage(my_image)
        self.canva_admin = Label(self.window, image=my_icon, height=85, width=340, bg=self.fg_color)
        self.canva_admin.image = my_icon
        #  admin icon : 
        my_image = Image.open('Images/icons8-admin-64.png')
        my_icon = ImageTk.PhotoImage(my_image)
        self.canva_icon_admin = Label(self.window, image=my_icon, height=64, width=64, bg="#F6F7F9")
        self.canva_icon_admin.image = my_icon        
        self.label_admin = Label(self.window, text="Espace administrateur ", font="Arial-BoldMT 13 underline",
                                bg="#F6F7F9", fg=self.fg_secondary)
        self.btn_see_admin = Button(self.window, text="Plus..", font="Arial-BoldMT 8 underline", bg="#F6F7F9",
            fg=self.bg_color, bd=0, command=lambda:see_admin_space(self))

        # emplacé les element dans la fentere : 
        self.entry_find.focus()
        self.canva_logo.place(relx=0.0, rely=0.0)
        self.canva_find.place(relx=0.5, rely=0.0)
        self.canva_find_icon.place(relx=0.5, rely=0.02)
        self.label_find.place(relx=0.53, rely=0.02)
        self.entry_find.place(relx=0.5, rely=0.065)
        self.combo_critaire.place(relx=0.5, rely=0.1)
        self.btn_find.place(relx=0.76, rely=0.105)
        
        self.canva_statistique.place(relx=0.02, rely=0.37)
        self.canva_icon_sta.place(relx=0.02, rely=0.3)
        self.label_sta.place(relx=0.15, rely=0.4)
        self.btn_see_sta.place(relx=0.29,rely=0.47)

        self.canva_notif.place(relx=0.5, rely=0.37)
        self.canva_icon_notif.place(relx=0.5, rely=0.3)
        self.label_notif.place(relx=0.63, rely=0.4)
        self.btn_see_notif.place(relx=0.77, rely=0.47)


        self.canva_users.place(relx=0.02, rely=0.67)
        self.canva_icon_users.place(relx=0.02, rely=0.6)
        self.label_users.place(relx=0.15, rely=0.7)
        self.btn_see_users.place(relx=0.29,rely=0.77)

        self.canva_admin.place(relx=0.5, rely=0.67)
        self.canva_icon_admin.place(relx=0.5, rely=0.6)
        self.label_admin.place(relx=0.63, rely=0.7)
        self.btn_see_admin.place(relx=0.77, rely=0.77)
        return
    
    def seconde_window(self):
        self.find = StringVar()
        self.window.geometry("1100x550")
        self.window.config(background=self.fg_color)
        self.menu_princip = Menu(self.window, tearoff=0)
        self.profil = Menu(self.menu_princip, tearoff=0)
        self.profil.add_cascade(label="Montre le profil", command=self.show_profile)
        self.profil.add_cascade(label="Mettre à jour le profil", command=self.update_profile)
        self.menu_princip.add_cascade(label="Profil", menu=self.profil)
        # Seconde :
        self.tasks = Menu(self.menu_princip, tearoff=0)
        self.tasks.add_cascade(label="Afficher les offres", command=lambda:Liste_offre(self))
        self.tasks.add_cascade(label="Ajouter une nouvelle offre", command=lambda:Add_Offre(self))
        self.tasks.add_cascade(label="Supprimer Offre", command=lambda:delet_offre(self))
        self.menu_princip.add_cascade(label="Offre", menu=self.tasks)
        # Last One :
        self.users = Menu(self.menu_princip, tearoff=0)
        self.users.add_cascade(label="Afficher les Dossiers", command= lambda:Liste_folder(self))
        self.users.add_cascade(label="Ajouter un Dossier", command= lambda:Add_folder(self))
        self.users.add_cascade(label="Lister les dossiers par critère", command=lambda:Find_folder(self))
        self.menu_princip.add_cascade(label="Dossier", menu=self.users)
        # Add Menu to Window :
        self.window.config(menu=self.menu_princip)
        # create a page main : 
        my_image = Image.open('Images/Logo_Bakr.png')
        my_icon = ImageTk.PhotoImage(my_image)
        self.canva_logo = Label(self.window, image=my_icon, width=452, height=200, bd=0)
        self.canva_logo.image = my_icon
        # search outils :
        # <==================================================== >
        my_image = Image.open('Images/TextBox_Bg.png')
        my_icon = ImageTk.PhotoImage(my_image)
        self.canva_find = Label(self.window, image=my_icon, height=85, width=340, bg=self.fg_color)
        self.canva_find.image = my_icon
        my_image = Image.open('Images/icons8-chercher-24.png')
        my_icon = ImageTk.PhotoImage(my_image)
        self.canva_find_icon = Label(self.window, image=my_icon, height=24, width=24, bg="#F6F7F9")
        self.canva_find_icon.image = my_icon
        
        self.label_find = Label(self.window, text="Cherche  ", font="Arial-BoldMT 13",
                                bg="#F6F7F9", fg=self.fg_secondary)
        self.entry_find = Entry(self.window, textvariable=self.find, font="Arial-BoldMT 13",  fg="black",
                                bg="#F6F7F9", width=37, bd=0)
        self.combo_critaire = ttk.Combobox(self.window,value=["Dossier","Offre"], state='readonly', width=20, 
            height=2)
        self.btn_find = Button(self.window, text="Chercher", font="Arial-BoldMT 8 underline", bg="#F6F7F9",
            fg=self.bg_color, bd=0, command=lambda:global_find(self,self.find.get(),self.combo_critaire.get()))

        self.combo_critaire.current(0)
        # <==================================================== >
        # Statictique outils : 
        my_image = Image.open('Images/TextBox_Bg.png')
        my_icon = ImageTk.PhotoImage(my_image)
        self.canva_statistique = Label(self.window, image=my_icon, height=85, width=340, bg=self.fg_color)
        self.canva_statistique.image = my_icon
        # icon statistique :
        my_image = Image.open('Images/icons8-statistiques-64.png')
        my_icon = ImageTk.PhotoImage(my_image)
        self.canva_icon_sta = Label(self.window, image=my_icon, height=64, width=64, bg="#F6F7F9")
        self.canva_icon_sta.image = my_icon

        self.label_sta = Label(self.window, text="Statistiques  ", font="Arial-BoldMT 13 underline",
                                bg="#F6F7F9", fg=self.fg_secondary)
        self.btn_see_sta = Button(self.window, text="Plus..", font="Arial-BoldMT 8 underline", bg="#F6F7F9",
            fg=self.bg_color, bd=0)
        # =========================================================== >
        # Notification outils :
        my_image = Image.open('Images/TextBox_Bg.png')
        my_icon = ImageTk.PhotoImage(my_image)
        self.canva_notif = Label(self.window, image=my_icon, height=85, width=340, bg=self.fg_color)
        self.canva_notif.image = my_icon
        # icon notification : 
        my_image = Image.open('Images/icons8-bell-64.png')
        my_icon = ImageTk.PhotoImage(my_image)
        self.canva_icon_notif = Label(self.window, image=my_icon, height=64, width=64, bg="#F6F7F9")
        self.canva_icon_notif.image = my_icon        
        self.label_notif = Label(self.window, text="Notification  ", font="Arial-BoldMT 13 underline",
                                bg="#F6F7F9", fg=self.fg_secondary)
        self.btn_see_notif = Button(self.window, text="Plus..", font="Arial-BoldMT 8 underline", bg="#F6F7F9",
            fg=self.bg_color, bd=0)
        # ==============================================================>
        # about users outils :
        my_image = Image.open('Images/TextBox_Bg.png')
        my_icon = ImageTk.PhotoImage(my_image)
        self.canva_users = Label(self.window, image=my_icon, height=85, width=340, bg=self.fg_color)
        self.canva_users.image = my_icon
        # about users icon : 
        my_image = Image.open('Images/icons8-users-64.png')
        my_icon = ImageTk.PhotoImage(my_image)
        self.canva_icon_users = Label(self.window, image=my_icon, height=64, width=64, bg="#F6F7F9")
        self.canva_icon_users.image = my_icon        
        self.label_users = Label(self.window, text="à propos de l'utilisateur ", font="Arial-BoldMT 13 underline",
                                bg="#F6F7F9", fg=self.fg_secondary)
        self.btn_see_users = Button(self.window, text="Plus..", font="Arial-BoldMT 8 underline", bg="#F6F7F9",
            fg=self.bg_color, bd=0, command=lambda:see_users_by_admin(self))
        # ========================================================================
        # Adminstrate space : 
        my_image = Image.open('Images/TextBox_Bg.png')
        my_icon = ImageTk.PhotoImage(my_image)
        self.canva_admin = Label(self.window, image=my_icon, height=85, width=340, bg=self.fg_color)
        self.canva_admin.image = my_icon
        #  admin icon : 
        my_image = Image.open('Images/icons8-admin-64.png')
        my_icon = ImageTk.PhotoImage(my_image)
        self.canva_icon_admin = Label(self.window, image=my_icon, height=64, width=64, bg="#F6F7F9")
        self.canva_icon_admin.image = my_icon        
        self.label_admin = Label(self.window, text="Espace administrateur ", font="Arial-BoldMT 13 underline",
                                bg="#F6F7F9", fg=self.fg_secondary)
        self.btn_see_admin = Button(self.window, text="Plus..", font="Arial-BoldMT 8 underline", bg="#F6F7F9",
            fg=self.bg_color, bd=0, command=lambda:see_admin_space(self))

        # emplacé les element dans la fentere : 
        self.entry_find.focus()
        self.canva_logo.place(relx=0.0, rely=0.0)
        self.canva_find.place(relx=0.5, rely=0.0)
        self.canva_find_icon.place(relx=0.5, rely=0.02)
        self.label_find.place(relx=0.53, rely=0.02)
        self.entry_find.place(relx=0.5, rely=0.065)
        self.combo_critaire.place(relx=0.5, rely=0.1)
        self.btn_find.place(relx=0.76, rely=0.105)
        
        self.canva_statistique.place(relx=0.02, rely=0.37)
        self.canva_icon_sta.place(relx=0.02, rely=0.3)
        self.label_sta.place(relx=0.15, rely=0.4)
        self.btn_see_sta.place(relx=0.29,rely=0.47)

        self.canva_notif.place(relx=0.5, rely=0.37)
        self.canva_icon_notif.place(relx=0.5, rely=0.3)
        self.label_notif.place(relx=0.63, rely=0.4)
        self.btn_see_notif.place(relx=0.77, rely=0.47)


        self.canva_users.place(relx=0.02, rely=0.67)
        self.canva_icon_users.place(relx=0.02, rely=0.6)
        self.label_users.place(relx=0.15, rely=0.7)
        self.btn_see_users.place(relx=0.29,rely=0.77)

        self.canva_admin.place(relx=0.5, rely=0.67)
        self.canva_icon_admin.place(relx=0.5, rely=0.6)
        self.label_admin.place(relx=0.63, rely=0.7)
        self.btn_see_admin.place(relx=0.77, rely=0.77)
        
        return
    
    def update_profile(self):
        self.disabled_menu()
        self.frame_body = Frame(self.window , height=350, width=600, bd=0, bg=self.fg_color)
        # --------> Insertion d image au canva :
        my_image = Image.open('Images/icons8-info-64.png')
        my_icon = ImageTk.PhotoImage(my_image)
        canva = Label(self.frame_body, image=my_icon, height=65, width=65, bg=self.fg_color)
        canva.image = my_icon
        self.label = Label(self.frame_body, text="Données d'utilisateur :" , font="Arial-BoldMT 20 underline",
            bg=self.fg_color, fg=self.fg_secondary, bd=0)
        # input system:
        my_image = Image.open('Images/TextBox_Bg.png')
        my_icon = ImageTk.PhotoImage(my_image)
        # ----------------------------------------------------------------------------------------------------------
        # User Name : 

        self.canva_user = Label(self.frame_body, image=my_icon, height=65, width=340, bg=self.fg_color)
        self.canva_user.image = my_icon
        self.label_user = Label(self.frame_body, text="Nom Utilisateur ", font="Arial-BoldMT 13",
                                bg="#F6F7F9", fg=self.fg_secondary)
        self.entry_user = Entry(self.frame_body, textvariable=self.user_name, font="Arial-BoldMT 13",  fg="black",
                                bg="#F6F7F9", width=37, bd=0)
        # ---------------------------------------------------------------------------------------------------------
        #user Password :

        self.canva_password = Label(self.frame_body, image=my_icon, height=65, width=340, bg=self.fg_color)
        self.canva_password.image = my_icon
        self.label_password = Label(self.frame_body, text="Mot de Pass utilisateur ", font="Arial-BoldMT 13",
                                bg="#F6F7F9", fg=self.fg_secondary)
        self.entry_password = Entry(self.frame_body, textvariable=self.user_password, font="Arial-BoldMT 13",  fg="black",
                                bg="#F6F7F9", width=37, bd=0)
        #-----------------------------------------------------------------------------------------------------------
        #user Access setting :
        self.type_compte = StringVar()
        self.type_compte.set(str(self.connexion[3]))

        self.canva_type = Label(self.frame_body, image=my_icon, height=65, width=340, bg=self.fg_color)
        self.canva_type.image = my_icon
        self.label_type = Label(self.frame_body, text="Mode d acce utilisateur ", font="Arial-BoldMT 13",
                                bg="#F6F7F9", fg=self.fg_secondary)
        self.entry_type = Entry(self.frame_body, textvariable=self.type_compte, font="Arial-BoldMT 13",  fg="black",
                                bg="#F6F7F9", width=37, bd=0)

        # -----------------------------------------------------------------------------------------------------------
        # Btn update : 
        self.btn_update = Button(master=self.window,bg=self.bg_color,fg=self.fg_color,
                                            font="Arial-BoldMT 12",text="Enregistré",bd=0, command= lambda:Update_User(self.connexion[0],
                                                self.user_name.get(),self.user_password.get(), self))
        
        self.btn_cancel = Button(master=self.window,bg=self.fg_secondary,fg=self.fg_color,
                                            font="Arial-BoldMT 12",text="annuler",bd=0, command=self.clear_widget_update)
        # add widget into window :
        canva.place(relx=0.01, rely=0.1)
        self.label.place(relx=0.13, rely=0.15)
        self.label_user.place(relx=0.12, rely=0.33)
        self.canva_user.place(relx=0.12, rely=0.33)
        self.entry_user.place(relx=0.12, rely=0.42)

        self.label_password.place(relx=0.12, rely=0.62)
        self.canva_password.place(relx=0.12, rely=0.62)
        self.entry_password.place(relx=0.12, rely=0.73)
        
        
        self.label_type.place(relx=0.12, rely=0.84)
        self.canva_type.place(relx=0.12, rely=0.84)
        self.entry_type.place(relx=0.12, rely=0.9)
        self.btn_update.place(relx=0.38, rely=0.9)
        self.btn_cancel.place(relx=0.49, rely=0.9)
        self.frame_body.place(relx=0.2, rely=0.1)
        return

    def show_profile(self):
        self.disabled_menu()
        my_image = Image.open('Images/icons8-user-64.png')
        my_icon = ImageTk.PhotoImage(my_image)
        self.canva_image = Label(self.window, image=my_icon, height=80, width=80, bg=self.fg_color)
        self.canva_image.image = my_icon
        self.label_Profile = Label(self.window, text=" Profile ", font="Arial-BoldMT 21 underline", fg=self.fg_secondary
            , bg=self.fg_color, bd=0)
        self.label_Name = Label(self.window, text=str(self.user_name.get()), font="Arial-BoldMT 20", fg=self.fg_secondary
            , bg=self.fg_color, bd=0)
        self.label_access = Label(self.window, text="Compte : "+str(self.connexion[3]), font="Arial-BoldMT 20", bg=self.fg_color
            , fg=self.fg_secondary, bd=0)
        self.label_designe = Frame(self.window, width=150, height=5, bg=self.fg_secondary)

        self.current_widget = [self.label_designe, self.label_access, 
                            self.label_Name, self.label_Profile, self.canva_image]
        self.btn_cancel = TkinterCustomButton(master=self.window,
                                            bg_color="#F6F7F9",
                                            fg_color=self.fg_color,
                                            hover_color=self.fg_secondary,
                                            border_color=self.fg_color,
                                            text_font="Arial-BoldMT",
                                            text="Retour",
                                            text_color="black",
                                            corner_radius=10,
                                            width=100,
                                            height=30,
                                            hover=True,
                                            command = self.clear_widget_profile)
        # Emplace :
        self.canva_image.place(relx=0.3, rely=0.1)
        self.label_Name.place(relx=0.4, rely=0.13)
        self.label_access.place(relx=0.4, rely=0.22)
        self.label_designe.place(relx=0.42, rely=0.35)
        self.btn_cancel.place(relx=0.5, rely=0.4)
        return

    def clear_widget_profile(self):
        self.canva_image.destroy()
        self.label_Name.destroy()
        self.label_access.destroy()
        self.label_designe.destroy()
        self.btn_cancel.destroy()
        self.enabel_menu()
        return

    def clear_widget_update(self):
        self.frame_body.destroy()
        self.btn_update.destroy()
        self.btn_cancel.destroy()
        self.enabel_menu()
        return

    def user_connexion(self):
        user =self.user_name.get()
        password = self.user_password.get() 
        self.connexion = User_connect(user,password)
        print(self.connexion)
        if self.connexion==[]:
            messagebox.showerror("Erreur de connexion!", "Impossible de se connecter en tant que "+str(user))
            self.user_entry.delete(0, "end")
            self.pswd_entry.delete(0, "end")
            self.user_entry.focus()
        else:
            messagebox.showinfo("Connexion bien établie!", "Bienvenue  "+str(user))
            date_str = str(datetime.now())
            update_last_connexion(self.connexion[0], date_str)
            # clear window :
            self.clear_window()
            self.seconde_window()
        return
    
    def run(self):
        self.window.mainloop()
        return


if __name__ == '__main__':
    my_window = Task_Manager()
    my_window.run()
