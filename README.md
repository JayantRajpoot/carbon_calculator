# Personal Carbon Calculator Pro 🌍♻️

An advanced carbon footprint calculator with comprehensive tracking, goal setting, scenario comparison, and gamification features.

## 🎯 What's New in Version 3.0

### Core Enhancements

#### 1. **Multi-Country Support** 🌍
- Emission factors for 5+ countries (India, USA, UK, China, Australia)
- Region-specific calculations for transportation, diet, electricity, and waste
- Easy to expand with additional countries via `emission_factors.json`

#### 2. **Persistent History & Tracking** 📊
- All calculations automatically saved to local storage
- Time series visualization showing emissions trends over time
- Category breakdown charts tracking changes in transport, diet, electricity, and waste
- Statistics dashboard showing averages, highs, lows, and trends
- Export history to CSV for external analysis

#### 3. **Goal Setting & Progress Tracking** 🎯
- Set custom emission reduction targets with deadlines
- Real-time progress bars showing distance to goal
- Goal comparison against current footprint
- Persistent goal storage across sessions

#### 4. **Interactive Action Simulator** 🎮
- Real-time "what-if" scenario testing
- 12+ actionable items across all categories:
  - **Transportation:** Bike/walk days, carpooling, public transport, electric vehicles
  - **Energy:** LED bulbs, solar panels, efficient appliances
  - **Diet:** Reduce meat, go vegetarian, buy local
  - **Waste:** Composting, increased recycling, waste reduction
- Live calculation of potential savings in tonnes and percentage
- Visual comparison: current vs optimized footprint

#### 5. **Scenario Comparison** 🔬
- Pre-configured high-carbon vs low-carbon lifestyle scenarios
- Side-by-side category breakdown comparisons
- Interactive charts showing potential savings
- Educational tool for understanding impact of different choices

#### 6. **Achievement Badges** 🏆
- 8 unique badges to earn:
  - 🎯 **First Step:** Complete your first calculation
  - 🌟 **Low Carbon Hero:** Under 3 tonnes CO₂e
  - 💚 **Climate Champion:** Under 2 tonnes CO₂e
  - 📊 **Tracker:** 10 calculations completed
  - 📉 **Improving:** Downward emissions trend
  - 🚲 **Green Commuter:** Eco-friendly transport
  - 🥗 **Plant Powered:** Vegetarian/Vegan diet
  - ♻️ **Recycling Pro:** 70%+ recycling rate
- Progress tracking to next badges
- Visual badge display with locked/unlocked states

#### 7. **Enhanced Visualizations** 📈
- Time series line charts showing emissions over time
- Stacked area charts for category trends
- Interactive pie charts with hover details
- Bar charts for scenario comparisons
- Goal progress indicators

#### 8. **Expanded Data Inputs** 📝
- Additional transportation modes (diesel cars, auto rickshaw, electric vehicles)
- More diet options (low meat eater)
- Cooking fuel emissions (coming soon)
- Water usage tracking (coming soon)

## 🚀 Quick Start

### Installation

1. **Clone or download the project**

2. **Install dependencies:**
```powershell
pip install streamlit pandas plotly
```

3. **Run the app:**
```powershell
streamlit run app.py
```

4. **Open in browser:**
The app will automatically open at `http://localhost:8502`

## 📁 Project Structure

```
prac/
├── app.py                      # Main enhanced application
├── app_backup.py               # Original version backup
├── storage.py                  # Persistence & data management
├── emission_factors.json       # Multi-country emission data
├── carbon_history.json         # User calculation history (auto-created)
└── README.md                   # This file
```

## 🎨 Features Guide

### Tab 1: Calculate 📝
- Select your country for region-specific factors
- Input daily habits across 4 categories
- Real-time validation and helpful tips
- Instant calculation with detailed breakdown
- Automatic save to history

### Tab 2: History & Trends 📊
- Interactive timeline of all calculations
- Category trend analysis
- Statistical summaries (average, lowest, highest)
- Trend indicators (improving/worsening/neutral)
- Export functionality (CSV)

### Tab 3: Scenario Comparison 🎯
- Compare high-carbon vs low-carbon lifestyles
- See potential savings from major lifestyle changes
- Category-by-category breakdowns
- Educational scenarios

### Tab 4: Achievements 🏆
- View earned badges
- Track progress to next milestones
- Gamification for sustained engagement

### Sidebar Features ⚙️
- Theme color customization (4 colors)
- Personal statistics dashboard
- Goal setting & management
- Quick tips expander
- History management (clear data)

