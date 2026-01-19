import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import date

# Page configuration
st.set_page_config(
    page_title="BMI Calculator",
    page_icon="⚖️",
    layout="centered"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E88E5;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #43A047;
        margin-bottom: 1rem;
    }
    .bmi-value {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .underweight {
        background-color: #B3E5FC;
        color: #0277BD;
    }
    .normal {
        background-color: #C8E6C9;
        color: #2E7D32;
    }
    .overweight {
        background-color: #FFF9C4;
        color: #F9A825;
    }
    .obese {
        background-color: #FFCDD2;
        color: #C62828;
    }
    .info-box {
        background-color: #E3F2FD;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .stButton>button {
        width: 100%;
        background-color: #1E88E5;
        color: white;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Title and description
st.markdown('<h1 class="main-header">⚖️ BMI Calculator</h1>', unsafe_allow_html=True)
st.markdown("""
Body Mass Index (BMI) is a simple calculation using a person's height and weight. 
The formula is BMI = kg/m² where kg is a person's weight in kilograms and m² is 
their height in meters squared.
""")

# Sidebar for additional features
with st.sidebar:
    st.markdown("### 📊 Settings")
    unit_system = st.radio(
        "Select Unit System:",
        ["Metric (kg, cm)", "Imperial (lb, in)"]
    )
    
    st.markdown("---")
    st.markdown("### 📈 Track Progress")
    track_bmi = st.checkbox("Save BMI history")
    
    st.markdown("---")
    st.markdown("### ℹ️ About BMI")
    st.info("""
    **BMI Categories:**
    - Underweight: < 18.5
    - Normal weight: 18.5 - 24.9
    - Overweight: 25 - 29.9
    - Obesity: ≥ 30
    """)

# Initialize session state for BMI history
if 'bmi_history' not in st.session_state:
    st.session_state.bmi_history = []

# Main calculator
st.markdown('<h2 class="sub-header">Calculate Your BMI</h2>', unsafe_allow_html=True)

# Create two columns for input
col1, col2 = st.columns(2)

with col1:
    if unit_system == "Metric (kg, cm)":
        weight = st.number_input(
            "Weight (kg)", 
            min_value=20.0, 
            max_value=200.0, 
            value=70.0, 
            step=0.5,
            help="Enter your weight in kilograms"
        )
        height = st.number_input(
            "Height (cm)", 
            min_value=100.0, 
            max_value=250.0, 
            value=170.0, 
            step=0.5,
            help="Enter your height in centimeters"
        )
        # Convert height to meters for calculation
        height_m = height / 100
    else:
        weight = st.number_input(
            "Weight (lb)", 
            min_value=44.0, 
            max_value=440.0, 
            value=154.0, 
            step=0.5,
            help="Enter your weight in pounds"
        )
        height = st.number_input(
            "Height (in)", 
            min_value=39.0, 
            max_value=98.0, 
            value=67.0, 
            step=0.5,
            help="Enter your height in inches"
        )
        # Convert to metric for calculation
        weight_kg = weight * 0.453592
        height_m = height * 0.0254

with col2:
    st.markdown("### Your Details")
    age = st.slider("Age", 10, 100, 30)
    gender = st.radio("Gender", ["Male", "Female", "Other"])
    
    st.markdown("### Activity Level")
    activity = st.select_slider(
        "Select your activity level",
        options=["Sedentary", "Lightly Active", "Moderately Active", "Very Active", "Extremely Active"]
    )

# Calculate BMI
calculate_button = st.button("Calculate BMI")

if calculate_button:
    # Calculate BMI based on unit system
    if unit_system == "Metric (kg, cm)":
        bmi = weight / (height_m ** 2)
    else:
        bmi = weight_kg / (height_m ** 2)
    
    bmi = round(bmi, 1)
    
    # Determine BMI category
    if bmi < 18.5:
        category = "Underweight"
        color_class = "underweight"
    elif 18.5 <= bmi < 25:
        category = "Normal weight"
        color_class = "normal"
    elif 25 <= bmi < 30:
        category = "Overweight"
        color_class = "overweight"
    else:
        category = "Obesity"
        color_class = "obese"
    
    # Display result
    st.markdown(f'<div class="bmi-value {color_class}">{bmi}</div>', unsafe_allow_html=True)
    
    # Center the category text
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(f'<h3 style="text-align: center;">{category}</h3>', unsafe_allow_html=True)
    
    # Save to history if tracking is enabled
    if track_bmi:
        st.session_state.bmi_history.append({
            'date': date.today().strftime("%Y-%m-%d"),
            'bmi': bmi,
            'category': category,
            'weight': weight,
            'height': height,
            'unit': unit_system.split()[0]
        })
        st.success(f"BMI saved to history!")
    
    # Display additional information
    with st.expander("📋 Detailed Analysis"):
        st.markdown(f"""
        **Your BMI Results:**
        - BMI Value: **{bmi}**
        - Category: **{category}**
        - Age: **{age}**
        - Gender: **{gender}**
        - Activity Level: **{activity}**
        
        **What this means:**
        """)
        
        if category == "Underweight":
            st.markdown("""
            You may need to gain some weight. Consider consulting a doctor or nutritionist 
            for advice on healthy weight gain through a balanced diet and strength training.
            """)
        elif category == "Normal weight":
            st.markdown("""
            You have a healthy body weight for your height. Maintain this with a balanced 
            diet and regular physical activity.
            """)
        elif category == "Overweight":
            st.markdown("""
            You may need to lose some weight for better health. Consider increasing physical 
            activity and making healthy dietary changes.
            """)
        else:
            st.markdown("""
            For health reasons, it's recommended to lose weight. Consult with a healthcare 
            provider for a personalized plan that includes diet, exercise, and lifestyle changes.
            """)
        
        # Calculate healthy weight range
        if unit_system == "Metric (kg, cm)":
            healthy_min = 18.5 * (height_m ** 2)
            healthy_max = 24.9 * (height_m ** 2)
            st.markdown(f"""
            **Healthy weight range for your height ({height} cm):**
            - Minimum: **{healthy_min:.1f} kg**
            - Maximum: **{healthy_max:.1f} kg**
            """)
        else:
            healthy_min_kg = 18.5 * (height_m ** 2)
            healthy_max_kg = 24.9 * (height_m ** 2)
            healthy_min_lb = healthy_min_kg / 0.453592
            healthy_max_lb = healthy_max_kg / 0.453592
            st.markdown(f"""
            **Healthy weight range for your height ({height} in):**
            - Minimum: **{healthy_min_lb:.1f} lb**
            - Maximum: **{healthy_max_lb:.1f} lb**
            """)
    
    # Visualization
    st.markdown("### 📊 BMI Chart")
    
    # Create BMI chart
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Define BMI ranges
    categories = ['Underweight', 'Normal', 'Overweight', 'Obese']
    ranges = ['<18.5', '18.5-24.9', '25-29.9', '30+']
    colors = ['#B3E5FC', '#C8E6C9', '#FFF9C4', '#FFCDD2']
    
    # Create bar chart
    y_pos = np.arange(len(categories))
    ax.barh(y_pos, [18.5, 6.4, 5, 5], left=[0, 18.5, 25, 30], color=colors)
    
    # Mark user's BMI
    ax.axvline(x=bmi, color='red', linestyle='--', linewidth=3, label=f'Your BMI: {bmi}')
    
    # Customize chart
    ax.set_yticks(y_pos)
    ax.set_yticklabels([f'{cat}\n({r})' for cat, r in zip(categories, ranges)])
    ax.set_xlabel('BMI Value')
    ax.set_title('BMI Categories')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    st.pyplot(fig)

# Display BMI history if available
if st.session_state.bmi_history and track_bmi:
    st.markdown("---")
    st.markdown("### 📅 BMI History")
    
    # Convert to DataFrame
    history_df = pd.DataFrame(st.session_state.bmi_history)
    
    # Display table
    st.dataframe(history_df, use_container_width=True)
    
    # Plot trend if we have enough data points
    if len(history_df) > 1:
        st.markdown("#### 📈 BMI Trend Over Time")
        fig2, ax2 = plt.subplots(figsize=(10, 4))
        
        # Convert date strings to datetime for plotting
        history_df['date'] = pd.to_datetime(history_df['date'])
        history_df = history_df.sort_values('date')
        
        ax2.plot(history_df['date'], history_df['bmi'], marker='o', linewidth=2, markersize=8)
        
        # Add reference lines for BMI categories
        ax2.axhline(y=18.5, color='green', linestyle='--', alpha=0.5, label='Underweight/Normal')
        ax2.axhline(y=25, color='orange', linestyle='--', alpha=0.5, label='Normal/Overweight')
        ax2.axhline(y=30, color='red', linestyle='--', alpha=0.5, label='Overweight/Obese')
        
        ax2.set_xlabel('Date')
        ax2.set_ylabel('BMI')
        ax2.set_title('Your BMI Trend')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        plt.xticks(rotation=45)
        
        st.pyplot(fig2)
    
    # Clear history button
    if st.button("Clear History"):
        st.session_state.bmi_history = []
        st.rerun()

# Additional information section
st.markdown("---")
st.markdown("### 📚 Understanding BMI")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    **Limitations of BMI:**
    - Doesn't account for muscle mass
    - Doesn't consider bone density
    - Doesn't differentiate fat distribution
    - May not be accurate for athletes
    - Not suitable for children or pregnant women
    """)

with col2:
    st.markdown("""
    **Healthy Lifestyle Tips:**
    - Eat a balanced diet
    - Exercise regularly
    - Get enough sleep
    - Stay hydrated
    - Manage stress
    - Avoid smoking and limit alcohol
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; font-size: 0.9rem;">
    <p>Note: This BMI calculator is for informational purposes only. 
    Consult a healthcare professional for medical advice.</p>
    <p>Made with ❤️ using Streamlit</p>
</div>
""", unsafe_allow_html=True)