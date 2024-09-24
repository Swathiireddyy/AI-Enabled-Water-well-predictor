import streamlit as st
import numpy as np
import pandas as pd
import pickle
import requests
st.title("AI Water Well Predictor")
st.write("An AI water well predictor utilizes machine learning models to forecast groundwater levels, water quality, drilling techniques, and drilling duration based on geographical coordinates. By preprocessing and training with relevant data sources, it learns to correlate geographic features with well-related outcomes. The predictor offers a user-friendly interface for users to input coordinates and receive real-time predictions.")
#st.image(' https://wallpapercave.com/wp/wp10030354.jpg')
model=pickle.load(open('GW.pkl','rb'))
model2=pickle.load(open('GWQ.pkl','rb'))
model3=pickle.load(open('Rainfall.pkl','rb'))
#file_path = r"C:\Users\aksha\Downloads\dataset.csv"
import requests
#access_token = 'pk.eyJ1Ijoic3dhdGhpMTUiLCJhIjoiY2x2eXN4aW5yMmRraDJybnkzYnNoenhlMyJ9.YM6oe6xPMbj1YoEghpkMsQ'
def geocode_location(location_name, access_token):
    base_url = 'https://api.mapbox.com/geocoding/v5/mapbox.places'
    params = {
        'access_token': access_token,
        'limit': 1,  # Limit to one result
        'autocomplete': False,  # Disable autocomplete
        'bbox': '-180,-90,180,90',  # Restrict results to the whole world
        'types': 'place',  # Limit results to places
        'language': 'en',  # Language preference
        'query': location_name  # Location name to geocode
    }
    response = requests.get(base_url + '/{}.json'.format(location_name), params=params)
    if response.status_code == 200:
        data = response.json()
        if data['features']:
            # Extract latitude and longitude from the first feature in the response
            coordinates = data['features'][0]['geometry']['coordinates']
            return coordinates[1], coordinates[0]  # Latitude, Longitude
        else:
            return 0  # Handle no results found
    else:
        return None  # Handle request errors

# Example usage

  

# Read the CSV file into a DataFrame
#df = pd.read_csv(file_path)

# Display the DataFla
latitude=''
longitude=''
state=''
district=''


def login():
    st.title("Login")
    email = st.text_input("Email", key="login_email")  # Add unique key
    password = st.text_input("Password", type="password", key="login_password")  # Add unique key

    if st.button("Login"):
        # Perform authentication logic here
        if email == "example@example.com" and password == "password123":
            st.success("Login successful!")
            st.session_state.logged_in = True
            st.rerun()

def signup():
    st.title("Sign Up")

    name = st.text_input("Name", key="signup_name")  # Add unique key
    email = st.text_input("Email", key="signup_email")  # Add unique key
    create_password = st.text_input("Create Password", type="password", key="signup_create_password")  # Add unique key
    confirm_password = st.text_input("Confirm Password", type="password", key="signup_confirm_password")  # Add unique key

    if st.button("Sign Up"):
        if create_password != confirm_password:
            st.error("Passwords do not match. Please try again.")
        else:
            # Perform signup logic here
            st.success("Sign up successful! You can now log in.")
            st.session_state.logged_in = True
            st.rerun()

def predict_water_well(latitude, longitude):
    # Placeholder for AI prediction logic
    input = np.array([[latitude,longitude]]).astype(np.float64)
    prediction = model.predict(input)
    prediction2=model2.predict(input)
    op2=model3.predict(input)
    op1=np.array([op2])
    #st.write(op1[0])
    op=(np.sum(op1))/3
    op=round(op,2)
    #op3=(op+op1+op2)/3
    return prediction, prediction2, op



