import streamlit as st
import streamlit.components.v1 as components
import base64
from firebase_admin import auth
from utils.firebase_init import init_firebase
from utils.auth import verify_token_and_set_session

# Initialize Firebase
init_firebase()

# Set up Streamlit page
st.set_page_config(page_title="FlashMaid", layout="wide")

# Display logo at the top of the sidebar
def show_logo():
    logo_path = "assets/flashmaid_logo.png"
    try:
        with open(logo_path, "rb") as image_file:
            encoded = base64.b64encode(image_file.read()).decode()
        st.sidebar.markdown(
            f"""
            <div style="text-align: center; margin-bottom: 1rem;">
                <img src='data:image/png;base64,{encoded}' width='140'/>
            </div>
            """,
            unsafe_allow_html=True
        )
    except FileNotFoundError:
        st.sidebar.warning("Logo file not found.")

# Phone Number Sign-In using Firebase Auth
def phone_sign_in():
    auth_html = """
    <html>
    <head>
      <script src="https://www.gstatic.com/firebasejs/8.10.1/firebase-app.js"></script>
      <script src="https://www.gstatic.com/firebasejs/8.10.1/firebase-auth.js"></script>
      <script>
        var firebaseConfig = {
          apiKey: "AIzaSyDFz7MMAc6hm9QdrK6Xu_u_k1C2_bOcSRc",
          authDomain: "flashmaid-63233.firebaseapp.com",
          projectId: "flashmaid-63233",
          storageBucket: "flashmaid-63233.appspot.com",
          messagingSenderId: "529866231861",
          appId: "1:529866231861:web:3d7569fee5680f7272a17c"
        };
        firebase.initializeApp(firebaseConfig);

        function sendOTP() {
          const phoneNumber = document.getElementById('phoneInput').value;
          const appVerifier = new firebase.auth.RecaptchaVerifier('recaptcha-container', {size: 'invisible'});

          firebase.auth().signInWithPhoneNumber(phoneNumber, appVerifier)
            .then(confirmationResult => {
              window.confirmationResult = confirmationResult;
              alert("OTP sent!");
            }).catch(error => {
              alert("Error sending OTP: " + error.message);
            });
        }

        function verifyOTP() {
          const code = document.getElementById('otpInput').value;
          window.confirmationResult.confirm(code).then(result => {
            return result.user.getIdToken();
          }).then(idToken => {
            window.location.replace(window.location.pathname + `?token=${idToken}`);
          }).catch(error => {
            alert("OTP verification failed: " + error.message);
          });
        }
      </script>
    </head>
    <body>
      <input id="phoneInput" placeholder="+91XXXXXXXXXX"/>
      <div id="recaptcha-container"></div>
      <button onclick="sendOTP()">Send OTP</button>
      <br><br>
      <input id="otpInput" placeholder="Enter OTP"/>
      <button onclick="verifyOTP()">Verify OTP</button>
    </body>
    </html>
    """
    components.html(auth_html, height=400)

# Main authentication flow
def main():
    show_logo()
    
    # Check for token in URL
    query_params = st.experimental_get_query_params()
    token = query_params.get("token", [None])[0]

    if token:
        if verify_token_and_set_session(token):
            st.experimental_set_query_params()  # Clear token from URL
            st.rerun()  # Refresh to show authenticated UI
        else:
            try:
                decoded_token = auth.verify_id_token(token, check_revoked=True)
                print("Decoded token:", decoded_token)
                uid = decoded_token['uid']
            except auth.RevokedIdTokenError:
                st.error("Token revoked, please sign in again")
            except auth.UserDisabledError:
                st.error("User account disabled")
            except Exception as e:
                st.error(f"Authentication failed: {str(e)}")

    # Show appropriate UI based on auth state
    if "user" not in st.session_state:
        st.title("Welcome to FlashMaid")
        st.write("Please sign in to continue")
        phone_sign_in()
        st.stop()
    else:
        show_authenticated_ui()

def show_authenticated_ui():
    user = st.session_state["user"]
    st.sidebar.title("FlashMaid")
    st.sidebar.markdown(f"Logged in as **{user.get('name', user.get('phone'))}**")
    st.sidebar.markdown(f"Role: **{user['role'].capitalize()}**")

    # Role-based navigation
    if user["role"] == "helper":
        st.switch_page("pages/helper/helper_profile.py")
    elif user["role"] == "household":
        st.switch_page("pages/household/household_profile.py")
    elif user["role"] == "admin":
        st.switch_page("pages/admin/dashboard.py")

if __name__ == "__main__":
    main()
