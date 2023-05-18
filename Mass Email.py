import pandas as pd
import csv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import tkinter as tk
from tkinter import messagebox
from tkinter import *
from tkinter import filedialog

# SMTP Server
smtp_server = 'smtp-relay.sendinblue.com'
smtp_port = 587
smtp_username = 'prithvi.analogica@gmail.com'
smtp_password = 'hUasxH4cj2POGqET'

# Connect to the SMTP server
smtp_connection = smtplib.SMTP(smtp_server, smtp_port)
smtp_connection.starttls()
smtp_connection.login(smtp_username, smtp_password)


def browse_file():
    # Allow the user to choose a file from a folder and set the file path in the entry field
    file_path = filedialog.askopenfilename()
    filepath_entry.insert(0, file_path)

def send_emails():
    # Get the sender email and email subject from the entry fields
    sender_email = sender_entry.get()
    email_subject = subject_entry.get()
    
    # Get the file path from the entry field
    file_path = filepath_entry.get()
    
    name_header = name_header_entry.get()
    mail_header = mail_header_entry.get()
    
    # Check the file extension
    if file_path.endswith('.csv'):
        # Read the CSV file into a Pandas DataFrame
        df = pd.read_csv(file_path, encoding='ISO-8859-1')
    elif file_path.endswith('.xlsx'):
        # Read the Excel file into a Pandas DataFrame
        df = pd.read_excel(file_path, engine='openpyxl')
    else:
        # Show an error message if the file is not a CSV or Excel file
        messagebox.showerror("Error", "Invalid file format. Please select a CSV or Excel file.")
    
    # Extract the Name and Email columns as lists
    names = df[f'{name_header}'].tolist()
    emails = df[f'{mail_header}'].tolist()
    
    # Iterate over the list of contacts
    for name, email in zip(names, emails):
        # Create the email message
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = email
        msg['Subject'] = email_subject
        
        # Set the email body
        email_body = body_text.get('1.0', tk.END).replace('{name}', name)
        msg.attach(MIMEText(email_body, 'plain'))

        # Send the email
        smtp_connection.sendmail(sender_email, email, msg.as_string())
    
    # Show a message box indicating the emails have been sent
    tk.messagebox.showinfo("Emails sent", "Emails have been sent!")


# Initialize the tkinter window
window = tk.Tk()
window.title("Certisured Email Sender")

headlabelfont = ("Noto Sans CJK TC", 15, 'bold')
labelfont = ('Garamond', 14)
entryfont = ('Garamond', 12)

# maximize the main window
window.state('zoomed')

lf_bg = 'MediumSpringGreen'

tk.Label(window, text="MESSAGE SENDER", font=headlabelfont, bg='SpringGreen').pack(side=TOP, fill=X)

Frame(window, bg=lf_bg)

# File path label and entry field
filepath_frame = Frame(window, bg=lf_bg)
filepath_frame.pack(side=TOP, padx=5, pady=5, fill=X)

filepath_label = tk.Label(filepath_frame, text="File path:", width=20, font=labelfont, bg=lf_bg)
filepath_label.pack(side=LEFT)

filepath_entry = tk.Entry(filepath_frame, width=90, font=entryfont)
filepath_entry.pack(side=LEFT, padx=5, pady=5, fill=X)

# Browse button
browse_button = tk.Button(filepath_frame, text="Browse", command=lambda: browse_file(), font=labelfont)
browse_button.pack(side=LEFT, padx=5, pady=5)


#Header names
_frame = Frame(window, bg="#008000")
_frame.pack(side=TOP, padx=5, pady=5, fill=X)

name_header_frame = Frame(window, bg=lf_bg)
name_header_frame.pack(side=TOP, padx=5, pady=5, fill=X)

name_header_label = tk.Label(name_header_frame, text="Name:", width=20, font=labelfont, bg=lf_bg)
name_header_label.pack(side=LEFT)

name_header_entry = tk.Entry(name_header_frame, width=100, font=entryfont)
name_header_entry.pack(side=LEFT, padx=5, pady=5, fill=X)

mail_header_frame = Frame(window, bg=lf_bg)
mail_header_frame.pack(side=TOP, padx=5, pady=5, fill=X)

mail_header_label = tk.Label(mail_header_frame, text="Mail:", width=20, font=labelfont, bg=lf_bg)
mail_header_label.pack(side=LEFT)

mail_header_entry = tk.Entry(mail_header_frame, width=100, font=entryfont)
mail_header_entry.pack(side=LEFT, padx=5, pady=5, fill=X)

_frame = Frame(window, bg="#008000")
_frame.pack(side=TOP, padx=5, pady=5, fill=X)


# Sender email label and entry field
sender_frame = Frame(window, bg=lf_bg)
sender_frame.pack(side=TOP, padx=5, pady=5, fill=X)

sender_label = tk.Label(sender_frame, text="Sender email:", width=20, font=labelfont, bg=lf_bg)
sender_label.pack(side=LEFT)

sender_entry = tk.Entry(sender_frame, width=100, font=entryfont)
sender_entry.pack(side=LEFT, padx=5, pady=5, fill=X)
#sender_entry.insert(0, 'sameerpasha658@gmail.com')


# Email subject label and entry field
subject_frame = Frame(window, bg=lf_bg)
subject_frame.pack(side=TOP, padx=5, pady=5, fill=X)

subject_label = tk.Label(subject_frame, text="Email subject:", width=20, font=labelfont, bg=lf_bg)
subject_label.pack(side=LEFT)

subject_entry = tk.Entry(subject_frame, width=100, font=entryfont)
subject_entry.pack(side=LEFT, padx=5, pady=5, fill=X)
#subject_entry.insert(0, 'I love Certisured')


# Email body label and text area
body_frame = Frame(window, bg=lf_bg)
body_frame.pack(side=TOP, padx=5, pady=5, fill=X)

body_label = tk.Label(body_frame, text="Email body:",width=19, font=labelfont, bg=lf_bg)
body_label.grid(row=0, column=0, padx=5, pady=5, sticky=W)

body_text = tk.Text(body_frame, width=130, height=20, font=entryfont)
body_text.grid(row=0, column=1, padx=5, pady=5, sticky=W)
body_text.insert(tk.END, 'Hello {name}, this is from Certisured')


# Create a frame widget for the buttons
button_frame = tk.Frame(window)
button_frame.pack(side=tk.BOTTOM, pady=10)

# Send button
send_button = tk.Button(button_frame, text="Send", command=lambda: send_emails(), width=15, font=labelfont)
send_button.grid(row=0, column=0, padx=5, pady=5, sticky=W)

def clear_fields():
    # Clear the sender email, email subject, and email body fields
    filepath_entry.delete(0, tk.END)
    name_header_entry.delete(0, tk.END)
    mail_header_entry.delete(0, tk.END)
    sender_entry.delete(0, tk.END)
    subject_entry.delete(0, tk.END)
    body_text.delete('1.0', tk.END)
    
# Clear button
clear_button = tk.Button(button_frame, text="Clear", command=lambda: clear_fields(), width=15, font=labelfont)
clear_button.grid(row=0, column=1, padx=5, pady=5, sticky=E)

# Run the tkinter event loop
window.mainloop()