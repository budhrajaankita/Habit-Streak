# import streamlit as st
# import pandas as pd
# from data_handler import HabitTracker
# from viz import create_streak_chart, create_completion_calendar, create_weekly_summary
# from datetime import datetime

# # Page configuration (must be the first Streamlit command)
# st.set_page_config(
#     page_title="Track Your Day",
#     page_icon="✨",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# # Initialize session state for theme and cache
# if 'theme' not in st.session_state:
#     st.session_state.theme = "dark"
# if 'habit_tracker' not in st.session_state:
#     st.session_state.habit_tracker = HabitTracker()

# # Define habit types with icons and descriptions
# HABIT_TYPES = {
#     "Water": {
#         "icon": "💧",
#         "description": "Track your daily water intake"
#     },
#     "Weights": {
#         "icon": "💪",
#         "description": "Strength training and weight lifting"
#     },
#     "Cardio": {
#         "icon": "🏃",
#         "description": "Running, cycling, and other cardio activities"
#     },
#     "Stretching": {
#         "icon": "🧘‍♂️",
#         "description": "Flexibility and mobility work"
#     },
#     "No THC": {
#         "icon": "🌿",
#         "description": "Track your THC-free days"
#     },
#     "LeetCode": {
#         "icon": "💻",
#         "description": "Coding practice and problem-solving"
#     },
#     "Art": {
#         "icon": "🎨",
#         "description": "Drawing, painting, or creative expression"
#     },
#     "Call a Friend": {
#         "icon": "📞",
#         "description": "Stay connected with friends and family"
#     },
#     "Fruits": {
#         "icon": "🍎",
#         "description": "Daily fruit intake for vitamins and fiber"
#     },
#     "Vegetables": {
#         "icon": "🥦",
#         "description": "Daily vegetable servings for nutrients"
#     },
#     "Protein": {
#         "icon": "🥩",
#         "description": "Track protein intake for muscle building"
#     },
#     "Sleep": {
#         "icon": "😴",
#         "description": "Maintain a healthy sleep schedule"
#     },
#     "Healthy Eating": {
#         "icon": "🥗",
#         "description": "Track nutritious meals"
#     },
#     "Medicines": {
#         "icon": "💊",
#         "description": "Medication reminders"
#     },
#     "Reading": {
#         "icon": "📚",
#         "description": "Daily reading habit"
#     },
#     "Meditation": {
#         "icon": "🧘",
#         "description": "Mindfulness practice"
#     },
#     "Custom": {
#         "icon": "✨",
#         "description": "Create your own habit"
#     }
# }

# @st.cache_data(ttl=300)  # Cache data for 5 minutes
# def load_habits_data():
#     """Load habits data from the database"""
#     habits = st.session_state.habit_tracker.load_habits()
#     habits_df = pd.DataFrame(habits)
#     if not habits_df.empty:
#         habits_df['streak'] = habits_df['habit_name'].apply(
#             lambda x: st.session_state.habit_tracker.get_streak(x)
#         )
#         habits_df['completion_rate'] = habits_df['habit_name'].apply(
#             lambda x: st.session_state.habit_tracker.get_completion_rate(x)
#         )
#     return habits_df

# # Apply dark theme consistently
# st.markdown("""
# <style>
# .stApp {
#     background-color: #0E1117;
#     color: #FFFFFF;
# }

# .stSidebar {
#     background-color: #262730;
# }

# [data-testid="stSidebar"] {
#     background-color: #262730;
# }

# .stHeader {
#     background-color: #0E1117;
# }

# h1, h2, h3, h4, h5, h6, p, span, div {
#     color: #FFFFFF !important;
# }

# .stSelectbox > div, .stNumberInput > div {
#     background-color: #262730 !important;
#     color: #FFFFFF !important;
# }

# div[data-baseweb="select"] * {
#     background-color: #262730 !important;
#     color: #FFFFFF !important;
# }

# div[data-baseweb="input"] * {
#     background-color: #262730 !important;
#     color: #FFFFFF !important;
# }

# button {
#     background-color: #262730 !important;
#     color: #FFFFFF !important;
# }

# .stMarkdown, .stMarkdown * {
#     color: #FFFFFF !important;
# }

