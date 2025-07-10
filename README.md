# 📚 Book Recommendation System

This is a Book Recommendation System built with Python. It uses collaborative filtering based on user ratings and displays results via a Tkinter GUI interface.

---

## 🧠 Project Overview

The system takes a book name as input and recommends 5 similar books. These recommendations are based on user rating patterns using **cosine similarity**. The results are shown with book titles and cover images in a GUI window.

---

## 🗂️ Dataset

Three CSV files are used in this project:
Link to kaggle datset : https://www.kaggle.com/datasets/arashnic/book-recommendation-dataset

- `Books.csv` — Metadata of books (title, image URL, etc.)
- `Users.csv` — User demographic information
- `Ratings.csv` — User ratings for books

---

## 📊 Data Preprocessing (Before GUI Integration)

Before loading into the GUI, we performed the following analysis in pandas:

```python
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

books = pd.read_csv('Books.csv')
users = pd.read_csv('Users.csv')
ratings = pd.read_csv('Ratings.csv')

# Merge ratings with book titles
ratings_with_name = ratings.merge(books, on='ISBN')

# Filter users who have rated more than 200 books
x = ratings_with_name.groupby('User-ID').count()['Book-Rating'] > 200
good_users = x[x].index
filtered_rating = ratings_with_name[ratings_with_name['User-ID'].isin(good_users)]

# Filter books with at least 50 ratings
y = filtered_rating.groupby('Book-Title')['Book-Rating'].count() >= 50
famous_books = y[y].index

# Create final pivot table
final_ratings = filtered_rating[filtered_rating['Book-Title'].isin(famous_books)]
pt = final_ratings.pivot_table(index='Book-Title', columns='User-ID', values='Book-Rating')
pt.fillna(0, inplace=True)

# Compute similarity scores
similarity_scores = cosine_similarity(pt)
```
## 📚 Recommendation Function (Console)
```python
def recommend(book_name):
    index = np.where(pt.index == book_name)[0][0]
    similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:6]
    for i in similar_items:
        print(pt.index[i[0]])
```
## 🖥️ GUI Integration
The GUI is built using Tkinter. It allows users to enter a book name and get 5 similar recommendations with cover images fetched from URLs.

## 🔑 Features
Book search bar

- Image and title display
- Option to filter by rating or publication date (checkboxes)
- Graceful fallback if image is unavailable
- Clean and modern UI

## 📦 Dependencies

```bash
pip install pandas numpy scikit-learn pillow requests
```

