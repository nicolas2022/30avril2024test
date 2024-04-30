import customtkinter as ctk
from tkinter import messagebox
import smtplib
from email.mime.text import MIMEText
from smtplib import SMTPException, SMTPAuthenticationError
from datetime import datetime

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

# Création du dictionnaire pour stocker l'historique des mots de passe
historique_password = {"Nicolas": [("motdepasse", datetime.now()),
                                   ("MDP", datetime.now()),
                                   ("123", datetime.now())]}


def login():
    username = username_entry.get()
    password = password_entry.get()

    # Vérifier si l'utilisateur existe dans l'historique des mots de passe
    if username in historique_password:
        # Vérifier si le mot de passe est le dernier dans l'historique
        if password == historique_password[username][-1][0]:
            # Afficher un message de bienvenue
            messagebox.showinfo("Bienvenue", "Connexion réussie ! Bienvenue !")
        else:
            messagebox.showerror("Erreur de connexion", "Mot de passe incorrect.")
    else:
        messagebox.showerror("Erreur de connexion", "Identifiant incorrect.")


def forgot_password():
    # Envoyer un e-mail avec un lien pour changer le mot de passe
    try:
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        sender_email = "tv.desappointement@gmail.com"
        receiver_email = "nicolas.bertolini@gmail.com"
        password = "motdepasseemail"  # Mot de passe de votre compte Gmail

        # Créer un message
        message = MIMEText("Cliquez sur ce lien pour changer votre mot de passe : http://changementmotdepasse.com")
        message['Subject'] = "Réinitialisation du mot de passe"
        message['From'] = sender_email
        message['To'] = receiver_email

        # Connexion au serveur SMTP et envoi de l'email
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())

        messagebox.showinfo("Mot de passe oublié",
                            "Un email a été envoyé avec un lien pour réinitialiser votre mot de passe.")

    except SMTPAuthenticationError:
        messagebox.showerror("Erreur", "Authentification SMTP échouée. Veuillez vérifier vos identifiants Gmail.")
    except SMTPException as e:
        messagebox.showerror("Erreur", f"Une erreur SMTP s'est produite : {e}")
    except Exception as e:
        messagebox.showerror("Erreur", f"Une erreur s'est produite lors de l'envoi de l'email : {e}")


def on_username_entry_return(event):
    # Lorsque la touche "Entrée" est pressée dans username_entry, le focus passe à password_entry
    password_entry.focus_set()


def on_password_entry_return(event):
    # Lorsque la touche "Entrée" est pressée dans password_entry, appeler la fonction login
    login()


# Création de la fenêtre principale
interface_de_connexion = ctk.CTk()
interface_de_connexion.title("Gestion des ADD - Connexion")
interface_de_connexion.geometry("400x300")


# Label et Entry pour l'identifiant
username_label = ctk.CTkLabel(interface_de_connexion, text="Identifiant:")
username_label.pack(pady=5, padx=12)
username_entry = ctk.CTkEntry(interface_de_connexion, width=300)
username_entry.pack()

# Liaison de l'événement "Return" à la fonction on_username_entry_return
username_entry.bind("<Return>", on_username_entry_return)

# Label et Entry pour le mot de passe
password_label = ctk.CTkLabel(interface_de_connexion, text="Mot de passe:")
password_label.pack(pady=5, padx=12)
password_entry = ctk.CTkEntry(interface_de_connexion, show="*")
password_entry.pack()

# Liaison de l'événement "Return" à la fonction on_password_entry_return
password_entry.bind("<Return>", on_password_entry_return)

# Bouton "Connexion"
login_button = ctk.CTkButton(interface_de_connexion, text="Connexion", command=login)
login_button.pack(pady=25, padx=12)

# Bouton "Mot de passe oublié"
forgot_password_button = ctk.CTkButton(interface_de_connexion, text="Mot de passe oublié", command=forgot_password)
forgot_password_button.pack(pady=25, padx=12)

# Lancement de la boucle principale
interface_de_connexion.mainloop()
