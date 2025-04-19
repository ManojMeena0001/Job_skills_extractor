# 🛠️ Job Skills Extractor

An intelligent tool to automatically extract and categorize skills from job descriptions using Natural Language Processing (NLP). Perfect for job seekers, recruiters, and data scientists looking to analyze job postings and extract essential information.

---

## 📚 Table of Contents

- [📌 Project Summary](#-project-summary)
- [🎯 Features](#-features)
- [📂 Folder Structure](#-folder-structure)
- [⚙️ Setup & Installation](#️-setup--installation)
- [▶️ How to Run](#️-how-to-run)
- [🧐 How the Project Works](#-how-the-project-works)
- [📸 Screenshots (Optional)](#-screenshots-optional)
- [🛠️ Tech Stack](#️-tech-stack)
- [📬 Contact Info](#-contact-info)
- [🙌 Contribution](#-contribution)
- [📄 License](#-license)

---

## 📌 Project Summary

**Job Skills Extractor** is a Streamlit-powered web application that helps users analyze job descriptions by identifying and categorizing relevant skills. Whether you're tailoring a resume, analyzing job market trends, or building HR tools, this project offers a foundational skill extraction engine.

---

## 🎯 Features

- ✅ Paste any job description and extract skills automatically.
- ✅ Categorizes extracted skills into relevant categories.
- ✅ Easy-to-use interface built with Streamlit.
- ✅ Clean and modular Python codebase.
- ✅ Ready for extension into ATS (Applicant Tracking System) tools or HR analytics platforms.

---

## 📂 Folder Structure

```
Job_skills_extractor/
├── .streamlit/               # Streamlit configuration
├── attached_assets/          # Images or assets for the UI
├── data/                     # Skill list or job data
├── app.py                    # Main Streamlit app
├── preprocessing.py          # Text cleaning and preprocessing
├── skill_extractor.py        # Skill extraction logic
├── skill_categorizer.py      # Categorizing extracted skills
├── utils.py                  # Utility/helper functions
├── generated-icon.png        # App icon
├── pyproject.toml            # Python dependencies & metadata
├── replit.nix                # Replit environment file
└── uv.lock                   # Locked dependency versions
```

---

## ⚙️ Setup & Installation

Follow the steps below to run the project on your local machine.

### 1. Clone the repository

```bash
git clone https://github.com/ManojMeena0001/Job_skills_extractor.git
cd Job_skills_extractor
```

### 2. Create a Virtual Environment (Recommended)

```bash
python -m venv venv
```

Activate it:

- On Windows:
  ```bash
  venv\Scripts\activate
  ```
- On Mac/Linux:
  ```bash
  source venv/bin/activate
  ```

### 3. Install Dependencies

If a `requirements.txt` file is available, run:

```bash
pip install -r requirements.txt
```

If not, install manually using the dependencies defined in `pyproject.toml`:

```bash
pip install streamlit pandas nltk
```

You may also need to download NLTK resources:

```python
import nltk
nltk.download('punkt')
nltk.download('stopwords')
```

---

## ▶️ How to Run

To launch the web application:

```bash
streamlit run app.py
```

You will see a link like `http://localhost:8501` in the terminal. Open it in your browser to use the app.

---

## 🧐 How the Project Works

### Step 1: Input Job Description

The user pastes a job description in the input field of the app interface.

### Step 2: Preprocessing

The input text is cleaned using `preprocessing.py` which includes:
- Lowercasing
- Removing special characters
- Tokenization
- Removing stopwords

### Step 3: Skill Extraction

Using `skill_extractor.py`, the system compares preprocessed tokens against a predefined skill list to extract relevant matches.

### Step 4: Skill Categorization

`skill_categorizer.py` takes the extracted skills and organizes them into categories like:
- Programming Languages
- Soft Skills
- Tools/Technologies
- Frameworks

### Step 5: Output

The results are displayed on the UI. Users get a categorized list of skills from the job description.

---

## 📸 Screenshots (Optional)

You can insert interface images here to make the project visually informative.

```
![Home Page](attached_assets/homepage.png)
![Result Page](attached_assets/results.png)
```

*Note: Save your screenshots inside the `attached_assets` folder and update paths above accordingly.*

---

## 🛠️ Tech Stack

| Tool/Library     | Purpose                            |
|------------------|-------------------------------------|
| Python           | Core programming language           |
| Streamlit        | Web application framework           |
| NLTK             | Natural Language Processing         |
| pandas           | Data manipulation                   |
| Git & GitHub     | Version control & collaboration     |

---

## 📬 Contact Info

**Developer**: Manoj Meena  
**Email**: manojofficialmail689@gmail.com  
**GitHub**: [https://github.com/ManojMeena0001](https://github.com/ManojMeena0001)

---

## 🙌 Contribution

Feel free to contribute by:
- Forking this repository
- Making your improvements
- Submitting a pull request

Suggestions, bug reports, and feature requests are welcome!

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

🌟 **If you like this project, please consider starring the repository!**

