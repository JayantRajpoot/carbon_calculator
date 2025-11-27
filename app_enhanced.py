import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
from datetime import datetime
from storage import CarbonFootprintStorage
import os

# Initialize storage
storage = CarbonFootprintStorage()

# Load emission factors from JSON
@st.cache_data
def load_emission_factors():
    """Load emission factors from JSON file."""
    try:
        with open('emission_factors.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        st.error("⚠️ emission_factors.json not found!")
        return {}

EMISSION_FACTORS = load_emission_factors()

# Achievement badges configuration
BADGES = {
    "first_calculation": {"icon": "🎯", "title": "First Step", "description": "Completed first calculation"},
    "under_3_tonnes": {"icon": "🌟", "title": "Low Carbon Hero", "description": "Under 3 tonnes CO₂e"},
    "under_2_tonnes": {"icon": "💚", "title": "Climate Champion", "description": "Under 2 tonnes CO₂e"},
    "10_calculations": {"icon": "📊", "title": "Tracker", "description": "10 calculations completed"},
    "improving_trend": {"icon": "📉", "title": "Improving", "description": "Downward emissions trend"},
    "transport_optimizer": {"icon": "🚲", "title": "Green Commuter", "description": "Using eco-friendly transport"},
    "vegetarian": {"icon": "🥗", "title": "Plant Powered", "description": "Vegetarian or Vegan diet"},
    "recycler": {"icon": "♻️", "title": "Recycling Pro", "description": "70%+ recycling rate"}
}

def check_badges(calc_data, stats):
    """Check which badges user has earned."""
    earned = []
    
    if stats["total_calculations"] >= 1:
        earned.append("first_calculation")
    
    if calc_data.get("total_emissions", 999) < 3:
        earned.append("under_3_tonnes")
    
    if calc_data.get("total_emissions", 999) < 2:
        earned.append("under_2_tonnes")
    
    if stats["total_calculations"] >= 10:
        earned.append("10_calculations")
    
    if stats.get("trend") == "improving":
        earned.append("improving_trend")
    
    if calc_data.get("transport_mode") in ["Bicycle/Walk", "Metro/Train", "Electric Vehicle"]:
        earned.append("transport_optimizer")
    
    if calc_data.get("diet_type") in ["Vegetarian", "Vegan"]:
        earned.append("vegetarian")
    
    if calc_data.get("recycling_pct", 0) >= 70:
        earned.append("recycler")
    
    return earned

# --- PAGE CONFIGURATION ---
st.set_page_config(
    layout="wide",
    page_title="Personal Carbon Calculator Pro",
    page_icon="♻️"
)

# --- CUSTOM STYLING ---
st.markdown("""
<style>
    .main-header {
        color: #2E8B57;
        text-align: center;
        font-size: 3rem;
        margin-bottom: 1rem;
    }
    
    .metric-card {
        background: linear-gradient(45deg, #e8f5e8, #f0fff0);
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #2E8B57;
        margin: 0.5rem 0;
    }
    
    .stButton > button {
        background: linear-gradient(45deg, #2E8B57, #32CD32);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.5rem 2rem;
        font-weight: bold;
        transition: all 0.3s;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(46, 139, 87, 0.3);
    }
    
    .section-header {
        color: #2E8B57;
        border-bottom: 2px solid #2E8B57;
        padding-bottom: 0.5rem;
        margin: 1rem 0;
    }
    
    .badge-container {
        display: inline-block;
        background: #f0f0f0;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        margin: 0.25rem;
        text-align: center;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.markdown('<h3 class="section-header">⚙️ Settings</h3>', unsafe_allow_html=True)
    
    # Theme selector
    theme_color = st.selectbox(
        "🎨 Theme Color",
        ["Green (Default)", "Blue", "Purple", "Orange"],
        help="Select your preferred color theme"
    )
    
    color_map = {
        "Green (Default)": "#2E8B57",
        "Blue": "#4682B4", 
        "Purple": "#663399",
        "Orange": "#FF8C00"
    }
    
    if theme_color != "Green (Default)":
        selected_color = color_map[theme_color]
        st.markdown(f"""
        <style>
            .main-header, .section-header {{ color: {selected_color} !important; }}
            .stButton > button {{ background: linear-gradient(45deg, {selected_color}, {selected_color}99) !important; }}
            .metric-card {{ border-left-color: {selected_color} !important; }}
        </style>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Statistics
    stats = storage.get_statistics()
    st.markdown('<h4 class="section-header">📊 Your Stats</h4>', unsafe_allow_html=True)
    st.metric("Total Calculations", stats["total_calculations"])
    if stats["total_calculations"] > 0:
        st.metric("Average Footprint", f"{stats['average_footprint']} tonnes")
        st.metric("Lowest Recorded", f"{stats['lowest_footprint']} tonnes")
        
        # Trend indicator
        trend_emoji = {"improving": "📉", "worsening": "📈", "neutral": "➡️"}
        st.info(f"{trend_emoji[stats['trend']]} Trend: {stats['trend'].capitalize()}")
    
    st.markdown("---")
    
    # Goal setting
    st.markdown('<h4 class="section-header">🎯 Goal Setting</h4>', unsafe_allow_html=True)
    active_goal = storage.get_active_goal()
    
    if active_goal:
        st.success(f"Active Goal: {active_goal['target_emissions']} tonnes by {active_goal['target_date']}")
        if st.button("Clear Goal"):
            storage.save_goal({})
            st.rerun()
    else:
        with st.form("goal_form"):
            target_emissions = st.number_input("Target Emissions (tonnes/year)", min_value=0.0, value=2.0, step=0.1)
            target_date = st.date_input("Target Date")
            
            if st.form_submit_button("Set Goal"):
                storage.save_goal({
                    "target_emissions": target_emissions,
                    "target_date": str(target_date)
                })
                st.success("Goal saved!")
                st.rerun()
    
    st.markdown("---")
    
    # Data management
    st.markdown('<h4 class="section-header">💾 Data</h4>', unsafe_allow_html=True)
    if st.button("Clear All History"):
        if storage.clear_history():
            st.success("History cleared!")
            st.rerun()

# --- MAIN CONTENT ---
st.markdown('<h1 class="main-header">Personal Carbon Calculator Pro ♻️</h1>', unsafe_allow_html=True)
st.markdown("Advanced carbon footprint calculator with tracking, goals, and personalized insights.")

# Create main tabs
main_tab1, main_tab2, main_tab3, main_tab4 = st.tabs(["📝 Calculate", "📊 History & Trends", "🎯 Scenario Comparison", "🏆 Achievements"])

with main_tab1:
    # Location
    st.markdown('<h3 class="section-header">🌍 Your Location</h3>', unsafe_allow_html=True)
    country = st.selectbox("Select your country", list(EMISSION_FACTORS.keys()), help="Emission factors vary by region")
    
    st.divider()
    
    # Input tabs
    input_tab1, input_tab2 = st.tabs(["🚗 Transportation & 💡 Energy", "🍽️ Lifestyle & 🗑️ Waste"])
    
    with input_tab1:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<h4 class="section-header">🚗 Transportation</h4>', unsafe_allow_html=True)
            transport_mode = st.selectbox(
                "Primary mode of daily commute:",
                options=list(EMISSION_FACTORS[country]["Transportation"].keys()),
                help="Choose your most frequently used mode"
            )
            distance = st.number_input(
                "Daily commute distance (one way, in km):",
                min_value=0.0,
                value=10.0,
                step=0.5
            )
            
            if distance > 0:
                st.info(f"💡 That's {distance * 2 * 260:.0f} km per year!")
        
        with col2:
            st.markdown('<h4 class="section-header">💡 Electricity</h4>', unsafe_allow_html=True)
            electricity = st.slider(
                "Monthly electricity consumption (in kWh):",
                min_value=0.0,
                max_value=1000.0,
                value=100.0
            )
            
            if electricity < 50:
                st.success("🌟 Great! Low electricity usage")
            elif electricity > 200:
                st.warning("⚡ Consider energy-saving measures")
    
    with input_tab2:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<h4 class="section-header">🍽️ Diet</h4>', unsafe_allow_html=True)
            diet_type = st.selectbox(
                "Describe your diet:",
                options=list(EMISSION_FACTORS[country]["Diet"].keys())
            )
            
            diet_impact = EMISSION_FACTORS[country]["Diet"][diet_type]
            st.info(f"💡 Diet contributes ~{diet_impact/1000:.1f} tonnes CO₂e annually")
        
        with col2:
            st.markdown('<h4 class="section-header">🗑️ Waste Management</h4>', unsafe_allow_html=True)
            waste = st.slider(
                "Waste generated per week (in kg):",
                min_value=0.0,
                max_value=50.0,
                value=5.0
            )
            recycling_pct = st.slider(
                "Percentage recycled/composted:",
                min_value=0,
                max_value=100,
                value=50
            )
            
            if recycling_pct >= 70:
                st.success("♻️ Excellent recycling!")
            elif recycling_pct >= 30:
                st.info("👍 Good recycling")
            else:
                st.warning("📈 Increase recycling efforts")
    
    st.divider()
    
    # Calculate button
    calc_col1, calc_col2, calc_col3 = st.columns([1,2,1])
    with calc_col2:
        calculate_button = st.button("🔬 Calculate My Carbon Footprint", type="primary", use_container_width=True)
    
    if calculate_button:
        # Calculations
        yearly_distance = distance * 2 * 260
        transportation_emissions = (EMISSION_FACTORS[country]["Transportation"][transport_mode] * yearly_distance) / 1000
        
        yearly_electricity = electricity * 12
        electricity_emissions = (EMISSION_FACTORS[country]["Electricity"] * yearly_electricity) / 1000
        
        diet_emissions = EMISSION_FACTORS[country]["Diet"][diet_type] / 1000
        
        yearly_waste = waste * 52
        unrecycled_waste = yearly_waste * (1 - recycling_pct / 100)
        waste_emissions = (EMISSION_FACTORS[country]["Waste"] * unrecycled_waste) / 1000
        
        total_emissions = round(transportation_emissions + electricity_emissions + diet_emissions + waste_emissions, 2)
        
        # Save calculation
        calc_data = {
            "timestamp": datetime.now().isoformat(),
            "country": country,
            "total_emissions": total_emissions,
            "transportation": round(transportation_emissions, 2),
            "electricity": round(electricity_emissions, 2),
            "diet": round(diet_emissions, 2),
            "waste": round(waste_emissions, 2),
            "transport_mode": transport_mode,
            "daily_distance": distance,
            "monthly_electricity": electricity,
            "diet_type": diet_type,
            "weekly_waste": waste,
            "recycling_pct": recycling_pct
        }
        storage.save_calculation(calc_data)
        
        # Display results
        st.markdown("---")
        st.markdown('<h2 class="section-header">📊 Your Results</h2>', unsafe_allow_html=True)
        
        result_col1, result_col2, result_col3 = st.columns([1,2,1])
        with result_col2:
            st.markdown(f'''
            <div class="metric-card" style="text-align: center;">
                <h3 style="color: #000000; margin: 0.25rem 0 0.5rem 0;">🌍 Your Total Carbon Footprint</h3>
                <h1 style="color: #000000; font-size: 3.25rem; font-weight: 700; margin: 0;">{total_emissions}</h1>
                <h3 style="color: #000000; margin-top: 0.25rem;">tonnes CO₂e per year</h3>
            </div>
            ''', unsafe_allow_html=True)
        
        # Goal progress
        active_goal = storage.get_active_goal()
        if active_goal:
            st.markdown("---")
            goal_col1, goal_col2, goal_col3 = st.columns([1,2,1])
            with goal_col2:
                target = active_goal["target_emissions"]
                progress = min(100, (1 - (total_emissions - target) / total_emissions) * 100) if total_emissions > 0 else 0
                st.markdown('<h4 class="section-header">🎯 Goal Progress</h4>', unsafe_allow_html=True)
                st.progress(max(0, progress / 100))
                
                if total_emissions <= target:
                    st.success(f"🎉 Congratulations! You've achieved your goal of {target} tonnes!")
                else:
                    diff = round(total_emissions - target, 2)
                    st.info(f"📊 {diff} tonnes to go to reach your goal of {target} tonnes")
        
        # Comparisons
        st.markdown("---")
        comp_col1, comp_col2, comp_col3 = st.columns(3)
        
        benchmarks = {
            "India": 1.9,
            "USA": 15.5,
            "UK": 5.5,
            "China": 8.0,
            "Australia": 15.4,
            "Global Average": 4.7
        }
        
        with comp_col1:
            country_avg = benchmarks.get(country, 4.7)
            st.metric(
                label=f"🇮🇳 {country} Average",
                value=f"{country_avg} tonnes",
                delta=f"{total_emissions - country_avg:.1f} vs you"
            )
        
        with comp_col2:
            st.metric(
                label="🌍 Global Average", 
                value="4.7 tonnes",
                delta=f"{total_emissions - 4.7:.1f} vs you"
            )
        
        with comp_col3:
            st.metric(
                label="🎯 2050 Target",
                value="2.0 tonnes",
                delta=f"{total_emissions - 2.0:.1f} to target"
            )
        
        st.divider()
        
        # Breakdown
        res_col1, res_col2 = st.columns(2)
        
        with res_col1:
            st.markdown('<h4 class="section-header">📋 Detailed Breakdown</h4>', unsafe_allow_html=True)
            emissions_data = {
                "Category": ["🚗 Transportation", "💡 Electricity", "🍽️ Diet", "🗑️ Waste"],
                "Emissions (tonnes)": [
                    round(transportation_emissions, 2),
                    round(electricity_emissions, 2),
                    round(diet_emissions, 2),
                    round(waste_emissions, 2)
                ],
                "Percentage": [
                    f"{round((transportation_emissions/total_emissions)*100, 1)}%",
                    f"{round((electricity_emissions/total_emissions)*100, 1)}%",
                    f"{round((diet_emissions/total_emissions)*100, 1)}%",
                    f"{round((waste_emissions/total_emissions)*100, 1)}%"
                ]
            }
            emissions_df = pd.DataFrame(emissions_data)
            st.dataframe(emissions_df, use_container_width=True, hide_index=True)
        
        with res_col2:
            st.markdown('<h4 class="section-header">📊 Distribution</h4>', unsafe_allow_html=True)
            fig = px.pie(
                emissions_df,
                values='Emissions (tonnes)',
                names='Category',
                hole=.4,
                color_discrete_sequence=['#2E8B57', '#32CD32', '#90EE90', '#98FB98']
            )
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True)
        
        st.divider()
        
        # Action Simulator
        st.markdown('<h2 class="section-header">🎮 Action Simulator</h2>', unsafe_allow_html=True)
        st.markdown("See how different actions would impact your footprint:")
        
        sim_col1, sim_col2 = st.columns(2)
        
        with sim_col1:
            st.markdown("**🚗 Transportation Actions:**")
            action_bike_2days = st.checkbox("Bike/walk 2 days per week (20% reduction)")
            action_carpool = st.checkbox("Carpool 3 days per week (30% reduction)")
            action_public_transport = st.checkbox("Switch to public transport (60% reduction)")
            
            st.markdown("**💡 Energy Actions:**")
            action_led_bulbs = st.checkbox("Switch to LED bulbs (15% reduction)")
            action_solar = st.checkbox("Install solar panels (50% reduction)")
            action_appliances = st.checkbox("Energy-efficient appliances (20% reduction)")
        
        with sim_col2:
            st.markdown("**🍽️ Diet Actions:**")
            action_reduce_meat = st.checkbox("Reduce meat by 50%")
            action_vegetarian = st.checkbox("Go vegetarian")
            action_local_food = st.checkbox("Buy local food (10% reduction)")
            
            st.markdown("**🗑️ Waste Actions:**")
            action_compost = st.checkbox("Start composting (30% reduction)")
            action_recycle_more = st.checkbox("Increase recycling to 80%")
            action_reduce_waste = st.checkbox("Reduce waste by 25%")
        
        # Calculate simulated emissions
        sim_transport = transportation_emissions
        sim_electricity = electricity_emissions
        sim_diet = diet_emissions
        sim_waste = waste_emissions
        
        if action_bike_2days:
            sim_transport *= 0.8
        if action_carpool:
            sim_transport *= 0.7
        if action_public_transport:
            sim_transport *= 0.4
        
        if action_led_bulbs:
            sim_electricity *= 0.85
        if action_solar:
            sim_electricity *= 0.5
        if action_appliances:
            sim_electricity *= 0.8
        
        if action_reduce_meat:
            current_diet_index = list(EMISSION_FACTORS[country]["Diet"].keys()).index(diet_type)
            if current_diet_index > 0:
                sim_diet = EMISSION_FACTORS[country]["Diet"][list(EMISSION_FACTORS[country]["Diet"].keys())[current_diet_index - 1]] / 1000
        if action_vegetarian:
            sim_diet = EMISSION_FACTORS[country]["Diet"]["Vegetarian"] / 1000
        if action_local_food:
            sim_diet *= 0.9
        
        if action_compost:
            sim_waste *= 0.7
        if action_recycle_more:
            new_unrecycled = yearly_waste * 0.2
            sim_waste = (EMISSION_FACTORS[country]["Waste"] * new_unrecycled) / 1000
        if action_reduce_waste:
            sim_waste *= 0.75
        
        simulated_total = round(sim_transport + sim_electricity + sim_diet + sim_waste, 2)
        savings = round(total_emissions - simulated_total, 2)
        savings_pct = round((savings / total_emissions) * 100, 1) if total_emissions > 0 else 0
        
        st.markdown("---")
        st.markdown('<h4 class="section-header">🎯 Simulated Impact</h4>', unsafe_allow_html=True)
        
        sim_res_col1, sim_res_col2, sim_res_col3 = st.columns(3)
        
        with sim_res_col1:
            st.metric("Current Footprint", f"{total_emissions} tonnes")
        
        with sim_res_col2:
            st.metric("Simulated Footprint", f"{simulated_total} tonnes", delta=f"-{savings} tonnes")
        
        with sim_res_col3:
            st.metric("Potential Savings", f"{savings_pct}%", delta=f"{savings} tonnes saved")
        
        # Savings visualization
        if savings > 0:
            comparison_df = pd.DataFrame({
                "Scenario": ["Current", "With Actions"],
                "Emissions": [total_emissions, simulated_total]
            })
            
            fig_comparison = px.bar(
                comparison_df,
                x="Scenario",
                y="Emissions",
                color="Scenario",
                title="Current vs Optimized Emissions",
                color_discrete_sequence=['#FF6B6B', '#4ECDC4']
            )
            st.plotly_chart(fig_comparison, use_container_width=True)

with main_tab2:
    st.markdown('<h2 class="section-header">📊 Your History & Trends</h2>', unsafe_allow_html=True)
    
    calculations = storage.get_calculations()
    
    if not calculations:
        st.info("📭 No calculation history yet. Complete your first calculation to see trends!")
    else:
        # Time series chart
        st.markdown('<h4 class="section-header">📈 Emissions Over Time</h4>', unsafe_allow_html=True)
        
        df_history = pd.DataFrame(calculations)
        df_history['date'] = pd.to_datetime(df_history['timestamp']).dt.date
        df_history = df_history.sort_values('date')
        
        fig_timeline = go.Figure()
        
        fig_timeline.add_trace(go.Scatter(
            x=df_history['date'],
            y=df_history['total_emissions'],
            mode='lines+markers',
            name='Total Emissions',
            line=dict(color='#2E8B57', width=3),
            marker=dict(size=8)
        ))
        
        # Add goal line if exists
        active_goal = storage.get_active_goal()
        if active_goal:
            fig_timeline.add_hline(
                y=active_goal["target_emissions"],
                line_dash="dash",
                line_color="red",
                annotation_text=f"Goal: {active_goal['target_emissions']} tonnes"
            )
        
        fig_timeline.update_layout(
            title="Carbon Footprint Timeline",
            xaxis_title="Date",
            yaxis_title="Emissions (tonnes CO₂e)",
            hovermode='x unified'
        )
        
        st.plotly_chart(fig_timeline, use_container_width=True)
        
        # Category breakdown over time
        st.markdown('<h4 class="section-header">📊 Category Trends</h4>', unsafe_allow_html=True)
        
        fig_categories = go.Figure()
        
        fig_categories.add_trace(go.Scatter(
            x=df_history['date'],
            y=df_history['transportation'],
            name='Transportation',
            stackgroup='one',
            fillcolor='#2E8B57'
        ))
        
        fig_categories.add_trace(go.Scatter(
            x=df_history['date'],
            y=df_history['electricity'],
            name='Electricity',
            stackgroup='one',
            fillcolor='#32CD32'
        ))
        
        fig_categories.add_trace(go.Scatter(
            x=df_history['date'],
            y=df_history['diet'],
            name='Diet',
            stackgroup='one',
            fillcolor='#90EE90'
        ))
        
        fig_categories.add_trace(go.Scatter(
            x=df_history['date'],
            y=df_history['waste'],
            name='Waste',
            stackgroup='one',
            fillcolor='#98FB98'
        ))
        
        fig_categories.update_layout(
            title="Emissions by Category Over Time",
            xaxis_title="Date",
            yaxis_title="Emissions (tonnes CO₂e)",
            hovermode='x unified'
        )
        
        st.plotly_chart(fig_categories, use_container_width=True)
        
        # History table
        st.markdown('<h4 class="section-header">📋 Calculation History</h4>', unsafe_allow_html=True)
        
        display_df = df_history[['date', 'total_emissions', 'transportation', 'electricity', 'diet', 'waste', 'country']].copy()
        display_df.columns = ['Date', 'Total', 'Transport', 'Electricity', 'Diet', 'Waste', 'Country']
        
        st.dataframe(display_df, use_container_width=True, hide_index=True)
        
        # Export history
        csv_data = display_df.to_csv(index=False)
        st.download_button(
            label="📥 Download History (CSV)",
            data=csv_data,
            file_name=f"carbon_history_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )

with main_tab3:
    st.markdown('<h2 class="section-header">🎯 Scenario Comparison</h2>', unsafe_allow_html=True)
    st.markdown("Compare different lifestyle scenarios side-by-side.")
    
    scenario_col1, scenario_col2 = st.columns(2)
    
    with scenario_col1:
        st.markdown('<h4 class="section-header">📊 Scenario A: High Carbon</h4>', unsafe_allow_html=True)
        
        if country in EMISSION_FACTORS:
            # High carbon scenario
            high_transport = EMISSION_FACTORS[country]["Transportation"].get("Car (Petrol)", 0.192) * 50 * 2 * 260 / 1000
            high_electricity = EMISSION_FACTORS[country]["Electricity"] * 300 * 12 / 1000
            high_diet = EMISSION_FACTORS[country]["Diet"].get("High Meat Eater", 3300) / 1000
            high_waste = EMISSION_FACTORS[country]["Waste"] * 10 * 52 * 0.8 / 1000
            high_total = round(high_transport + high_electricity + high_diet + high_waste, 2)
            
            st.metric("Total Emissions", f"{high_total} tonnes")
            st.markdown(f"""
            - 🚗 Car commute: 50km/day
            - 💡 Electricity: 300 kWh/month
            - 🍽️ High meat diet
            - 🗑️ 10kg waste/week, 20% recycling
            """)
            
            scenario_a_data = {
                "Category": ["Transport", "Electricity", "Diet", "Waste"],
                "Emissions": [high_transport, high_electricity, high_diet, high_waste]
            }
    
    with scenario_col2:
        st.markdown('<h4 class="section-header">🌱 Scenario B: Low Carbon</h4>', unsafe_allow_html=True)
        
        if country in EMISSION_FACTORS:
            # Low carbon scenario
            low_transport = EMISSION_FACTORS[country]["Transportation"].get("Metro/Train", 0.035) * 10 * 2 * 260 / 1000
            low_electricity = EMISSION_FACTORS[country]["Electricity"] * 80 * 12 / 1000
            low_diet = EMISSION_FACTORS[country]["Diet"].get("Vegetarian", 1700) / 1000
            low_waste = EMISSION_FACTORS[country]["Waste"] * 3 * 52 * 0.2 / 1000
            low_total = round(low_transport + low_electricity + low_diet + low_waste, 2)
            
            st.metric("Total Emissions", f"{low_total} tonnes")
            st.markdown(f"""
            - 🚲 Metro/bike: 10km/day
            - 💡 Electricity: 80 kWh/month
            - 🥗 Vegetarian diet
            - ♻️ 3kg waste/week, 80% recycling
            """)
            
            scenario_b_data = {
                "Category": ["Transport", "Electricity", "Diet", "Waste"],
                "Emissions": [low_transport, low_electricity, low_diet, low_waste]
            }
    
    # Comparison visualization
    st.markdown("---")
    st.markdown('<h4 class="section-header">📊 Side-by-Side Comparison</h4>', unsafe_allow_html=True)
    
    comparison_data = pd.DataFrame({
        "Category": ["Transport", "Electricity", "Diet", "Waste"] * 2,
        "Scenario": ["High Carbon"] * 4 + ["Low Carbon"] * 4,
        "Emissions": [high_transport, high_electricity, high_diet, high_waste, 
                     low_transport, low_electricity, low_diet, low_waste]
    })
    
    fig_scenarios = px.bar(
        comparison_data,
        x="Category",
        y="Emissions",
        color="Scenario",
        barmode="group",
        title="Emissions Comparison by Category",
        color_discrete_sequence=['#FF6B6B', '#4ECDC4']
    )
    
    st.plotly_chart(fig_scenarios, use_container_width=True)
    
    # Savings calculation
    savings_amount = round(high_total - low_total, 2)
    savings_percent = round((savings_amount / high_total) * 100, 1) if high_total > 0 else 0
    
    st.success(f"💚 Potential Savings: {savings_amount} tonnes ({savings_percent}% reduction) by switching to a low-carbon lifestyle!")

with main_tab4:
    st.markdown('<h2 class="section-header">🏆 Your Achievements</h2>', unsafe_allow_html=True)
    
    # Get latest calculation for badge checking
    latest_calc = storage.get_latest_calculation()
    stats = storage.get_statistics()
    
    if latest_calc:
        earned_badges = check_badges(latest_calc, stats)
        
        st.markdown(f"### You've earned {len(earned_badges)} badge(s)!")
        
        # Display earned badges
        badge_cols = st.columns(4)
        col_idx = 0
        
        for badge_id, badge in BADGES.items():
            with badge_cols[col_idx % 4]:
                if badge_id in earned_badges:
                    st.markdown(f"""
                    <div class="badge-container" style="background: linear-gradient(45deg, #FFD700, #FFA500);">
                        <div style="font-size: 2rem;">{badge['icon']}</div>
                        <div style="font-weight: bold;">{badge['title']}</div>
                        <div style="font-size: 0.8rem;">{badge['description']}</div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="badge-container" style="background: #e0e0e0; opacity: 0.5;">
                        <div style="font-size: 2rem;">{badge['icon']}</div>
                        <div style="font-weight: bold;">{badge['title']}</div>
                        <div style="font-size: 0.8rem;">{badge['description']}</div>
                    </div>
                    """, unsafe_allow_html=True)
                col_idx += 1
        
        st.markdown("---")
        
        # Progress to next badges
        st.markdown('<h4 class="section-header">🎯 Progress to Next Badges</h4>', unsafe_allow_html=True)
        
        prog_col1, prog_col2 = st.columns(2)
        
        with prog_col1:
            if "10_calculations" not in earned_badges:
                progress_to_10 = min(100, (stats["total_calculations"] / 10) * 100)
                st.markdown("**📊 Tracker Badge**")
                st.progress(progress_to_10 / 100)
                st.caption(f"{stats['total_calculations']}/10 calculations completed")
        
        with prog_col2:
            if "under_2_tonnes" not in earned_badges:
                current_emissions = latest_calc.get("total_emissions", 999)
                if current_emissions > 2:
                    reduction_needed = round(current_emissions - 2, 2)
                    st.markdown("**💚 Climate Champion Badge**")
                    st.caption(f"Reduce by {reduction_needed} tonnes to reach under 2 tonnes")
    else:
        st.info("📭 Complete your first calculation to start earning badges!")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    <p><strong>Personal Carbon Calculator Pro v3.0</strong></p>
    <p>Data sources: IPCC, national environmental agencies. Calculations are estimates.</p>
    <p style="margin-top: 1rem; font-size: 0.9rem;">
        This is a college group project by <strong>Jayant Rajput, Aditya Pratap, Aarav Gupta</strong>
    </p>
</div>
""", unsafe_allow_html=True)

