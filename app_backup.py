import streamlit as st
import pandas as pd
import plotly.express as px
import json
from datetime import datetime

# --- EMISSION FACTORS AND DATA ---
# NOTE: These are illustrative values. For a real-world application,
# use scientifically validated, region-specific data.
EMISSION_FACTORS = {
    "India": {
        "Transportation": {
            "Car (Petrol)": 0.192,  # kgCO2e/km
            "Motorcycle": 0.105,   # kgCO2e/km
            "Bus": 0.08,           # kgCO2e/km (assumes average occupancy)
            "Metro/Train": 0.035,  # kgCO2e/km
            "Bicycle/Walk": 0.0
        },
        "Diet": {
            "High Meat Eater": 3300,   # kgCO2e/year
            "Medium Meat Eater": 2500, # kgCO2e/year
            "Vegetarian": 1700,        # kgCO2e/year
            "Vegan": 1500              # kgCO2e/year
        },
        "Electricity": 0.82,  # kgCO2e/kWh (national average)
        "Waste": 0.57         # kgCO2e/kg of unrecycled waste to landfill
    }
}

# --- PAGE CONFIGURATION ---
st.set_page_config(
    layout="wide",
    page_title="Personal Carbon Calculator",
    page_icon="♻️"
)

# --- CUSTOM STYLING ---
st.markdown("""
<style>
    /* Main header styling */
    .main-header {
        color: #2E8B57;
        text-align: center;
        font-size: 3rem;
        margin-bottom: 1rem;
    }
    
    /* Custom metric cards */
    .metric-card {
        background: linear-gradient(45deg, #e8f5e8, #f0fff0);
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #2E8B57;
        margin: 0.5rem 0;
    }
    
    /* Custom button styling */
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
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #f0fff0, #e8f5e8);
    }
    
    /* Hide Streamlit menu and footer */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Custom section headers */
    .section-header {
        color: #2E8B57;
        border-bottom: 2px solid #2E8B57;
        padding-bottom: 0.5rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# --- APP UI AND LOGIC ---
# Sidebar for additional options
with st.sidebar:
    st.markdown('<h3 class="section-header">⚙️ Settings</h3>', unsafe_allow_html=True)
    
    # Theme selector
    theme_color = st.selectbox(
        "🎨 Choose Theme Color",
        ["Green (Default)", "Blue", "Purple", "Orange"],
        help="Select your preferred color theme"
    )
    
    # Update CSS based on theme selection
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
    
    # Additional information
    st.markdown('<h4 class="section-header">📖 About</h4>', unsafe_allow_html=True)
    st.markdown("""
    This calculator estimates your carbon footprint based on:
    - Daily transportation habits
    - Energy consumption
    - Dietary choices  
    - Waste management
    
    **Version:** 2.0  
    **Data:** Based on Indian emission factors
    """)
    
    st.markdown("---")
    
    # Quick tips
    with st.expander("💡 Quick Tips"):
        st.markdown("""
        - **Accuracy**: Use actual data from bills for better estimates
        - **Updates**: Recalculate monthly to track progress  
        - **Goals**: Aim for 2 tonnes CO₂e per year by 2050
        - **Actions**: Focus on your highest emission category first
        """)

st.markdown('<h1 class="main-header">Personal Carbon Calculator App ♻️</h1>', unsafe_allow_html=True)
st.markdown("Calculate your estimated annual carbon footprint and get personalized tips to reduce it.")

# User inputs
st.markdown('<h3 class="section-header">🌍 Your Location</h3>', unsafe_allow_html=True)
# Note: Expanding this would require adding more countries to EMISSION_FACTORS
country = st.selectbox("Select your country", ["India"], help="More countries coming soon!")

st.divider()

# Create tabs for better organization
tab1, tab2 = st.tabs(["🚗 Transportation & 💡 Energy", "🍽️ Lifestyle & 🗑️ Waste"])

with tab1:
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<h4 class="section-header">🚗 Transportation</h4>', unsafe_allow_html=True)
        transport_mode = st.selectbox(
            "Primary mode of daily commute:",
            options=list(EMISSION_FACTORS[country]["Transportation"].keys()),
            help="Choose your most frequently used mode of transportation"
        )
        distance = st.number_input(
            "Daily commute distance (one way, in km):",
            min_value=0.0,
            value=10.0,
            step=0.5,
            help="Enter the distance you travel one way to work/school"
        )
        
        # Add visual indicator
        if distance > 0:
            st.info(f"💡 That's {distance * 2 * 260} km per year!")

    with col2:
        st.markdown('<h4 class="section-header">💡 Electricity</h4>', unsafe_allow_html=True)
        electricity = st.slider(
            "Monthly electricity consumption (in kWh):",
            min_value=0.0,
            max_value=1000.0,
            value=100.0,
            help="Check your electricity bill for accurate consumption"
        )
        
        # Add context
        if electricity < 50:
            st.success("🌟 Great! You're using less electricity than average")
        elif electricity > 200:
            st.warning("⚡ Consider energy-saving measures")

with tab2:
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<h4 class="section-header">🍽️ Diet</h4>', unsafe_allow_html=True)
        diet_type = st.selectbox(
            "Describe your diet:",
            options=list(EMISSION_FACTORS[country]["Diet"].keys()),
            help="Choose the option that best describes your eating habits"
        )
        
        # Add diet impact info
        diet_impact = EMISSION_FACTORS[country]["Diet"][diet_type]
        st.info(f"💡 Your diet choice contributes approximately {diet_impact/1000:.1f} tonnes CO2e annually")

    with col2:
        st.markdown('<h4 class="section-header">🗑️ Waste Management</h4>', unsafe_allow_html=True)
        waste = st.slider(
            "Waste generated per week (in kg):",
            min_value=0.0,
            max_value=50.0,
            value=5.0,
            help="Estimate your household waste including food scraps"
        )
        recycling_pct = st.slider(
            "Percentage of waste you recycle/compost:",
            min_value=0,
            max_value=100,
            value=50,
            help="Include recycling, composting, and reuse"
        )
        
        # Recycling feedback
        if recycling_pct >= 70:
            st.success("♻️ Excellent recycling habits!")
        elif recycling_pct >= 30:
            st.info("👍 Good recycling, room for improvement")
        else:
            st.warning("📈 Consider increasing recycling efforts")

st.divider()

# --- CALCULATION ---
calculate_col1, calculate_col2, calculate_col3 = st.columns([1,2,1])
with calculate_col2:
    if st.button("🔬 Calculate My Carbon Footprint", type="primary", use_container_width=True):
        # 1. Transportation Emissions
        # Yearly distance = daily distance * 2 (round trip) * 260 (working days)
        yearly_distance = distance * 2 * 260
        transportation_emissions = (EMISSION_FACTORS[country]["Transportation"][transport_mode] * yearly_distance) / 1000

        # 2. Electricity Emissions
        yearly_electricity = electricity * 12
        electricity_emissions = (EMISSION_FACTORS[country]["Electricity"] * yearly_electricity) / 1000

        # 3. Diet Emissions
        # This is an annual direct value from the dictionary
        diet_emissions = EMISSION_FACTORS[country]["Diet"][diet_type] / 1000

        # 4. Waste Emissions
        # Yearly waste = weekly waste * 52
        yearly_waste = waste * 52
        unrecycled_waste = yearly_waste * (1 - recycling_pct / 100)
        waste_emissions = (EMISSION_FACTORS[country]["Waste"] * unrecycled_waste) / 1000

        # Total Emissions
        total_emissions = round(
            transportation_emissions + electricity_emissions + diet_emissions + waste_emissions, 2
        )

        # --- ENHANCED RESULTS DISPLAY ---
        st.markdown("---")
        st.markdown('<h2 class="section-header">📊 Your Carbon Footprint Results</h2>', unsafe_allow_html=True)

        # Main result with custom styling
        result_col1, result_col2, result_col3 = st.columns([1,2,1])
        with result_col2:
            st.markdown(f'''
            <div class="metric-card" style="text-align: center;">
                <h3>🌍 Your Total Carbon Footprint</h3>
                <h1 style="color: #2E8B57; font-size: 3rem;">{total_emissions}</h1>
                <h3>tonnes CO₂e per year</h3>
            </div>
            ''', unsafe_allow_html=True)

        # Context and comparison
        st.markdown("---")
        comp_col1, comp_col2, comp_col3 = st.columns(3)
        
        with comp_col1:
            st.metric(
                label="🇮🇳 India Average",
                value="1.9 tonnes",
                delta=f"{total_emissions - 1.9:.1f} vs you"
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

        res_col1, res_col2 = st.columns(2)

        with res_col1:
            # Enhanced breakdown table
            st.markdown('<h4 class="section-header">📋 Detailed Breakdown</h4>', unsafe_allow_html=True)
            emissions_data = {
                "Category": ["🚗 Transportation", "💡 Electricity", "🍽️ Diet", "🗑️ Waste"],
                "Emissions (tonnes CO₂e)": [
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
            # Enhanced Pie Chart
            st.markdown('<h4 class="section-header">📊 Distribution Chart</h4>', unsafe_allow_html=True)
            fig = px.pie(
                emissions_df,
                values='Emissions (tonnes CO₂e)',
                names='Category',
                title='Your Carbon Footprint Distribution',
                hole=.4,
                color_discrete_sequence=['#2E8B57', '#32CD32', '#90EE90', '#98FB98']
            )
            fig.update_traces(textposition='inside', textinfo='percent+label')
            fig.update_layout(
                showlegend=True,
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                font=dict(size=12)
            )
            st.plotly_chart(fig, use_container_width=True)

        st.divider()

        # --- ENHANCED PERSONALIZED RECOMMENDATIONS ---
        st.markdown('<h2 class="section-header">💡 Your Personalized Action Plan</h2>', unsafe_allow_html=True)
        
        # Find the category with the highest emissions
        highest_emission_category = emissions_df.loc[emissions_df['Emissions (tonnes CO₂e)'].idxmax()]
        
        # Priority recommendations based on highest impact
        st.markdown(f"""
        <div class="metric-card">
            <h4>🎯 Priority Focus Area</h4>
            <p><strong>{highest_emission_category['Category']}</strong> is your biggest contributor at 
            <strong>{highest_emission_category['Emissions (tonnes CO₂e)']} tonnes</strong> 
            ({highest_emission_category['Percentage']} of your total footprint)</p>
        </div>
        """, unsafe_allow_html=True)

        # Create recommendation tabs
        rec_tab1, rec_tab2, rec_tab3 = st.tabs(["🚀 Quick Wins", "📈 Long-term Goals", "🌱 Eco-friendly Tips"])
        
        with rec_tab1:
            if highest_emission_category["Category"] == "🚗 Transportation":
                st.markdown("""
                **🚗 Immediate Transportation Actions:**
                - 🚌 **Try public transport** 2 days this week (could save ~20% of transport emissions)
                - 🚶‍♂️ **Walk or bike** for trips under 2km
                - 🤝 **Carpool** with colleagues - even once a week makes a difference
                - 📱 **Combine errands** into single trips
                """)
            elif "Diet" in highest_emission_category["Category"]:
                st.markdown("""
                **🍽️ Immediate Diet Changes:**
                - 🥗 **Try one plant-based meal** per day this week
                - 🥩 **Choose smaller portions** of meat when you do eat it
                - 🏪 **Buy local produce** from nearby farmers markets
                - 🧊 **Reduce food waste** by meal planning
                """)
            elif "Electricity" in highest_emission_category["Category"]:
                st.markdown("""
                **💡 Immediate Energy Actions:**
                - 🔌 **Unplug devices** when not in use (saves 5-10% electricity)
                - 🌡️ **Adjust thermostat** by 2°C (saves ~10% on heating/cooling)
                - 💡 **Switch to LED bulbs** in your most-used rooms
                - ☀️ **Use natural light** during the day instead of artificial lighting
                """)
            else:
                st.markdown("""
                **🗑️ Immediate Waste Actions:**
                - ♻️ **Set up separate bins** for recycling in your home
                - 🥬 **Start composting** kitchen scraps this week
                - 👜 **Use reusable bags** for all shopping trips
                - 📱 **Go paperless** for bills and statements
                """)

        with rec_tab2:
            st.markdown("""
            **🎯 3-Month Goals:**
            - 📊 **Track progress** monthly using this calculator
            - 🔄 **Switch to renewable energy** provider if available
            - 🌱 **Plant trees** or support reforestation projects
            - 🏠 **Improve home insulation** to reduce energy needs
            
            **📅 Annual Goals:**
            - 🚗 **Consider electric/hybrid vehicle** for next car purchase
            - 🏡 **Energy audit** of your home
            - 🌍 **Carbon offset** remaining emissions through verified projects
            - 📚 **Educate family/friends** about carbon footprint reduction
            """)

        with rec_tab3:
            st.markdown("""
            **🌿 Nature-Based Solutions:**
            - 🌳 **Support local tree planting** initiatives
            - 🌱 **Start a home garden** to grow your own vegetables
            - 🐝 **Create pollinator-friendly spaces** with native plants
            - 💧 **Harvest rainwater** for garden irrigation
            
            **💡 Smart Technology:**
            - 📱 **Use apps** to track your carbon footprint daily
            - 🏠 **Smart home devices** to optimize energy use
            - 🚗 **Route planning apps** to reduce driving time
            - 🛒 **Choose carbon-neutral delivery** options when shopping online
            """)
        
        # Impact calculator for quick actions
        st.markdown("---")
        st.markdown('<h4 class="section-header">📈 Potential Annual Savings</h4>', unsafe_allow_html=True)
        
        savings_col1, savings_col2, savings_col3 = st.columns(3)
        
        with savings_col1:
            if transportation_emissions > 0:
                transport_savings = transportation_emissions * 0.3  # 30% potential reduction
                st.metric("🚗 Transport Optimization", f"-{transport_savings:.1f} tonnes", "30% reduction possible")
        
        with savings_col2:
            if diet_emissions > 0:
                diet_savings = diet_emissions * 0.25  # 25% potential reduction
                st.metric("🍽️ Diet Adjustments", f"-{diet_savings:.1f} tonnes", "25% reduction possible")
                
        with savings_col3:
            if electricity_emissions > 0:
                energy_savings = electricity_emissions * 0.20  # 20% potential reduction
                st.metric("💡 Energy Efficiency", f"-{energy_savings:.1f} tonnes", "20% reduction possible")
        
        # Data export and tracking
        st.markdown("---")
        st.markdown('<h4 class="section-header">📊 Export & Track Progress</h4>', unsafe_allow_html=True)
        
        # Prepare data for export
        export_data = {
            "Date": datetime.now().strftime("%Y-%m-%d"),
            "Total_Emissions": total_emissions,
            "Transportation": round(transportation_emissions, 2),
            "Electricity": round(electricity_emissions, 2),
            "Diet": round(diet_emissions, 2),
            "Waste": round(waste_emissions, 2),
            "Transport_Mode": transport_mode,
            "Daily_Distance": distance,
            "Monthly_Electricity": electricity,
            "Diet_Type": diet_type,
            "Weekly_Waste": waste,
            "Recycling_Percentage": recycling_pct
        }
        
        export_col1, export_col2 = st.columns(2)
        
        with export_col1:
            # JSON download
            json_data = json.dumps(export_data, indent=2)
            st.download_button(
                label="📥 Download Results (JSON)",
                data=json_data,
                file_name=f"carbon_footprint_{datetime.now().strftime('%Y%m%d')}.json",
                mime="application/json"
            )
            
        with export_col2:
            # CSV download
            df_export = pd.DataFrame([export_data])
            csv_data = df_export.to_csv(index=False)
            st.download_button(
                label="📊 Download Results (CSV)",
                data=csv_data,
                file_name=f"carbon_footprint_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
