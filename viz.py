import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from datetime import datetime, timedelta
import calendar
import streamlit as st
import numpy as np
from plotly.subplots import make_subplots

def get_theme_colors():
    """Get theme-specific colors"""
    is_dark = st.session_state.get('theme', 'light') == 'dark'
    return {
        'background': '#1E1E1E' if is_dark else '#FFFFFF',
        'text': '#FFFFFF' if is_dark else '#1E1E1E',
        'primary': '#FF4B4B',
        'secondary': 'rgba(255,255,255,0.1)' if is_dark else 'rgba(0,0,0,0.1)',
        'grid': 'rgba(255,255,255,0.1)' if is_dark else 'rgba(0,0,0,0.1)'
    }

def create_streak_chart(habits_data, combined=True, habit_name=None, color_theme="green"):
    """Create a GitHub-style streak
    Args:
        habits_data: DataFrame containing habit data
        combined: If True, show combined data for all habits, else show individual habit data
        habit_name: If not combined, specify which habit to display
        color_theme: Color theme to use (green, blue, purple, orange)
    """
    if habits_data.empty:
        return None
        
    colors = get_theme_colors()
    
    # Get current date and date from 52 weeks ago
    end_date = datetime.now()
    start_date = end_date - timedelta(weeks=52)
    
    # Create a date range for the past 52 weeks
    date_range = pd.date_range(start=start_date, end=end_date)
    
    # Define color schemes
    color_schemes = {
        "green": [  #  green theme
            [0, colors['secondary']],  # No contributions
            [0.25, '#9be9a8'],         # Light green
            [0.5, '#40c463'],          # Medium green
            [0.75, '#30a14e'],         # Dark green
            [1, '#216e39']             # Darkest green
        ],
        "blue": [  # Blue theme for nutrition
            [0, colors['secondary']],  # No contributions
            [0.25, '#a6cee3'],         # Light blue
            [0.5, '#6baed6'],          # Medium blue
            [0.75, '#2171b5'],         # Dark blue
            [1, '#08519c']             # Darkest blue
        ],
        "purple": [  # Purple theme
            [0, colors['secondary']],  # No contributions
            [0.25, '#d8aeff'],         # Light purple
            [0.5, '#b77bea'],          # Medium purple
            [0.75, '#8e44ad'],         # Dark purple
            [1, '#5b2c6f']             # Darkest purple
        ],
        "orange": [  # Orange theme
            [0, colors['secondary']],  # No contributions
            [0.25, '#fed976'],         # Light orange
            [0.5, '#fd8d3c'],          # Medium orange
            [0.75, '#e6550d'],         # Dark orange
            [1, '#a63603']             # Darkest orange
        ]
    }
    
    # Select colorscale based on theme
    colorscale = color_schemes.get(color_theme, color_schemes["green"])
    
    # Create figure with subplots
    fig = make_subplots(rows=1, cols=1)
    
    # Filter data for specified habit if not combined
    if not combined and habit_name:
        habits_data = habits_data[habits_data['habit_name'] == habit_name]
        if habits_data.empty:
            return None
    
    # Get check-ins (combined or for single habit)
    all_check_ins = []
    for _, habit in habits_data.iterrows():
        if not pd.isna(habit['check_ins']) and habit['check_ins']:
            all_check_ins.extend(habit['check_ins'].split(','))
    
    z_data = np.zeros((7, 53))  # 7 days (rows) x 53 weeks (columns)
    text_data = np.empty((7, 53), dtype='object')  # For hover text
    
    # Count occurrences of each date in check-ins
    check_in_counts = {}
    for date_str in all_check_ins:
        check_in_counts[date_str] = check_in_counts.get(date_str, 0) + 1
    
    # Max value for color scaling
    max_count = max(check_in_counts.values()) if check_in_counts else 1
    
    current_date = start_date
    for week in range(53):
        for day in range(7):
            # Skip if we've gone past the end date
            if current_date > end_date:
                continue
                
            weekday = current_date.weekday()  # Monday=0, Sunday=6
            date_str = current_date.strftime('%Y-%m-%d')
            
            weekday = (weekday + 1) % 7  # Now Sunday=0, Saturday=6
            
            # Fill cell with count / max_count for color intensity
            count = check_in_counts.get(date_str, 0)
            intensity = count / max_count if max_count > 0 else 0
            z_data[weekday, week] = intensity
            
            #  hover text
            text_data[weekday, week] = f"{date_str}: {count} check-ins"
            
            current_date += timedelta(days=1)
    
    # Create heatmap
    heatmap = go.Heatmap(
        z=z_data,
        x=list(range(53)),  # weeks
        y=list(range(7)),   # days
        colorscale=colorscale,
        showscale=False,
        hoverongaps=False,
        text=text_data,
        hoverinfo='skip',
        xgap=3,  # Gap between cells
        ygap=3   # Gap between cells
    )
    
    fig.add_trace(heatmap)
    
    # Calculate month positions for labels
    month_positions = []
    months_list = []
    current_date = start_date
    
    for week in range(53):
        month = current_date.strftime('%b')
        if month not in months_list:
            months_list.append(month)
            month_positions.append((week, month))
        current_date += timedelta(weeks=1)
    
    # Set title based on mode
    title_text = "Habit Activity (Last 52 Weeks)" if combined else f"{habit_name} Activity"
    
    # Update layout
    fig.update_layout(
        title={
            'text': title_text,
            'y': 0.95,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {'size': 20, 'color': colors['text']}
        },
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=220,
        margin=dict(l=10, r=10, t=50, b=10),
        dragmode=False,
        hovermode=False,
        autosize=False,
        xaxis=dict(
            showgrid=False,
            zeroline=False,
            showticklabels=False,
            side='top',
            fixedrange=True
        ),
        yaxis=dict(
            showgrid=False,
            zeroline=False,
            ticktext=['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'],
            tickvals=list(range(7)),
            tickfont=dict(size=10, color=colors['text']),
            autorange="reversed",
            fixedrange=True
        ),
    )
    
    # Add month labels
    for week, month in month_positions:
        fig.add_annotation(
            x=week,
            y=-0.8,
            text=month,
            showarrow=False,
            font=dict(size=10, color=colors['text']),
            xanchor='center'
        )
    
    # Add legend at the bottom
    fig.add_annotation(
        x=0,
        y=8,
        text="Less",
        showarrow=False,
        font=dict(size=10, color=colors['text']),
        xanchor='left'
    )
    
    # Add colored boxes for legend
    legend_colors = [colorscale[0][1], colorscale[1][1], colorscale[2][1], colorscale[3][1], colorscale[4][1]]
    for i, color in enumerate(legend_colors):
        fig.add_shape(
            type="rect",
            x0=2 + i*2,
            y0=7.7,
            x1=3 + i*2,
            y1=8.3,
            fillcolor=color,
            line=dict(width=1, color=color),
        )
    
    fig.add_annotation(
        x=13,
        y=8,
        text="More",
        showarrow=False,
        font=dict(size=10, color=colors['text']),
        xanchor='left'
    )
    
    return fig

