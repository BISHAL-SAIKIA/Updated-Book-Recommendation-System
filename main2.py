import pandas as pd
from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
from io import BytesIO
import requests
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Load and preprocess data
df = pd.read_csv("pt.csv", index_col=0)
final = pd.read_csv("final.csv", index_col=0)

# Convert titles to lowercase
df.index = df.index.str.lower()
final['Book-Title'] = final['Book-Title'].str.lower()

# Compute similarity matrix
similarity = cosine_similarity(df.fillna(0))
similarity_df = pd.DataFrame(similarity, index=df.index, columns=df.index)

# GUI setup
root = Tk()
root.title("Book Recommendation System")
root.geometry("1250x700+200+100")
root.config(bg="#111119")
root.resizable(False, False)

class Request:
    def __init__(self, method, args):
        self.args = args
        self.method = method

inc = 0

def fetch_information(title, poster_url):
    global inc
    inc += 1

    if f'a{inc}' in text:
        text[f'a{inc}'].config(text=title)

    try:
        if poster_url and poster_url.startswith("http"):
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
            }
            response = requests.get(poster_url, headers=headers, timeout=5)
            response.raise_for_status()

            img_data = response.content
            img = Image.open(BytesIO(img_data))
            resized_image = img.resize((140, 200))
            photo = ImageTk.PhotoImage(resized_image)

            if f'b{inc}' in image:
                image[f'b{inc}'].config(image=photo)
                image[f'b{inc}'].image = photo
        else:
            print(f"No valid image URL for: {title}")
    except Exception as e:
        print(f"Failed to load image for: {title}. Error: {e}")

def get_image_url(df, book_title):
    match = df[df['Book-Title'] == book_title]
    if not match.empty:
        return match.iloc[0]['Image-URL-S']
    else:
        return "https://via.placeholder.com/140x200?text=No+Image"

def search():
    global inc
    inc = 0
    query = Search.get().strip().lower()

    if query not in df.index:
        messagebox.showinfo("Not Found", "Book not found in recommendations.")
        return

    try:
        similar_scores = similarity_df.loc[query]
        top_similar = similar_scores.sort_values(ascending=False)[1:6]

        for title in top_similar.index:
            poster = get_image_url(final, title)
            fetch_information(title.title(), poster)

        if check_var.get() or check_var2.get():
            frame11.place(x=160, y=600)
            frame22.place(x=360, y=600)
            frame33.place(x=560, y=600)
            frame44.place(x=760, y=600)
            frame55.place(x=960, y=600)
        else:
            frame11.place_forget()
            frame22.place_forget()
            frame33.place_forget()
            frame44.place_forget()
            frame55.place_forget()

    except Exception as e:
        messagebox.showerror("Error", str(e))

# UI images
icon_image = PhotoImage(file="Images/icon.png")
root.iconphoto(False, icon_image)

heading_image = PhotoImage(file="Images/background.png")
Label(root, image=heading_image, bg='#111119').place(x=-2, y=-2)

heading = Label(root, text="BOOK RECOMMENDATION", font=("Lato", 30, "bold"), fg="white", bg="#0099ff")
heading.place(x=410, y=90)

search_box = PhotoImage(file="Images/Rectangle 2.png")
Label(root, image=search_box, bg="#0099ff").place(x=300, y=155)

Search = StringVar()
search_entry = Entry(root, textvariable=Search, width=20, font=("Lato", 25), bg="white", fg="black", bd=0)
search_entry.place(x=415, y=172)

recommend_button_image = PhotoImage(file="Images/Search.png")
recommend_button = Button(root, image=recommend_button_image, bg="#0099ff", bd=0, activebackground="#252532", command=search)
recommend_button.place(x=860, y=169)


menu = Menu(root, tearoff=0)
check_var = BooleanVar()
menu.add_checkbutton(label="Published Date", variable=check_var)
check_var2 = BooleanVar()
menu.add_checkbutton(label="Rating", variable=check_var2)

logout_image = PhotoImage(file="Images/logout.png")
Button(root, image=logout_image, bg="#0099ff", cursor="hand2", command=lambda: root.destroy()).place(x=1150, y=20)

# Recommendation display frames
frames = [Frame(root, width=150, height=240, bg="white") for _ in range(5)]
for i, frame in enumerate(frames):
    frame.place(x=160 + i * 200, y=350)

text = {f'a{i+1}': Label(frames[i], text="Book Title", font=("Arial", 10), fg="green") for i in range(5)}
image = {f'b{i+1}': Label(frames[i]) for i in range(5)}

for i in range(5):
    text[f'a{i+1}'].place(x=10, y=4)
    image[f'b{i+1}'].place(x=3, y=30)

# Extra info frames
frames_extra = [Frame(root, width=150, height=50, bg="#e6e6e6") for _ in range(5)]


frame11, frame22, frame33, frame44, frame55 = frames_extra

root.mainloop()
