import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
from email_validator import validate_email
from time import sleep
from nav import make_sidebar
make_sidebar()



# Establish connection to Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)
existing_data = conn.read(worksheet="PatientDetails", usecols=list(range(7)), ttl=5)
existing_data = existing_data.dropna(how="all")


def redirect(_url):
    link = st.markdown(link, unsafe_allow_html=True)



# Streamlit app code
def main():
    st.image("./Logo.png", width=100)
    # Set the app title and description
    st.markdown("""<h1 style='text-align: center;'>Player Basic Information</h1>""", unsafe_allow_html=True)
    # st.title("Dementia Classifier using MOD-1D-CNN")
    st.write("Please Enter the Basic Details and Proceed Further !!!")
    st.write("**Health Metrics Input Format:**")
    bullet_points = [
        "**Name :- FirstName LastName**",
        "**Email I'd :- For Example: abc@gmail.com**",
        "**Phone Number :- Enter 10 Digit Valid Phone Number**",
        "**Address :- Building Name, Floor No., District, State, Pincode**"
     ]

    st.write("- " + "\n- ".join(bullet_points))
    
    
    # Input fields for patient details
    Name = st.text_input(label="Name*")
    Email = st.text_input(label="Email*")
    Phone_Number = st.text_input(label="Phone Number*")
    Address = st.text_input(label="Address*")

    # Submit button
    if st.button("Submit"):
        # Check if any required field is empty
        if not Name or not Email or not Phone_Number or not Address:
            st.error("Please fill in all the required fields.")
        else:
            # Validate email
            try:
                valid = validate_email(Email)
                email = valid.email
            except Exception as e:
                st.error("Please enter a valid email address.")
                return
            
            # Validate phone number length
            if len(Phone_Number) != 10:
                st.error("Phone number should have exactly 10 digits.")
                return
            else:
                # Convert existing email and phone number columns to strings
                existing_data["Email"] = existing_data["Email"].astype(str)
                existing_data["Phone_Number"] = existing_data["Phone_Number"].astype(str)
                
                # Check if email or phone number already exists
                if existing_data["Email"].str.contains(email).any():
                    st.error("Email already exists.")
                    return
                if existing_data["Phone_Number"].str.contains(Phone_Number).any():
                    st.error("Phone number already exists.")
                    return
                
                # Create DataFrame with entered details
                Details_Data = pd.DataFrame(
                    [
                        {
                            "Name": Name,
                            "Email": email,
                            "Phone_Number": Phone_Number,
                            "Address": Address
                        }
                    ]
                )
                # Concatenate new data with existing data
                updated_df = pd.concat([existing_data, Details_Data], ignore_index=True)

                # Update Google Sheets with new data
                conn.update(worksheet="PatientDetails", data=updated_df)

                # Show success message
                # st.success("Health Metrics Details Successfully Submitted!")
                
                
                # # webbrowser.open("https://dementia-prediction.streamlit.app/")
                
                if st.success("Health Metrics Details Successfully Submitted!"):
                    st.session_state.logged_in = True
                    sleep(0.5)
                    st.switch_page("pages/app.py")


if __name__ == '__main__':
    main()


