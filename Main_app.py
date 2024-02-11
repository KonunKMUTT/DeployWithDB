import pickle
import pandas as pd
import streamlit as st
import GSheetsConnection
from streamlit_gsheets 

# Load the Google Sheets worksheet
sheet = client.open('Your Google Sheet Name').sheet1  # Change 'Your Google Sheet Name' to the name of your Google Sheet

# Streamlit app
def main():
    st.title('Google Sheets Connection')
    
    # Example: Read data from Google Sheets
    data = sheet.get_all_records()
    st.write('Data from Google Sheets:')
    st.write(data)

if __name__ == '__main__':
    main()


# Load the model
with open('model.pkl', 'rb') as file:
    model = pickle.load(file)

# Function to make prediction
def predict_heart_disease(age, impulse, pressure_high, pressure_low, glucose, kcm, troponin, female, male):
    x_new = pd.DataFrame({
        'age': [age],
        'impluse': [impulse],
        'pressurehight': [pressure_high],
        'pressurelow': [pressure_low],
        'glucose': [glucose],
        'kcm': [kcm],
        'troponin': [troponin],
        'female': [female],
        'male': [male]
        })

    y_pred_new = model.predict(x_new)
    return y_pred_new

# Streamlit app
def main():
    st.markdown('<p style="text-align:center; font-weight:bold; font-size:30px;">Heart Disease Prediction App</p>', unsafe_allow_html=True)

    age = st.text_input("Enter age:")
    impulse = st.text_input("Enter impulse:")
    pressure_high = st.text_input("Enter high blood pressure:")
    pressure_low = st.text_input("Enter low blood pressure:")
    glucose = st.text_input("Enter glucose level:")
    kcm = st.text_input("Enter KCM:")
    troponin = st.text_input("Enter troponin level:")
    gender = st.selectbox("Select gender", ["Female", "Male"])

    # Set gender value based on selection
    if gender == "Female":
        female = 1
        male = 0
    else:
        female = 0
        male = 1
       
    if st.button("Predict"):
      
        result = predict_heart_disease(age, impulse, pressure_high, pressure_low, glucose, kcm, troponin, female, male)
        
        # Set color based on the result
        color = "red" if result == "positive" else "green"  # Adjust this condition based on your model's output

        # Apply styling with HTML
        styled_result = f'<p style="color:{color}; font-size:20px; text-align:center; font-weight:bold; background-color:#4B4A54; padding:10px; border-radius: 15px;">{result}</p>'
        
        # Display the styled result
        st.markdown(styled_result, unsafe_allow_html=True)

     # Create a connection object.
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('token.json', scope)
    client = gspread.authorize(creds)
    
    # Load the Google Sheets worksheet
    sheet = client.open('IS_HeartDiseasePredictionApp').sheet1  # Change 'Your Google Sheet Name' to the name of your Google Sheet
    sheet.append_row([age, impulse, pressure_high, pressure_low, glucose, kcm, troponin, female, male, result])

if __name__ == '__main__':
    main()