def create_completion_calendar(check_ins):
    """Create a calendar heatmap of habit completions"""
    if not check_ins or pd.isna(check_ins):
        return None
        
    dates = check_ins.split(',')
    colors = get_theme_colors()
    
    # Convert check-ins to datetime objects
    dates = [datetime.strptime(date, '%Y-%m-%d') for date in dates]
    
    # Create a date range from the first check-in to today
    start_date = min(dates)
    end_date = datetime.now()
    date_range = pd.date_range(start=start_date, end=end_date)
    
    # Create a DataFrame with all dates and mark check-ins
    df = pd.DataFrame(index=date_range)
    df['completed'] = df.index.strftime('%Y-%m-%d').isin(dates)
    df['weekday'] = df.index.weekday
    df['week'] = df.index.isocalendar().week
    
    # Create heatmap
    fig = go.Figure(data=go.Heatmap(
        z=df['completed'].astype(int),
        x=df.index,
        y=df['weekday'],
        colorscale=[[0, colors['secondary']], [1, colors['primary']]],
        showscale=False
    ))
    
    fig.update_layout(
        title='Completion Calendar',
        template='none',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(
            color=colors['text'],
            size=14
        ),
        margin=dict(l=10, r=10, t=40, b=10),  # Reduced margins
        xaxis=dict(
            showgrid=False,
            tickfont=dict(color=colors['text']),
            title_font=dict(color=colors['text']),
            tickangle=45
        ),
        yaxis=dict(
            ticktext=['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
            tickvals=[0, 1, 2, 3, 4, 5, 6],
            tickfont=dict(color=colors['text']),
            title_font=dict(color=colors['text'])
        ),
        height=250  # Adjusted height for calendar view
    )
    
    return fig

def create_weekly_summary(check_ins):
    """Create a bar chart showing completions by day of week"""
    if not check_ins or pd.isna(check_ins):
        return None
        
    dates = [datetime.strptime(d, '%Y-%m-%d') for d in check_ins.split(',')]
    days = [d.strftime('%A') for d in dates]
    day_counts = pd.Series(days).value_counts()
    colors = get_theme_colors()
    
    # Ensure all days are represented
    all_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    for day in all_days:
        if day not in day_counts:
            day_counts[day] = 0
    
    # Sort by day of week
    day_counts = day_counts.reindex(all_days)
    
    fig = go.Figure(data=[
        go.Bar(
            x=day_counts.index,
            y=day_counts.values,
            marker_color=colors['primary']
        )
    ])
    
    fig.update_layout(
        title='Weekly Pattern',
        xaxis_title='Day of Week',
        yaxis_title='Completions',
        template='none',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(
            color=colors['text'],
            size=14
        ),
        showlegend=False,
        margin=dict(l=10, r=10, t=40, b=10),  # Reduced margins
        xaxis=dict(
            showgrid=False,
            tickfont=dict(color=colors['text']),
            title_font=dict(color=colors['text']),
            tickangle=45
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor=colors['grid'],
            tickfont=dict(color=colors['text']),
            title_font=dict(color=colors['text']),
            zerolinecolor=colors['grid']
        ),
        height=250  # Adjusted height for weekly summary
    )
    
    return fig