# .css-145kmo2 {
#     color: #FFFFFF !important;
# }

# /* Fix for plotly elements */
# .js-plotly-plot .plotly, .js-plotly-plot .plotly * {
#     color: #FFFFFF !important;
# }

# /* Ensure all elements are properly styled */
# .stExpander {
#     background-color: #262730 !important;
#     border-color: #4E5969 !important;
# }

# .stMetric {
#     background-color: #262730 !important;
#     color: #FFFFFF !important;
# }

# .stMetric label {
#     color: #9CA3AF !important;
# }
# </style>
# """, unsafe_allow_html=True)

# # Title and description
# st.title("✨ Track Your Day")
# st.write("Make every day count by building positive routines, one habit at a time")

# # Sidebar for adding new habits
# with st.sidebar:
#     st.header("Settings")
    
#     # Light mode toggle removed - always dark mode now
    
#     st.header("Add New Habit")

#     # Habit type selector
#     habit_type = st.selectbox(
#         "Select Habit Type",
#         options=list(HABIT_TYPES.keys()),
#         format_func=lambda x: f"{HABIT_TYPES[x]['icon']} {x}"
#     )

#     # Custom habit name input for "Custom" type
#     if habit_type == "Custom":
#         new_habit = st.text_input("Custom Habit Name")
#         if new_habit:
#             st.info(f"You're creating a custom habit: {new_habit}")
#     else:
#         new_habit = habit_type
#         st.info(f"{HABIT_TYPES[habit_type]['icon']} {HABIT_TYPES[habit_type]['description']}")

#     frequency = st.selectbox(
#         "Target Frequency",
#         ["Daily", "Weekly", "Monthly"]
#     )

#     if st.button("Add Habit"):
#         if new_habit:
#             success = st.session_state.habit_tracker.save_habit(new_habit, frequency)
#             if success:
#                 st.success(f"Added new habit: {HABIT_TYPES.get(new_habit, {'icon': '✨'})['icon']} {new_habit}")
#                 st.cache_data.clear()  # Clear cache when adding new habit
#                 st.rerun()
#             else:
#                 st.error(f"Habit '{new_habit}' already exists!")
#         else:
#             st.error("Please select a habit type or enter a custom habit name")

# # Main content
# habits_df = load_habits_data()

# if not habits_df.empty:
#     # Create two columns for the main content
#     col1, col2 = st.columns([1.5, 1])  # Changed from [2, 1] to [1.5, 1] for more compact left column

#     with col1:
#         st.subheader("Your Habits")

#         # Display habits with check-in buttons
#         for _, habit in habits_df.iterrows():
#             # Get the habit name and look up its icon
#             habit_name = habit['habit_name']
#             habit_icon = HABIT_TYPES.get(habit_name, {"icon": "✨"})["icon"]
#             with st.expander(f"{habit_icon} {habit_name} (Streak: {habit['streak']} days)"):
#                 col_a, col_b, col_c = st.columns([0.8, 1, 1])  # Made check-in column slightly smaller

#                 with col_a:
#                     if st.button("✅ Check-in", key=f"checkin_{habit_name}"):
#                         st.session_state.habit_tracker.check_in_habit(habit_name)
#                         st.cache_data.clear()  # Clear cache when checking in
#                         st.rerun()

#                 with col_b:
#                     st.metric("Current Streak", f"{habit['streak']} days")

#                 with col_c:
#                     st.metric("Completion Rate", f"{habit['completion_rate']:.1f}%")

#                 # Show habit-specific visualizations with more height
#                 if not pd.isna(habit['check_ins']) and habit['check_ins']:
#                     cal_chart = create_completion_calendar(habit['check_ins'])
#                     if cal_chart:
#                         st.plotly_chart(cal_chart, use_container_width=True, key=f"cal_{habit_name}", height=300)

#                     weekly_chart = create_weekly_summary(habit['check_ins'])
#                     if weekly_chart:
#                         st.plotly_chart(weekly_chart, use_container_width=True, key=f"weekly_{habit_name}", height=300)

#     with col2:
#         # st.subheader("Overall Progress")
#         # # Display streak chart
#         # streak_chart = create_streak_chart(habits_df)
#         # st.plotly_chart(streak_chart, use_container_width=True, key="overall_streak_chart")

