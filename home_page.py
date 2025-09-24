import streamlit as st
import streamlit_authenticator as stauth
from database import SessionLocal, User 
import yaml 
from yaml.loader import SafeLoader
import traceback


def fetch_users():
    """Fetches user data from the database for the authenticator."""
    db = SessionLocal()
    users = db.query(User).all()
    db.close()
    print("Fetched users for authenticator:")
    for user in users:
        print(f"Username: {user.username}, Hashed PW: {user.hashed_password}")
    credentials = {"usernames": {}}
    for user in users:
        credentials["usernames"][user.username] = {
            "name": user.username, 
            "password": user.hashed_password
        }
    return credentials



st.title("AI Fashion Stylist ✨")

credentials = fetch_users()

config = {
    'credentials': credentials,
    'cookie': {
        'name': 'ai_stylist_cookie',
        'key': 'myGrandFa1h3rC10c1<', 
        'expiry_days': 30
    }
}
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)



if "show_registration" not in st.session_state:
    st.session_state["show_registration"] = False

if not st.session_state["show_registration"]:
    authenticator.login('main', 'login')
    if st.session_state.get("authentication_status"):
        st.write(f'Welcome *{st.session_state["name"]}*')
        authenticator.logout('logout')
        st.info("Select a page from the sidebar to get started.")
        st.sidebar.success("You are logged in.")
    elif st.session_state.get("authentication_status") is False:
        st.error('Username/password is incorrect')
    elif st.session_state.get("authentication_status") is None:
        st.warning('Please enter your username and password')
        if st.button("New user? Create account"):
            st.session_state["show_registration"] = True
            st.rerun()
else:
    st.subheader("Create a New Account")
    try:
        registration_result = authenticator.register_user('main', 'Register user')
        if registration_result:
            email, username, name = registration_result 
            
            # Find the hashed password from the updated credentials
            hashed_password = config['credentials']['usernames'][username]['password']

           
            db = SessionLocal()
            new_user = User(username=username, hashed_password=hashed_password)
            db.add(new_user)
            db.commit()
            db.close()

            
            with open('config.yaml', 'w') as file:
                yaml.dump(config, file, default_flow_style=False)

            st.session_state["show_registration"] = False
            st.success('User registered successfully. Please login.')
            st.rerun()
    except Exception as e:
        st.error(e)
        pass
    if st.button("Back to Login"):
        st.session_state["show_registration"] = False
        st.rerun()

