from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json
from json.decoder import JSONDecodeError

BG = "black"
LABEL_BG = "black"
LABEL_FG = "white"


# -------------------------SEARCH WEBSITES IN DATA.JSON-------------------------------#
def do_search():
    website_to_search = website_entry.get()
    try:
        with open("data.json", "r") as file:
            file_data = json.load(file)
    except FileNotFoundError:
        messagebox.showinfo(title="No directory found", message="Please add passwords in order to access them.")
    else:
        if website_to_search in file_data:
            email = file_data[website_to_search]["Email/Username"]
            password = file_data[website_to_search]["Password"]
            messagebox.showinfo(title=website_to_search, message=f"Email/Username: {email}\nPassword: {password}")
        else:
            messagebox.showinfo(title="OOPS", message=f"'{website_to_search}' ==> such entry doesn't exist")


# -------------------------PASSWORD MANAGER-------------------------------#
def generate_password():
    """generates a strong random password of a random length"""
    letters = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u",
               "v", "w", "x", "y", "z", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P",
               "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]

    symbols = ["!", "@", "#", "*", "-", "%", "^", "&"]

    password_letters = [random.choice(letters) for _ in range(random.randint(6, 8))]

    # Below to ensure that at least one capitalized letter
    password_letters.append(random.choice(letters[27:]))
    password_symbols = [random.choice(symbols) for _ in range(random.randint(4, 6))]
    password_numbers = [str(random.randint(0, 9)) for _ in range(random.randint(3, 4))]

    password_list = password_letters + password_symbols + password_numbers

    random.shuffle(password_list)

    password = "".join(password_list)

    password_entry.insert(0, password)
    pyperclip.copy(password)


# -------------------------ADDING INFO TO TEXT FILE AND MESSAGE BOX OUTPUTS-------------------------------#
def add_to_file():
    """adds required information in data.json if it not exists it'll make data.json and adds info"""

    # Adding data in data.json only if least website and username are provided
    if (website_entry.get() != "") and (email_entry.get() != ""):
        data = {website_entry.get():
            {
                "Email/Username": email_entry.get(),
                "Password": password_entry.get()
            }
        }
        try:
            with open("data.json", "r") as file:
                file_data = json.load(file)
        except FileNotFoundError:
            with open("data.json", "w") as file:
                json.dump(data, file, indent=4)
        except JSONDecodeError:
            with open("data.json", "w") as file:
                json.dump(data, file, indent=4)
        else:
            file_data.update(data)
            with open("data.json", "w") as file:
                json.dump(file_data, file, indent=4)
        finally:
            website_entry.delete(0, END)
            password_entry.delete(0, END)


# -------------------------UI-------------------------------#
window = Tk()
window.title("Password Generator")
window.config(padx=100, pady=100, bg=BG)

# Creating canvas
canvas = Canvas(width=200, height=200, bg=BG, highlightthickness=0)
logo = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo)
canvas.grid(column=1, row=0)

# Creating labels
website_label = Label(text="Website:", bg=LABEL_BG, fg=LABEL_FG)
email_label = Label(text="Email/Username:", bg=LABEL_BG, fg=LABEL_FG)
password_label = Label(text="Password:", bg=LABEL_BG, fg=LABEL_FG)

website_label.grid(column=0, row=1)
email_label.grid(column=0, row=2)
password_label.grid(column=0, row=3)

# Creating entries
website_entry = Entry(width=35)
email_entry = Entry(width=35)
password_entry = Entry(width=35)

website_entry.grid(column=1, row=1)
website_entry.focus()
email_entry.grid(column=1, row=2)
# email_entry.insert(0, "Your Email")
password_entry.grid(column=1, row=3)

# Creating buttons
generate_button = Button(text="Generate Password", command=generate_password)
generate_button.grid(column=1, row=4)

add_button = Button(text="Add", padx=10, pady=10, command=add_to_file, bg="green")
add_button.grid(column=2, row=2, rowspan=2)

search_button = Button(text="Search", command=do_search, bg="lightgreen")
search_button.grid(column=2, row=1)

window.mainloop()