def prediction_page():
    st.success("Login successful!")
    st.title("Prediction")

    # Your prediction page content here
    st.write("Welcome to the prediction page!")
    st.write("Enter location name or co ordinates of the place")
    state=st.text_input("Enter location name",key="State_input")
    #district = st.text_input("Enter District",key="District_input")
    #value_to_find = district
    #value_to_find1= state

        # Use boolean indexing to find the row(s) where the value is located
        # Assuming you want to find the value in a specific column named "column_name"
        #filtered_df1 = df[df["State"] == value_to_find1]
    #filtered_df = df[df["District"] == value_to_find]
    #filtered_df1 = df[df["State"] == value_to_find1]
    if st.button("Submit"):
        if(state is not None):
            access_token = 'sk.eyJ1Ijoic3dhdGhpMTUiLCJhIjoiY2x2ejFzYmg0MHdkcjJrcGRvdTl6ZHh4eCJ9.BIXgNWRFgeYjbq74rHiCig'
            location_name = state
            coordinate=geocode_location(location_name, access_token)
            if(coordinate == 0):
                st.write("Please enter co ordinates")
            else:
                output,output1,output2=predict_water_well(coordinate[0], coordinate[1])
                #st.write("{}".format(coordinate[0]))
                #st.write("{}".format(coordinate[1]))
                if(output <= 50):
                    st.success('This area is suitable for water well construction.')
                else: 
                    st.success('This area is not suitable for water well construction.')
                st.success('Availability of ground water is : {} metres below ground water level(mbgl) .'.format(output))
                if(output2 < 0):
                    st.success('Due to weather patterns the ground water level might decrease by {} metres below ground water level(mbgl). '.format(output2))
                #st.success('{}'.format(output2))
                if(output1 == 1):
                    st.success('water is safe to drink.')
                else:
                    st.success('water is not safe to drink.') 
                st.success('Suggested Drilling Techniques:')  
                st.success('Auger Drilling: Takes 1-2 days to complete.')  
                st.success('Rotary Drilling: Takes 2-3 days to complete.') 
                st.success('Percussion Drilling: Takea 3-5 days to complete.')     
        else:
            st.warning('Please fill in location name')

    st.write("Or")
        # Check if the value is present in the DataFrame
    latitude = st.text_input("Enter Latitude", key="Latitude_input")
    longitude = st.text_input("Enter Longitude", key="Longitude_input")  # Float input
             # Float input

    if st.button("Predict"):
        if latitude is not None and longitude is not None:
                    # Placeholder for prediction logic
            prediction, prediction2, prediction3 = predict_water_well(latitude, longitude)
            if(prediction <= 15):
                st.success('This area is suitable for water well construction.')
            else: 
                st.success('This area is not suitable for water well construction.')
            st.success('Availability of ground water is : {} metres below ground water level(mbgl) .'.format(prediction))
            if(prediction3 < 0):
                st.success('Due to weather patterns the ground water level might decrease by {} metres below ground water level(mbgl). '.format(prediction3))
            if(prediction2 == 1):
                st.success('water is safe to drink.')
            else:
                st.success('water is not safe to drink.') 
            st.success('Suggested Drilling Techniques:')  
            st.success('Auger Drilling: Takes 1-2 days to complete.')  
            st.success('Rotary Drilling: Takes 2-3 days to complete.') 
            st.success('Percussion Drilling: Takea 3-5 days to complete.')     
        else:
            st.warning('Please fill in both latitude and longitude.')
    st.title("We would love your feedback!")
    st.slider('Rate our website!', min_value=1, max_value=10)
    st.text_input("Drop in any suggestions you would like!")
    if(st.button("submit")):
        st.write("""
                <style>
                    .big-font {
                    font-size: 500px;
                    }
                </style>
                """, unsafe_allow_html=True)

# Display text in a bigger font
        st.write("Thank You", unsafe_allow_html=True, key="big-font")

def main():
    st.title("AI Water Well Predictor")
    st.write("Welcome to the AI Water Well Predictor!")

if __name__ == "__main__":
    # CSS for background image
    st.markdown(
        """
        <style>
        .stApp {
            background-image: url('https://epiprod.evoqua.com/siteassets/images/resources/articles/digital-water-article.jpg');
            background-size: cover;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    page = st.radio("Select:", ["Login", "Sign Up"], index=0)
    if page == "Login":
        login()
        st.markdown('<a href="./">Back to Login</a>', unsafe_allow_html=True)
    else:
        signup()
        st.markdown('<a href="./">Back to Login</a>', unsafe_allow_html=True)

    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if st.session_state.logged_in:
        prediction_page()