#         # # Display overall statistics
#         st.subheader("Statistics")
#         total_habits = len(habits_df)
#         active_streaks = (habits_df['streak'] > 0).sum()
#         avg_completion = habits_df['completion_rate'].mean()

#         st.metric("Total Habits", total_habits)
#         st.metric("Active Streaks", active_streaks)
#         st.metric("Average Completion Rate", f"{avg_completion:.1f}%")


import streamlit as st
import pandas as pd
from data_handler import HabitTracker
from viz import create_streak_chart, create_completion_calendar, create_weekly_summary
from datetime import datetime
from database import get_db
from auth import create_user, authenticate_user, create_session_token, validate_session, logout_user, User


from database import Base, engine

# This will create all tables defined using the Base class
Base.metadata.create_all(bind=engine)

# Page configuration (must be the first Streamlit command)
st.set_page_config(
    page_title="Track Your Day",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state for theme and authentication
if 'theme' not in st.session_state:
    st.session_state.theme = "dark"
if 'user_id' not in st.session_state:
    st.session_state.user_id = None
if 'username' not in st.session_state:
    st.session_state.username = None
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'login_error' not in st.session_state:
    st.session_state.login_error = ""
if 'register_error' not in st.session_state:
    st.session_state.register_error = ""
if 'register_success' not in st.session_state:
    st.session_state.register_success = False
if 'current_page' not in st.session_state:
    st.session_state.current_page = "login"

# Check for session token in cookies
if 'session_token' in st.session_state and not st.session_state.authenticated:
    db = next(get_db())
    HabitTracker.add_user_id_column()

    user = validate_session(db, st.session_state.session_token)
    if user:
        st.session_state.authenticated = True
        st.session_state.user_id = user.id
        st.session_state.username = user.username
        st.session_state.current_page = "dashboard"

# Initialize habit tracker with user_id if authenticated
if 'habit_tracker' not in st.session_state or st.session_state.authenticated and st.session_state.habit_tracker.user_id != st.session_state.user_id:
    st.session_state.habit_tracker = HabitTracker(st.session_state.user_id)

# Define habit types with icons and descriptions
HABIT_TYPES = {
    "Water": {
        "icon": "💧",
        "description": "Track your daily water intake"
    },
    "Weights": {
        "icon": "💪",
        "description": "Strength training and weight lifting"
    },
    "Cardio": {
        "icon": "🏃",
        "description": "Running, cycling, and other cardio activities"
    },
    "Stretching": {
        "icon": "🧘‍♂️",
        "description": "Flexibility and mobility work"
    },
    "No THC": {
        "icon": "🌿",
        "description": "Track your THC-free days"
    },
    "LeetCode": {
        "icon": "💻",
        "description": "Coding practice and problem-solving"
    },
    "Art": {
        "icon": "🎨",
        "description": "Drawing, painting, or creative expression"
    },
    "Call a Friend": {
        "icon": "📞",
        "description": "Stay connected with friends and family"
    },
    "Fruits": {
        "icon": "🍎",
        "description": "Daily fruit intake for vitamins and fiber"
    },
    "Vegetables": {
        "icon": "🥦",
        "description": "Daily vegetable servings for nutrients"
    },
    "Protein": {
        "icon": "🥩",
        "description": "Track protein intake for muscle building"
    },
    "Sleep": {
        "icon": "😴",
        "description": "Maintain a healthy sleep schedule"
    },
    "Healthy Eating": {
        "icon": "🥗",
        "description": "Track nutritious meals"
    },
    "Medicines": {
        "icon": "💊",
        "description": "Medication reminders"
    },
    "Reading": {
        "icon": "📚",
        "description": "Daily reading habit"
    },
    "Meditation": {
        "icon": "🧘",
        "description": "Mindfulness practice"
    },
    "Custom": {
        "icon": "✨",
        "description": "Create your own habit"
    }
}

# Login callback
def login():
    username = st.session_state.login_username
    password = st.session_state.login_password
    
    db = next(get_db())
    user = authenticate_user(db, username, password)
    
    if user:
        # Create session token
        token = create_session_token(db, user)
        st.session_state.session_token = token
        st.session_state.authenticated = True
        st.session_state.user_id = user.id
        st.session_state.username = user.username
        st.session_state.current_page = "dashboard"
        st.session_state.login_error = ""
        # Initialize habit tracker with user_id
        st.session_state.habit_tracker = HabitTracker(user.id)
    else:
        st.session_state.login_error = "Invalid username or password"

# Register callback
def register():
    username = st.session_state.register_username
    email = st.session_state.register_email
    password = st.session_state.register_password
    confirm_password = st.session_state.register_confirm_password
    
    # Validate inputs
    if not username or not email or not password:
        st.session_state.register_error = "All fields are required"
        return
    
    if password != confirm_password:
        st.session_state.register_error = "Passwords do not match"
        return
    
    if len(password) < 8:
        st.session_state.register_error = "Password must be at least 8 characters"
        return
    
    # Create user
    db = next(get_db())
    user = create_user(db, username, email, password)
    
    if user:
        st.session_state.register_success = True
        st.session_state.register_error = ""
        st.session_state.current_page = "login"
    else:
        st.session_state.register_error = "Username or email already exists"

# Logout callback
def logout():
    if st.session_state.authenticated and st.session_state.user_id:
        db = next(get_db())
        user = db.query(User).filter(User.id == st.session_state.user_id).first()
        if user:
            logout_user(db, user)
    
    # Clear session
    st.session_state.authenticated = False
    st.session_state.user_id = None
    st.session_state.username = None
    st.session_state.session_token = None
    st.session_state.current_page = "login"

# Switch page callback
def switch_to_page(page):
    st.session_state.current_page = page
    # Clear any errors
    st.session_state.login_error = ""
    st.session_state.register_error = ""
    st.session_state.register_success = False

@st.cache_data(ttl=300)  # Cache data for 5 minutes
def load_habits_data():
    """Load habits data from the database"""
    if not st.session_state.authenticated:
        return pd.DataFrame()
        
    habits = st.session_state.habit_tracker.load_habits()
    habits_df = pd.DataFrame(habits)
    if not habits_df.empty:
        habits_df['streak'] = habits_df['habit_name'].apply(
            lambda x: st.session_state.habit_tracker.get_streak(x)
        )
        habits_df['completion_rate'] = habits_df['habit_name'].apply(
            lambda x: st.session_state.habit_tracker.get_completion_rate(x)
        )
    return habits_df

# Apply dark theme consistently
st.markdown("""
<style>
.stApp {
    background-color: #0E1117;
    color: #FFFFFF;
}

.stSidebar {
    background-color: #262730;
}

[data-testid="stSidebar"] {
    background-color: #262730;
}

.stHeader {
    background-color: #0E1117;
}

h1, h2, h3, h4, h5, h6, p, span, div {
    color: #FFFFFF !important;
}

.stSelectbox > div, .stNumberInput > div {
    background-color: #262730 !important;
    color: #FFFFFF !important;
}

div[data-baseweb="select"] * {
    background-color: #262730 !important;
    color: #FFFFFF !important;
}

div[data-baseweb="input"] * {
    background-color: #262730 !important;
    color: #FFFFFF !important;
}

button {
    background-color: #262730 !important;
    color: #FFFFFF !important;
}

.stMarkdown, .stMarkdown * {
    color: #FFFFFF !important;
}

.css-145kmo2 {
    color: #FFFFFF !important;
}

/* Fix for plotly elements */
.js-plotly-plot .plotly, .js-plotly-plot .plotly * {
    color: #FFFFFF !important;
}

/* Ensure all elements are properly styled */
.stExpander {
    background-color: #262730 !important;
    border-color: #4E5969 !important;
}

.stMetric {
    background-color: #262730 !important;
    color: #FFFFFF !important;
}

.stMetric label {
    color: #9CA3AF !important;
}

/* Style for login/register forms */
.auth-form {
    background-color: #262730;
    padding: 2rem;
    border-radius: 10px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    margin: 0 auto;
    max-width: 400px;
}

.auth-form input {
    background-color: #1E1E1E !important;
    color: white !important;
    border: 1px solid #4E5969 !important;
}

.auth-link {
    color: #FF4B4B !important;
    text-decoration: none;
    cursor: pointer;
}

.auth-link:hover {
    text-decoration: underline;
}

.auth-error {
    background-color: rgba(255, 75, 75, 0.1);
    color: #FF4B4B !important;
    padding: 0.5rem;
    border-radius: 5px;
    margin-top: 0.5rem;
}

.auth-success {
    background-color: rgba(75, 255, 75, 0.1);
    color: #4BFF4B !important;
    padding: 0.5rem;
    border-radius: 5px;
    margin-top: 0.5rem;
}
</style>
""", unsafe_allow_html=True)

# # Render the appropriate page
# if st.session_state.current_page == "login":
#     # Login Page
#     st.title("✨ Track Your Day")
#     st.write("Make every day count by building positive routines, one habit at a time")
    
#     with st.container():
#         st.header("Login")
        
#         # Login Form
#         with st.form("login_form", clear_on_submit=False):
#             st.text_input("Username", key="login_username")
#             st.text_input("Password", type="password", key="login_password")
            
#             if st.session_state.login_error:
#                 st.markdown(f"""
#                 <div class="auth-error">
#                     {st.session_state.login_error}
#                 </div>
#                 """, unsafe_allow_html=True)
                
#             if st.session_state.register_success:
#                 st.markdown(f"""
#                 <div class="auth-success">
#                     Registration successful! Please log in.
#                 </div>
#                 """, unsafe_allow_html=True)
                
#             col1, col2 = st.columns([1, 1])
#             with col1:
#                 login_button = st.form_submit_button("Login", on_click=login)
                
#             with col2:
#                 st.markdown(f"""
#                 <div style="text-align: right; padding-top: 5px;">
#                     <a class="auth-link" onClick='
#                     document.dispatchEvent(new CustomEvent("streamlit:componentCommunication", {{
#                         detail: {{
#                             type: "streamlit:setValue",
#                             value: "register",
#                             target: "current_page"
#                         }}
#                     }}));
#                     '>Register</a>
#                 </div>
#                 """, unsafe_allow_html=True)
        
#         # Demo account info
#         st.markdown("""
#         <div style="margin-top: 20px; text-align: center;">
#             <p>Demo account: <code>demo / password123</code></p>
#         </div>
#         """, unsafe_allow_html=True)
            
# elif st.session_state.current_page == "register":
#     # Register Page
#     st.title("✨ Track Your Day")
#     st.write("Make every day count by building positive routines, one habit at a time")
#     print("HERE")
#     with st.container():
#         st.header("Register")
        
#         # Register Form
#         with st.form("register_form", clear_on_submit=False):
#             st.text_input("Username", key="register_username")
#             st.text_input("Email", key="register_email")
#             st.text_input("Password", type="password", key="register_password")
#             st.text_input("Confirm Password", type="password", key="register_confirm_password")
            
#             if st.session_state.register_error:
#                 st.markdown(f"""
#                 <div class="auth-error">
#                     {st.session_state.register_error}
#                 </div>
#                 """, unsafe_allow_html=True)
                
#             col1, col2 = st.columns([1, 1])
#             with col1:
#                 register_button = st.form_submit_button("Register", on_click=register)
#             with col2:
#                 st.markdown(f"""
#                 <div style="text-align: right; padding-top: 5px;">
#                     <a class="auth-link" onClick='
#                     document.dispatchEvent(new CustomEvent("streamlit:componentCommunication", {{
#                         detail: {{
#                             type: "streamlit:setValue",
#                             value: "login",
#                             target: "current_page"
#                         }}
#                     }}));
#                     '>Back to Login</a>
#                 </div>
#                 """, unsafe_allow_html=True)
# Render the appropriate page
if st.session_state.current_page == "login":
    # Login Page
    st.title("✨ Track Your Day")
    st.write("Make every day count by building positive routines, one habit at a time")
    
    with st.container():
        st.header("Login")
        
        # Login Form
        with st.form("login_form", clear_on_submit=False):
            st.text_input("Username", key="login_username")
            st.text_input("Password", type="password", key="login_password")
            
            if st.session_state.login_error:
                st.markdown(f"""
                <div class="auth-error">
                    {st.session_state.login_error}
                </div>
                """, unsafe_allow_html=True)
                
            if st.session_state.register_success:
                st.markdown(f"""
                <div class="auth-success">
                    Registration successful! Please log in.
                </div>
                """, unsafe_allow_html=True)
                
            login_button = st.form_submit_button("Login", on_click=login)
        
        # Register link outside the form
        col1, col2 = st.columns([1, 1])
        with col2:
            if st.button("Register", key="to_register"):
                st.session_state.current_page = "register"
                st.rerun()
            
        # Demo account info
        st.markdown("""
        <div style="margin-top: 20px; text-align: center;">
            <p>Demo account: <code>demo / password123</code></p>
        </div>
        """, unsafe_allow_html=True)
            
elif st.session_state.current_page == "register":
    # Register Page
    st.title("✨ Track Your Day")
    st.write("Make every day count by building positive routines, one habit at a time")
    
    with st.container():
        st.header("Register")
        
        # Register Form
        with st.form("register_form", clear_on_submit=False):
            st.text_input("Username", key="register_username")
            st.text_input("Email", key="register_email")
            st.text_input("Password", type="password", key="register_password")
            st.text_input("Confirm Password", type="password", key="register_confirm_password")
            
            if st.session_state.register_error:
                st.markdown(f"""
                <div class="auth-error">
                    {st.session_state.register_error}
                </div>
                """, unsafe_allow_html=True)
                
            register_button = st.form_submit_button("Register", on_click=register)
        
        # Back to login link outside the form
        col1, col2 = st.columns([1, 1])
        with col2:
            if st.button("Back to Login", key="to_login"):
                st.session_state.current_page = "login"
                st.rerun()

elif st.session_state.current_page == "dashboard" and st.session_state.authenticated:
    # Dashboard (only accessible when authenticated)
    # Title and description
    st.title(f"✨ Track Your Day - Welcome, {st.session_state.username}!")
    st.write("Make every day count by building positive routines, one habit at a time")

    # Sidebar for adding new habits and logout
    with st.sidebar:
        st.header("Settings")
        
        # Logout button
        if st.button("Logout", on_click=logout):
            pass  # Logic is handled in the callback
        
        st.header("Add New Habit")

        # Habit type selector
        habit_type = st.selectbox(
            "Select Habit Type",
            options=list(HABIT_TYPES.keys()),
            format_func=lambda x: f"{HABIT_TYPES[x]['icon']} {x}"
        )

        # Custom habit name input for "Custom" type
        if habit_type == "Custom":
            new_habit = st.text_input("Custom Habit Name")
            if new_habit:
                st.info(f"You're creating a custom habit: {new_habit}")
        else:
            new_habit = habit_type
            st.info(f"{HABIT_TYPES[habit_type]['icon']} {HABIT_TYPES[habit_type]['description']}")

        frequency = st.selectbox(
            "Target Frequency",
            ["Daily", "Weekly", "Monthly"]
        )

        if st.button("Add Habit"):
            if new_habit:
                success = st.session_state.habit_tracker.save_habit(new_habit, frequency)
                if success:
                    st.success(f"Added new habit: {HABIT_TYPES.get(new_habit, {'icon': '✨'})['icon']} {new_habit}")
                    st.cache_data.clear()  # Clear cache when adding new habit
                    st.rerun()
                else:
                    st.error(f"Habit '{new_habit}' already exists!")
            else:
                st.error("Please select a habit type or enter a custom habit name")

    # Main content
    habits_df = load_habits_data()

    if not habits_df.empty:
        # Create two columns for the main content
        col1, col2 = st.columns([1.5, 1])  # Changed from [2, 1] to [1.5, 1] for more compact left column

        with col1:
            st.subheader("Your Habits")

            # Display habits with check-in buttons
            for _, habit in habits_df.iterrows():
                # Get the habit name and look up its icon
                habit_name = habit['habit_name']
                habit_icon = HABIT_TYPES.get(habit_name, {"icon": "✨"})["icon"]
                with st.expander(f"{habit_icon} {habit_name} (Streak: {habit['streak']} days)"):
                    col_a, col_b, col_c = st.columns([0.8, 1, 1])  # Made check-in column slightly smaller

                    with col_a:
                        if st.button("✅ Check-in", key=f"checkin_{habit_name}"):
                            st.session_state.habit_tracker.check_in_habit(habit_name)
                            st.cache_data.clear()  # Clear cache when checking in
                            st.rerun()

                    with col_b:
                        st.metric("Current Streak", f"{habit['streak']} days")

                    with col_c:
                        st.metric("Completion Rate", f"{habit['completion_rate']:.1f}%")

                    # Show habit-specific visualizations with more height
                    if not pd.isna(habit['check_ins']) and habit['check_ins']:
                        cal_chart = create_completion_calendar(habit['check_ins'])
                        if cal_chart:
                            st.plotly_chart(cal_chart, use_container_width=True, key=f"cal_{habit_name}", height=300)

                        weekly_chart = create_weekly_summary(habit['check_ins'])
                        if weekly_chart:
                            st.plotly_chart(weekly_chart, use_container_width=True, key=f"weekly_{habit_name}", height=300)

        with col2:
            st.subheader("Statistics")
            total_habits = len(habits_df)
            active_streaks = (habits_df['streak'] > 0).sum()
            avg_completion = habits_df['completion_rate'].mean()

            st.metric("Total Habits", total_habits)
            st.metric("Active Streaks", active_streaks)
            st.metric("Average Completion Rate", f"{avg_completion:.1f}%")

            # Show dashboard

            # Display main dashboard after habit form
            def show_dashboard(habits_df):
                if len(habits_df) > 0:
                    st.subheader("Overall Stats")
                    col1, col2, col3 = st.columns(3)
                    
                    total_habits = len(habits_df)
                    avg_streak = habits_df['streak'].mean()
                    avg_completion = habits_df['completion_rate'].mean()
                    
                    col1.metric("Total Habits", total_habits)
                    col2.metric("Average Streak", f"{avg_streak:.1f} days")
                    col3.metric("Average Completion Rate", f"{avg_completion:.1f}%")
                    
                    # Create two tabs for all habits and nutrition tracking
                    tab1, tab2 = st.tabs(["All Habits", "Nutrition Tracking"])
                    
                    with tab1:
                        # Overall Progress - Combined GitHub style chart
                        st.subheader("Overall Progress")
                        streak_chart = create_streak_chart(habits_df)
                        if streak_chart:
                            st.plotly_chart(streak_chart, use_container_width=True, key="overall_streak")
                        
                        # Individual habit GitHub charts
                        for idx, habit in habits_df.iterrows():
                            with st.expander(f"{HABIT_TYPES.get(habit['habit_name'], {}).get('icon', '')} {habit['habit_name']} - {habit['streak']} day streak"):
                                # Create individual GitHub-style chart
                                individual_chart = create_streak_chart(habits_df, combined=False, habit_name=habit['habit_name'])
                                if individual_chart:
                                    st.plotly_chart(individual_chart, use_container_width=True, key=f"habit_{idx}_streak")
                    
                    with tab2:
                        # Filter nutrition habits based on habit_name instead of habit_type
                        nutrition_habits = habits_df[habits_df['habit_name'].isin(['Fruits', 'Vegetables', 'Protein'])]
                        
                        if not nutrition_habits.empty:
                            st.subheader("Nutrition Tracking")
                            # Create combined nutrition chart with blue theme
                            nutrition_chart = create_streak_chart(nutrition_habits, color_theme="purple")
                            if nutrition_chart:
                                st.plotly_chart(nutrition_chart, use_container_width=True, key="nutrition_streak")
                            
                            # Individual nutrition habits with blue theme
                            for idx, habit in nutrition_habits.iterrows():
                                habit_name = habit['habit_name']
                                habit_icon = HABIT_TYPES.get(habit_name, {"icon": "✨"})["icon"]
                                with st.expander(f"{habit_icon} {habit_name} - {habit['streak']} day streak"):
                                    # Create individual GitHub-style chart with blue theme
                                    individual_chart = create_streak_chart(nutrition_habits, combined=False, habit_name=habit['habit_name'], color_theme="blue")
                                    if individual_chart:
                                        st.plotly_chart(individual_chart, use_container_width=True, key=f"nutrition_{idx}_streak")
                        else:
                            st.info("Add habits with type 'Fruits', 'Vegetables', or 'Protein' to see nutrition tracking.")

            show_dashboard(habits_df)

    else:
        st.info("No habits added yet. Use the sidebar to add your first habit!")