### Action Simulator (in Calculate tab) 🎮
- Select multiple potential actions
- See cumulative impact in real-time
- Visual before/after comparison
- Prioritize highest-impact changes

## 📊 Data & Accuracy

### Emission Factors Sources
- **Transportation:** Based on IPCC and national transport agencies
- **Electricity:** Country-specific grid emission intensities
- **Diet:** Life-cycle assessment studies (varies by country)
- **Waste:** Landfill methane emissions (IPCC guidelines)

### Accuracy Notes
- Estimates are averages; individual impact varies
- Use actual bills/receipts for better accuracy
- Factors updated periodically from authoritative sources
- Regional variations within countries not yet captured

## 🔧 Customization

### Adding New Countries

Edit `emission_factors.json`:

```json
{
  "YourCountry": {
    "Transportation": {
      "Car (Petrol)": 0.192,  // kgCO2e per km
      ...
    },
    "Diet": {
      "High Meat Eater": 3300,  // kgCO2e per year
      ...
    },
    "Electricity": 0.82,  // kgCO2e per kWh
    "Waste": 0.57  // kgCO2e per kg
  }
}
```

### Adding New Badges

Edit `app.py` and add to `BADGES` dictionary:

```python
BADGES = {
    "your_badge_id": {
        "icon": "🎖️",
        "title": "Badge Name",
        "description": "How to earn it"
    }
}
```

Update `check_badges()` function with earning logic.

### Theming

Modify the `color_map` in sidebar section:

```python
color_map = {
    "Your Theme": "#HEXCOLOR",
    ...
}
```

## 📈 Advanced Features

### Goal Tracking
1. Set target in sidebar (e.g., 2.0 tonnes by 2026-01-01)
2. Progress bar appears after each calculation
3. Get celebratory message when goal achieved
4. Compare against 2050 global target (2 tonnes)

### Trend Analysis
- **Improving:** Latest footprint < 95% of historical average
- **Worsening:** Latest footprint > 105% of historical average
- **Neutral:** Within ±5% of average

### Statistics
- Automatically calculates:
  - Total calculations
  - Average footprint
  - Lowest recorded
  - Highest recorded
  - Current trend direction
  - First/last calculation dates

## 🐛 Troubleshooting

### App won't start
```powershell
# Check Python version (requires 3.7+)
python --version

# Reinstall dependencies
pip install --upgrade streamlit pandas plotly
```

### `emission_factors.json` not found
- Ensure file is in same directory as `app.py`
- Check file name spelling (case-sensitive on some systems)

### History not saving
- Check write permissions in app directory
- `carbon_history.json` is auto-created on first save
- Clear history from sidebar if corrupted

### Charts not displaying
```powershell
pip install --upgrade plotly
```

## 🌟 Tips for Best Results

1. **Be Consistent:** Use same measurement units each time
2. **Use Real Data:** Check electricity bills, odometer readings
3. **Monthly Tracking:** Calculate monthly to spot trends
4. **Set Realistic Goals:** Start with 10-20% reduction targets
5. **Try Simulator:** Test actions before committing to changes
6. **Export History:** Keep external backups of your data

## 🔮 Future Enhancements (Planned)

- [ ] PDF report generation
- [ ] Mobile responsive layout improvements
- [ ] OAuth authentication for cloud sync
- [ ] Community anonymized benchmarking
- [ ] Carbon offset marketplace integration
- [ ] Water usage tracking
- [ ] Home heating/cooling calculations
- [ ] Flight emissions calculator
- [ ] Weekly email reports
- [ ] API for automated tracking

## 📄 License & Credits

**Version:** 3.0  
**Last Updated:** November 2025  
**Framework:** Streamlit  
**Charts:** Plotly  

### Data Sources
- IPCC (Intergovernmental Panel on Climate Change)
- National environmental protection agencies
- Life-cycle assessment research papers

### Disclaimer
This calculator provides estimates for educational purposes. For professional carbon accounting, consult certified environmental consultants.

## 🤝 Contributing

To add features or improve accuracy:
1. Fork the repository
2. Make changes to `app.py` or `emission_factors.json`
3. Test thoroughly with `streamlit run app.py`
4. Submit pull request with description

## 📞 Support

For issues or questions:
- Check troubleshooting section above
- Review code comments in `app.py` and `storage.py`
- Ensure all dependencies are up to date

---

**Made with 💚 for a sustainable future**

*Remember: Every tonne of CO₂ reduced makes a difference!*
