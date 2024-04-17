import streamlit as st
import crypto
import cv2
import numpy as np
from deepface import DeepFace
import time

# Define a SessionState class to manage login session
class SessionState:
    def __init__(self):
        self.logged_in = False

# Function to verify username and password (dummy implementation)
def verify_username_password(username, password):
    return username == "admin" and password == "admin123"

# Create a SessionState object
session_state = SessionState()

# Main function
def main():
    placeholder1 = st.empty()
    with placeholder1.container():
        st.title("Login using:")
        selected_page = st.radio("Login method:",["Password", "Face Recognition"], label_visibility="hidden", key="login_method")
        
        # Password login
        if selected_page == "Password":
                st.title("Password Login")
                username = st.text_input("Username")
                password = st.text_input("Password", type="password")
                if st.button("Login", key="login"):
                    # Perform username and password verification
                    if not verify_username_password(username, password):
                        st.error("Invalid username or password")
                    else:
                        session_state.logged_in = True
        
        # Face Recognition login
        elif selected_page == "Face Recognition":
            try:
                st.title("Face Recognition Login")
                # Capture an image from the webcam
                captured_image = st.camera_input("Take a picture")

                if captured_image is not None:
                    bytes_data = captured_image.getvalue()
                    cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)
                    cv2.imwrite('temp.jpg', cv2_img)

                    dfs = DeepFace.find(img_path="/home/umermansoor/Downloads/ml1_internship/crypto_streamlit/temp.jpg", db_path="/home/umermansoor/Downloads/ml1_internship/crypto_streamlit/faces", model_name="Facenet")

                    if not dfs or dfs[0].empty:
                        st.error("Face not recognized.")
                    else:
                        captured_image = None
                        dfs = None
                        session_state.logged_in = True
                else:
                    st.warning("No image captured.")
            except Exception as e:
                print("An error occurred:", e)
                st.error("Face not detected.")
    
    # Placeholder for the main content
    placeholder2 = st.empty()
    with placeholder2.container():
        if session_state.logged_in:
            placeholder1.empty()
            alert = st.success("Logged in successfully!")
            crypto.app(session_state)
            time.sleep(3)
            alert.empty()           
        else:
            st.warning("Please login to continue.")

if __name__ == "__main__":
    main()