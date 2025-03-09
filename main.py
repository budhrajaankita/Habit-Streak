import streamlit as st
import pandas as pd
from data_handler import HabitTracker
from viz import create_streak_chart, create_completion_calendar, create_weekly_summary
from datetime import datetime

# Page configuration (must be the first Streamlit command)
st.set_page_config(
    page_title="Track Your Day",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state for theme and cache
if 'theme' not in st.session_state:
    st.session_state.theme = "dark"
if 'habit_tracker' not in st.session_state:
    st.session_state.habit_tracker = HabitTracker()

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

@st.cache_data(ttl=300)  # Cache data for 5 minutes
def load_habits_data():
    """Load habits data from the database"""
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
</style>
""", unsafe_allow_html=True)

# Title and description
st.title("✨ Track Your Day")
st.write("Make every day count by building positive routines, one habit at a time")

# Sidebar for adding new habits
with st.sidebar:
    st.header("Settings")
    
    # Light mode toggle removed - always dark mode now
    
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
        # st.subheader("Overall Progress")
        # # Display streak chart
        # streak_chart = create_streak_chart(habits_df)
        # st.plotly_chart(streak_chart, use_container_width=True, key="overall_streak_chart")

        # # Display overall statistics
        st.subheader("Statistics")
        total_habits = len(habits_df)
        active_streaks = (habits_df['streak'] > 0).sum()
        avg_completion = habits_df['completion_rate'].mean()

        st.metric("Total Habits", total_habits)
        st.metric("Active Streaks", active_streaks)
        st.metric("Average Completion Rate", f"{avg_completion:.1f}%")

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