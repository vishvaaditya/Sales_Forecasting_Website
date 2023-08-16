#Importing the required packages
import logging
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_pymongo import pymongo
from flask import Flask, request,render_template,jsonify,make_response,session
from flask_cors import CORS,cross_origin
import jwt
import datetime
from functools import wraps

#from app import application.

import pandas as pd
import statsmodels.api as sma
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_absolute_error,mean_squared_error,mean_absolute_percentage_error
import numpy as np

import threading

# Creating a FLASK APP

#web_app = Flask(__name__, template_folder="template")  # Initialize Flask App
#CORS(web_app)

# Connecting the Database and collection of MongodbAtlas using pymongo

con_string = "mongodb+srv://Vishvaaditya:Vishva11@cluster0.hjnojmy.mongodb.net/?retryWrites=true&w=majority"

client = pymongo.MongoClient(con_string)

db = client.get_database('signupdb')

user_collection = pymongo.collection.Collection(db, 'signupusers') #(<database_name>,"<collection_name>")
print("MongoDB connected Successfully")


db2 = client['filedb']

#file_collection= pymongo.collection.Collection(db2, 'sales1') #(<database_name>,"<collection_name>")
#print("second database connected successfully")

# Configuration for authentication




# Backend API routes for ARIMA

def project_api_routes(endpoints):
    @endpoints.route('/file_upload',methods=['POST'])
    def file_upload():
    #Getting file from angular server and storing it in a local variable
      req = request.form
      file1 = request.files.get('file')
      filename = file1.filename
      collection_name = filename.split('.')[0]  # Use filename as collection name

    # Create a collection for the CSV file
      collection = db2[collection_name]
      sales= pd.read_csv(file1)
      records = sales.to_dict('records') 
      collection.insert_many(records)
      
           

    # checking for NAN values 
      
      sales.isna().sum() 

    #Filling null value using mean/mode method as it has only one null value
      def value_mode(inputs):
       mode = sales[inputs].mode()[0]
       sales[inputs] =sales[inputs].fillna(mode) 
      for data in sales:
        value_mode(data)
      print(sales.isnull().sum())

      sales2 = sales
      sales2.head(10)

    # Converting sales column type
      sales2['sales'] = sales2['sales'].astype('int64')
      print(sales2.info())  

    # Converting date column to datetime type
      sales2['Date'] = pd.to_datetime(sales2['Date'])
      sales2['Date']= sales2['Date'].dt.to_period("M")
      sales3 = sales2.groupby('Date').sum().reset_index()
      sales3  
      sales3['Date'] = sales3['Date'].dt.to_timestamp()
      sales3 = pd.DataFrame(sales3).set_index('Date')
      print(sales3.head(40))
    
      # To make the series stationary(using log transformation)
      sales_log = np.log(sales3)


      
       

      # perform Augmented Dickey- fuller test:
      # if ADF test is null hypothesis = non - stationary or if p- value < 5% it is stationary
      from statsmodels.tsa.stattools import adfuller

      adfuller_test = adfuller(sales_log, autolag='AIC')
      print(f' ADF statistic:{adfuller_test[0]}')
      print(f' P-value:{adfuller_test[1]}')
      

      # Perform Arima model 
      from statsmodels.tsa.arima.model import ARIMA
      

      model = ARIMA(sales_log, order=(2,1,6))
      result_model = model.fit()
      


      # reverse scaling the data

      unscaled_sales = np.exp(sales_log)
      print(unscaled_sales)

      unscaled_prediction = np.exp(result_model.fittedvalues)
      print(unscaled_prediction)

      pred=result_model.forecast(steps = 20)
      print(pred)

      unscaled_forecast = np.exp(pred)
      print(unscaled_forecast)


      # Sales data with Forescast data
      import matplotlib.pyplot as plt
      import uuid

# Generate a unique filename for the image
      #image_filename = "output.png"

      unscaled_forecast.plot(legend="True", label="Forecasted Result", figsize=(10, 6))
      unscaled_prediction.plot(legend="True", label="Predicted Result")
      plt.title("Sales Forecast", fontsize=16, fontweight='bold')
      plt.legend(loc="best")
      plt.xlabel("Time")
      plt.ylabel("Sales")
      plt.grid(True, linestyle='--', alpha=0.4)

# Save the image with the unique filename
      plt.savefig("H:/Final_year_project/digiverzapp/flaskread/static/output.png")

# Print the image filename
      #print(image_filename)
      
      MSE=np.sqrt(mean_squared_error(sales3,unscaled_prediction))
      print(MSE)

      MAE = np.sqrt(mean_absolute_error(sales3,unscaled_prediction))
      print(MAE)

      MAPE = np.sqrt(mean_absolute_percentage_error(sales3,unscaled_prediction))
      print(MAPE)
      
      result = [MSE,MAE,MAPE,"H:/Final_year_project/digiverzapp/flaskread/static/output.png"]
      print(result)

      




 

    


      return render_template("predictions.html",result=result)
 
     
   # Mongodb API connection for Signup users    
    @endpoints.route('/signup', methods=['POST'])
    @cross_origin()
    def signup():
        
        resp = {}
        try:
            
            name = request.json.get('Name')
            password = generate_password_hash(request.json.get('Password'))
            user = user_collection.find_one({'Name':name})

            if user:
                return jsonify({'success': False,'message':'Name already exists'}), 409
            
            user_id = user_collection.insert_one({'Name': name, 'Password': password}).inserted_id

            return jsonify({'success': True, 'user_id': str(user_id)}), 201

            user_collection.insert_one({'Name': name, 'Password':password})   
            #return jsonify({'Name': name, 'Password': password})         
            print("User Data Stored Successfully in the Database.")
            status = {
                "statusCode":"200",
                "statusMessage":"User Data Stored Successfully in the Database."
            }
        except Exception as e:
            print(e)
            status = {
                "statusCode":"400",
                "statusMessage":str(e)
            }
        resp["status"] =status
        return resp
 
    @endpoints.route('/login',methods=['POST'])
    @cross_origin()
    def login():
      
            name = request.json.get('Name')
            password = request.json.get('Password')
            signupusers = user_collection.find_one({'Name':name})

            if signupusers and check_password_hash(signupusers['Password'], password):
              session["user_collection"] = name
              return make_response({'success': True}), 200

            return make_response({'success': False}, 401,{'WWW-Authenticate': 'Basic realm="Login required"'})
    @endpoints.route('/check_login_status',methods=['GET'])
    def check_login_status():
       if 'user_collection' in session:
         return jsonify({'isLoggedIn': True}), 200
       else:
         return jsonify({'isLoggedIn': False}), 200     
        
    return endpoints


#if __name__ == "__main__":
  #  web_app.run(debug=True)
   

   