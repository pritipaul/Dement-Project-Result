import streamlit as st
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import Conv1D, MaxPooling1D, Flatten, Dense, Dropout
from streamlit_gsheets import GSheetsConnection
from nav import make_sidebar


make_sidebar()



# Load the dataset
data = pd.read_csv("./Dataset/Dementia_new_data.csv")

# Establish connection to Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)
existing_data = conn.read(worksheet="Dementia", usecols=list(range(7)), ttl=5)
existing_data = existing_data.dropna(how="all")


# Split into features and target
y = data['Dementia']
x = data.drop('Dementia', axis=1)

# Split into training and testing data
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=1, stratify=y)

# Standardize the data
sc = StandardScaler()
x_train_sc = sc.fit_transform(x_train)
x_test_sc = sc.transform(x_test)

n_features, n_outputs = x_train_sc.shape[1], 2
model = Sequential()
model.add(Conv1D(filters=64, kernel_size=2, activation='relu', input_shape=(n_features,1)))
model.add(Conv1D(filters=64, kernel_size=2, activation='relu'))
model.add(Dropout(0.2))
model.add(MaxPooling1D(pool_size=2))
model.add(Flatten())
model.add(Dense(100, activation='relu'))
model.add(Dense(n_outputs, activation='softmax'))

# Compile the model
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Load the trained model weights
model.load_weights("DementiaDetection_DL_Model_1DCNN_CSV.h5")

# Define class labels
class_labels = ['Non-Demented', 'Demented']


def predict_dementia(features):
    processed_features = sc.transform([features])
    prediction = model.predict(processed_features)[0]
    predicted_index = np.argmax(prediction)
    predicted_label = class_labels[predicted_index]
    return predicted_label


# Streamlit app code
def main():
    
    st.image("./Logo.png", width=100)
    # Set the app title and description
    st.markdown("""<h1 style='text-align: center;'>Dementia Classifier using<br>MOD-1D-CNN</h1>""", unsafe_allow_html=True)
    # st.title("Dementia Classifier using MOD-1D-CNN")
    st.write("Enter the health metrics features and predict whether demented or non-demented.")
    st.write("**Health Metrics Input Format:**")
    bullet_points = [
    "**Diabetic status (0 for absence or 1 for presence)**",
    "**Age: 1(40-64) or 2(65-70) or 3(75-90)**",
    "**Heart rate: 1(<60bpm) or 2(60bpm – 100bpm) or 3(>100bpm)**",
    "**Blood oxygen level (1(<95%) or 2(95%-100%) or 3(>100%))**",
    "**Body temperature: 1(<36.5oC) or 2(36.5oC – 37.5oC) or 3(>37.5oC)**",
    "**Weight: 1(<50kg) or 2(50kg – 70kg) or 3(>70kg)**"
     ]

    st.write("- " + "\n- ".join(bullet_points)) 
    # Email = st.text_input(label="Email*",value='pre_filled_email',disabled=True)
    
    Diabetic = st.radio("Diabetic", [0, 1])
    Age_Class = st.radio("Age_Class", [1, 2, 3])
    HeartRate_Class = st.radio("HeartRate_Class", [1, 2, 3])
    BloodOxygenLevel_Class = st.radio("BloodOxygenLevel_Class", [1, 2, 3])
    BodyTemperature_Class = st.radio("BodyTemperature_Class", [1, 2, 3])
    Weight_Class = st.radio("Weight_Class", [1, 2, 3])

    if st.button("Predict"):
        features = [Diabetic, Age_Class, HeartRate_Class, BloodOxygenLevel_Class, BodyTemperature_Class, Weight_Class]
        predicted_label = predict_dementia(features)
        st.write("Predicted Label:", predicted_label)
        Dementia_Data = pd.DataFrame(
            [
                {
                    "Diabetic": Diabetic,
                    "Age_Class": Age_Class,
                    "HeartRate_Class": HeartRate_Class,
                    "BloodOxygenLevel_Class": BloodOxygenLevel_Class,
                    "BodyTemperature_Class": BodyTemperature_Class,
                    "Weight_Class": Weight_Class,
                    "predicted_label": predicted_label
                }
            ]
        )

        updated_df = pd.concat([existing_data, Dementia_Data], ignore_index=True)
        conn.update(worksheet="Dementia", data=updated_df)

        st.success("Health Metrics Details Successfully Submitted!")
        st.write(f'''
            <a target="_self" href="https://code2project2023.github.io/code2project2023/index.html">
                <button>
                    Please login via Google
                </button>
            </a>
            ''',
            unsafe_allow_html=True
        )




if __name__ == '__main__':
    main()
