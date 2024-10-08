import os
from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip
import webbrowser
import json

# Change file destination
FILE_PATH = "data.json"


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = password_letters + password_symbols + password_numbers
    shuffle(password_list)

    password = "".join(password_list)

    password_entry.delete(0, END)
    password_entry.insert(0, password)
    pyperclip.copy(password)

    # print(f"Your password is: {password}")


# ---------------------------- SAVE PASSWORD ------------------------------- #

def save_password():
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    new_data = {
        website: {
            "email": email,
            "password": password,
        }
    }

    # You can use '' or 0 to define a error, or len() to capture a limit.
    if website == '' or email == '' or len(password) == 0:
        messagebox.showinfo(title="Error", message="Please fill all fields")

    else:
        try:
            with open(FILE_PATH, "r") as data_file:
                # Reading old data
                data = json.load(data_file)
        except FileNotFoundError:
            with open(FILE_PATH, "w") as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            # Updating old data with new data
            data.update(new_data)

            with open(FILE_PATH, "w") as data_file:
                # Saving updated data
                json.dump(data, data_file, indent=4)
        finally:
            website_entry.delete(0, END)
            password_entry.delete(0, END)


def search_password():
    website = website_entry.get()
    try:
        with open(FILE_PATH) as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showerror(title="Error", message="Data file was not found.")
    else:
        if website in data:
            email = data[website]["email"]
            password = data[website]["password"]
            messagebox.showinfo(title="Search", message=f"Email: {email}\nPassword: {password}")

        else:
            messagebox.showerror(title="Error", message=f"No details for {website} exist.")


def open_document():
    try:
        webbrowser.open('file://' + os.path.realpath(FILE_PATH))
    except webbrowser.Error:
        messagebox.showerror(title="Error", message="File not found.")


# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title('Password Manager')
window.iconbitmap(default='favicon.ico')
window.config(padx=50, pady=50)
window.resizable(width=False, height=False)

# Canvas IMG
canvas = Canvas(width=200, height=200)

mypass_img = PhotoImage(file='logo.png')
canvas.create_image(100, 100, image=mypass_img)
canvas.grid(row=0, column=1)

# Website Entry
website_label = Label(text='Website:')
website_label.grid(row=1, column=0)
website_label.config(font=('Arial', 8))

website_entry = Entry(width=33)
website_entry.grid(row=1, column=1)
website_entry.focus()

website_button = Button(text='  Search  ', command=search_password)
website_button.grid(row=1, column=2)

# Email Entry
email_label = Label(text='Email/Username:')
email_label.grid(row=2, column=0)
email_label.config(font=('Arial', 8))

email_entry = Entry(width=43)
email_entry.grid(row=2, column=1, columnspan=2)
email_entry.insert(0, 'email123@test.com')  # Can change email to most used for efficiency

# Password Entry & Generate
password_label = Label(text='Password:')
password_label.grid(row=3, column=0)
password_label.config(font=('Arial', 8))

password_entry = Entry(width=33)
password_entry.grid(row=3, column=1)

generate_button = Button(text='Generate', command=generate_password)
generate_button.grid(row=3, column=2)

# Save Entries Button

add_button = Button(text='Add', command=save_password)
add_button.config(width=36)
add_button.grid(row=4, column=1, columnspan=2)

# Open Document Button

exit_button = Button(text='Open Document', command=open_document)
exit_button.config(width=36)
exit_button.grid(row=5, column=1, columnspan=2)

# Exit Button

exit_button = Button(text='Exit', command=window.destroy)
exit_button.config(width=36)
exit_button.grid(row=6, column=1, columnspan=2)

window.mainloop()
