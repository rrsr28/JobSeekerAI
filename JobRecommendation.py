# Importing the Libraries

from flask import Flask, render_template, request

import ast
import webbrowser
import numpy as np
import pandas as pd
import seaborn as sns
import mysql.connector
from scipy import stats
from ast import literal_eval
import matplotlib.pyplot as plt
from sklearn.metrics.pairwise import linear_kernel, cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer

import warnings; warnings.simplefilter('ignore')

app = Flask(__name__)

# ------------------------------------------------------------------------------

def getRecommendation(user_input):

    string = ""

    # Create a TF-IDF vectorizer
    vectorizer = TfidfVectorizer()

    # Fit and transform the skills in the skill database
    tfidf_matrix = vectorizer.fit_transform(Data['Key_Skills'])

    # Calculate cosine similarity between user's skills and job skills
    user_tfidf = vectorizer.transform([user_input])
    cosine_similarities = cosine_similarity(user_tfidf, tfidf_matrix).flatten()

    # Get indices of top job matches
    top_matches_indices = cosine_similarities.argsort()[-5:][::-1]

    # Get the top job recommendations
    top_job_recommendations = Data.iloc[top_matches_indices]['Job_Title']
    for i in top_job_recommendations:

        recommended_job = i
        string += "Recommended Job : " + i + "<br>"
        # Find the index of the recommended job in the skill database
        recommended_job_index = Data.index[Data['Job_Title'] == recommended_job][0]

        # Get the skills required for the recommended job
        recommended_skills = Data.loc[recommended_job_index, 'Key_Skills']

        # Assuming user_input contains the user's input skills
        user_skills = set(user_input.split(','))  # Convert to set for efficient comparison

        # Find the missing skills required for the recommended job
        missing_skills = [skill.strip() for skill in recommended_skills.split(',') if skill.strip() not in user_skills]

        if len(missing_skills) > 0:
            string = string + "Missing skills for the recommended job : " +  ' '.join(missing_skills) + "<br>"
        elif len(missing_skills) == 0:
            string = string + "You have all the skills required for the Recommended Job !" + "<br>"

        string += "<br>"

    return(string)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_input = request.form['skills']
        string = getRecommendation(user_input)
        return render_template('index.html', recommendations=string)
    return render_template('index.html')

if __name__ == '__main__':
    # Create the connection object
    myconn = mysql.connector.connect(host="localhost", user="root", passwd="$R#28@mah$qL", database="ajsr")
    print(myconn)

    # Creating the cursor object
    cur = myconn.cursor()

    query = "SELECT * FROM myTable"
    Data = pd.read_sql(query, myconn)

    app.run(debug=True)

