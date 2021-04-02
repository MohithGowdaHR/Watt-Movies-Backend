#!pip install pymysql
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy import insert
import pymysql
import mysql.connector as msql

def predictRatings():
  
  #Start MySQL connection
  db_connection_str = 'mysql+pymysql://sql4399167:VMAJwNlAix@sql4.freesqldatabase.com/sql4399167'
  db_connection = create_engine(db_connection_str)



  #Get number of clients for insertion
  client_count = pd.read_sql('select count(*) as count from user_predictions', con=db_connection)
  clients_pred = client_count['count'].mean()
  client_max = pd.read_sql('select count(*) as count from user', con=db_connection)
  total_clients = client_max['count'].mean()
  #print(clients_pred)
  #print(total_clients)

  if (total_clients > clients_pred):
      #Query necessary columns for first suggestion system
      vote_df = pd.read_sql('select movie_id,user_rate,vote_count from movies', con=db_connection)
      vote_df.head(3)

      # Calculate mean of vote average column
      C = vote_df['user_rate'].mean()
      #print(C)

      # Calculate the minimum number of votes required to be in the chart, m
      m = vote_df['vote_count'].quantile(0.80)
      #print(m)

      # Filter out all qualified movies into a new DataFrame
      q_movies = vote_df.copy().loc[vote_df['vote_count'] >= m]
      q_movies.shape

      # Function that computes the weighted rating of each movie
      def weighted_rating(x, m=m, C=C):
          v = x['vote_count']
          R = x['user_rate']
          # Calculation based on the IMDB formula
          return (v/(v+m) * R) + (m/(m+v) * C)

      # Define a new feature 'score' and calculate its value with `weighted_rating()`
      q_movies['score'] = q_movies.apply(weighted_rating, axis=1)

      #Sort movies based on score calculated above
      q_movies = q_movies.sort_values('score', ascending=False)

      #Print the top 15 movies
      q_movies[['movie_id', 'score']].head(12)

      # Filter only movies with rate >= 8
      sug_movies1 = q_movies.copy().loc[q_movies['score'] >= 8]
      sug_movies1.head(10)
      
      #get random movie from top list
      suggested_movie1=sug_movies1.sample()['movie_id'].mean()
      #print(suggested_movie1)

      #Insert into new user_predictions
      mydb = msql.connect(
        host="sql4.freesqldatabase.com",
        user="sql4399167",
        password="VMAJwNlAix",
        database="sql4399167"
      )

      mycursor = mydb.cursor()

      sql = "INSERT INTO user_predictions (user_id, sg_movie_id_1) VALUES (%s, %s)"
      val = (str(clients_pred+1), str(suggested_movie1))
      mycursor.execute(sql, val)

      mydb.commit()
      print(mycursor.rowcount, "record inserted.")
  else:
    print("No new suggestions necessary.")
  

#predictRatings()