#!pip install pymysql
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy import insert
import pymysql
import mysql.connector as msql
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

def predictPlot():
  
  #Start MySQL connection
  db_connection_str = 'mysql+pymysql://sql4399167:VMAJwNlAix@sql4.freesqldatabase.com/sql4399167'
  db_connection = create_engine(db_connection_str)

  #Query userid, movieid for prediction
  history = pd.read_sql('select user_id,movie_id from user_history order by date_time desc limit 1', con=db_connection)
  user=history['user_id'].iloc[0]
  premovie=history['movie_id'].iloc[0]

  #Query necessary columns for first suggestion system
  plot_df = pd.read_sql('select movie_id,title,plot from movies', con=db_connection)
  plot_df['plot'].head(3)

  #Define a TF-IDF Vectorizer Object. Remove all english stop words such as 'the', 'a'
  tfidf = TfidfVectorizer(stop_words='english')

  #Replace NaN with an empty string
  plot_df['plot'] = plot_df['plot'].fillna('')

  #Construct the required TF-IDF matrix by fitting and transforming the data
  tfidf_matrix = tfidf.fit_transform(plot_df['plot'])

  #Output the shape of tfidf_matrix
  tfidf_matrix.shape

  #Array mapping from feature integer indices to feature name.
  tfidf.get_feature_names()[5:15]

  # Compute the cosine similarity matrix
  cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

  cosine_sim.shape

  cosine_sim[1]

  #Construct a reverse map of indices and movie titles
  indices = pd.Series(plot_df.index, index=plot_df['movie_id']).drop_duplicates()

  indices[:10]

  # Function that takes in movie title as input and outputs most similar movies
  def get_recommendations(title, cosine_sim=cosine_sim):
      # Get the index of the movie that matches the title
      idx = indices[title]

      # Get the pairwsie similarity scores of all movies with that movie
      sim_scores = list(enumerate(cosine_sim[idx]))

      # Sort the movies based on the similarity scores
      sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

      # Get the scores of the 10 most similar movies
      sim_scores = sim_scores[1:11]

      # Get the movie indices
      movie_indices = [i[0] for i in sim_scores]

      # Return the top 10 most similar movies
      return plot_df['movie_id'].iloc[movie_indices]

  sug_movie2 = get_recommendations(premovie)
  sug_movie2.head()

  #Update user_predictions
  mydb = msql.connect(
    host="sql4.freesqldatabase.com",
    user="sql4399167",
    password="VMAJwNlAix",
    database="sql4399167"
  )

  mycursor = mydb.cursor()


  smovieid1 = sug_movie2.iloc[0]
  smovieid2 = sug_movie2.iloc[1]

  sql = "UPDATE user_predictions SET sg_movie_id_2 = %s, sg_movie_id_3 = %s WHERE user_id = %s"
  val = (str(smovieid1),str(smovieid2),str(user))
  mycursor.execute(sql,val)

  mydb.commit()
  print("Recommendations updated for user ",user)