import pandas as pd 
import streamlit as st 
import numpy as np 
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import mpl_toolkits
from datetime import datetime
import seaborn as sn

from sklearn.ensemble import RandomForestRegressor
from sklearn.datasets import make_regression
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_squared_error
from sklearn.metrics import accuracy_score

st.title('Waka Waka Seattle Home Prices')

st.write("""
# Home Prices Predicted Using Machine Learning
""")

#read and display csv
@st.cache 
def fetch_data(): 
    df = pd.read_csv('clean1.csv')

    return df


#Select and split X and y
def preprocessing(df):
    X = df.iloc[:,1:].values
    y = df.iloc[:,0].values

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    return X_train, X_test, y_train, y_test

# Train the Random Forest model
@st.cache(allow_output_mutation=True)
def randomForest(X_train, X_test, y_train, y_test):
    regressor = RandomForestRegressor(n_estimators = 100, random_state=42)
    regressor.fit(X_train,y_train)
    y_predict = regressor.predict(X_test)
    score = r2_score(y_test, y_predict)*100

    return score ,regressor

#User input for the model
def user_input():
    bedrooms = st.slider("Bedrooms: ", 1,15)
    bathrooms = st.text_input("Bathrooms: ")
    sqft_living = st.text_input("Square Feet: ")
    sqft_lot = st.text_input("Lot Size: ")
    floors = st.text_input("Number Of Floors: ")
    waterfront = st.text_input("Waterfront? For Yes type '1',  For No type '0': ")
    view = st.slider("View (A higher score will mean a better view) : ", 0,4)
    condition = st.slider("House Condition (A higher score will mean a better condition): ", 1,5)
    yr_built = st.text_input("Year Built: ")
    yr_reno = st.text_input("A Renovated Property? For Yes type '1',  For No type '0': ")
    zipcode = st.text_input("Zipcode (5 digit): ")
    year_sold = st.text_input("Year Sold: ")
    month_sold = st.slider("Month Sold: ", 1,12)
   
    user_input_prediction = np.array([bedrooms,bathrooms,sqft_living,
    sqft_lot,floors,waterfront,view,condition,yr_built,yr_reno,zipcode,year_sold,month_sold]).reshape(1,-1)
    
    return(user_input_prediction)





def main():
    data = fetch_data()
    X_train, X_test, y_train, y_test = preprocessing(data)

    if st.checkbox("Show the Data We Used"):
        st.subheader("Home Sales From 2014 to 2015")
        st.write(data.head())

    ml_model = st.sidebar.selectbox("Choose a Model to Predict Home Prices", ["Random Forest", "Coming Soon"])

    if(ml_model == "Random Forest"):
        score, regressor= randomForest(X_train, X_test, y_train, y_test)
        st.text("Accuracy of Random Forest model is: ")
        st.write(round(score,2),"%")

        try:
            if(st.checkbox("Start a Search")):
                user_input_prediction = user_input()
                pred = regressor.predict(user_input_prediction)
                st.write('The Predicted Home Price is: ', pred)
        except:
            pass


        




if __name__ == "__main__":
	main()