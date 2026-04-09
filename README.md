<img width="1781" height="915" alt="image" src="https://github.com/user-attachments/assets/c63206ce-f548-4deb-ac77-f768426b8eaa" />


# 📺 Netflix‑Style TV Series Rating Graph  
A small Flask application that visualizes episode ratings for any TV series using data from the TMDb API.  
You enter a show title, the app fetches all seasons and episodes, and it renders an interactive line graph showing how ratings change across the series.

---

## 🚀 Features
- Search any TV series by title  
- Fetch season and episode data from TMDb  
- Plot episode ratings season‑by‑season  
- Hover tooltips with episode titles and rating values  
- Dark‑themed graph for a clean, modern look  
- Simple Flask backend + HTML/JS frontend  

---

## 📊 Example Output  
The app generates a graph like this for each series, showing rating trends across episodes and seasons.

<img width="1909" height="950" alt="image" src="https://github.com/user-attachments/assets/335df680-a9ac-48b3-abff-e69b5a796c07" />

---

## 🧩 How It Works
1. The user enters a series title.  
2. The backend queries TMDb’s `/search/tv` endpoint to get the series ID.  
3. It then fetches all seasons and their episodes.  
4. Episode ratings (`vote_average`) are extracted and grouped by season.  
5. The frontend renders the data as a line graph.

---

## 🛠️ Tech Stack
- **Python 3**  
- **Flask**  
- **TMDb API**  
- **Chart.js** for graph rendering  
- **HTML / CSS / JavaScript**

---

## 📦 Setup

### 1. Clone the repo
```bash
git clone <your-repo-url>
cd <project-folder>
```

### 2. Install dependencies
```bash
pip install flask
```

### 3. Add your TMDb API key  
Open the Python file and replace the placeholder key in `API_LIST`.

### 4. Run the app
```bash
python app.py
```

### 5. Open in browser  
```
http://127.0.0.1:5000
```

---

## 🗂️ Project Structure
```
.
├── app.py
├── templates/
│   ├── home.html
│   └── darkGraph.html
└── static/
    └── (optional JS/CSS files)
```

---

## 🔑 API Usage  
This project uses the following TMDb endpoints:

- `/3/search/tv` – find a series by title  
- `/3/tv/{series_id}` – fetch season metadata  
- `/3/tv/{series_id}/season/{season_number}` – fetch episodes + ratings  

You’ll need a free TMDb API key to run the project.

---

## 📌 Notes
- TMDb ratings are community‑driven and may differ from IMDb ratings.  
- Some older shows may have incomplete rating data.  
- Specials (Season 0) are ignored intentionally.

---

## 🧭 Future Improvements
- Add Netflix availability data  
- Add caching to reduce API calls  
- Add comparison mode (e.g., compare two shows)  
- Deploy to Render / Railway  


