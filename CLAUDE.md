# TerraPulse AI

## Project Overview
AI-powered Earth Intelligence Dashboard built with Streamlit for environmental monitoring and data analysis.

## Tech Stack
- Python 3.x
- Streamlit
- pandas
- numpy
- plotly
- opencv-python
- scikit-learn
- torch
- Pillow

## Current Files
- `app.py` — main Streamlit dashboard
- `requirements.txt` — Python dependencies
- `sample_weather.csv` — test data

## Project Structure
terrapulse-ai/
├── app.py
├── requirements.txt
├── CLAUDE.md
└── sample_weather.csv

text


## Current Features
- Interactive sidebar controls (location, days)
- Dynamic metrics dashboard (temperature, humidity)
- CSV file upload and analysis
- Image file upload and preview
- Data visualization with charts
- Numeric column insights (min, max, avg)

## Coding Guidelines for Claude
1. Keep code beginner-friendly and well-commented
2. Use Streamlit best practices
3. Prefer small, incremental changes
4. Explain major changes before implementing
5. Do NOT rewrite entire files unless explicitly asked
6. Focus on production-ready, clean code
7. Keep UI simple and modern
8. Use proper error handling

## Development Workflow
1. Small feature additions
2. Test immediately in browser
3. Commit to GitHub after each working feature
4. Prioritize portfolio-ready code quality

## Current Goals
- [ ] Improve CSV analytics dashboard
- [ ] Add image analysis features
- [ ] Implement download report functionality
- [ ] Add basic ML prediction capabilities
- [ ] Enhance UI/UX design

## Important Notes
- This is a portfolio project
- Code should be GitHub-ready
- Focus on practical, deployable features
- Keep dependencies minimal


---

# 🚀 Claude Code Usage Guide for TerraPulse AI

## Quick Start Prompts

### 1. Adding New Features
```
Add [feature name] to my TerraPulse AI dashboard. 
Requirements:
- Should integrate with existing tabs
- Use the current data structure (sample_data DataFrame)
- Follow the existing UI style
- Add it to the appropriate tab or create a new one
```

### 2. Fixing Bugs
```
I'm getting an error in [file name] at line [X]:
[paste error message]

Please fix this bug and explain what caused it.
```

### 3. Improving Existing Features
```
Improve the [feature name] in my dashboard by:
- [specific improvement 1]
- [specific improvement 2]
- Make it more professional/faster/better looking
```

---

## 📋 Ready-to-Use Prompts for Common Tasks

### Export Functionality
```
Add data export functionality to TerraPulse AI:
1. Add "Download CSV" button for current environmental data
2. Add "Download Chart as PNG" button for visualizations  
3. Add "Generate PDF Report" with summary statistics
4. Place these in a new "Export" section in the sidebar
```

### City Comparison
```
Add a city comparison feature:
1. Create a new "Compare Cities" tab
2. Allow selecting 2-3 cities from dropdown
3. Show side-by-side metrics comparison table
4. Add comparison charts (bar charts, radar charts)
5. Highlight which city has better/worse air quality
```

### Historical Trends
```
Add historical trend analysis to the Dashboard tab:
1. Show 7-day and 30-day trend charts
2. Calculate trend direction (improving/worsening)
3. Add moving averages overlay
4. Show percentage change over time periods
5. Add trend indicators with up/down arrows
```

### Enhanced Visualizations
```
Improve visualizations in the Dashboard tab:
1. Replace basic line charts with interactive Plotly charts
2. Add zoom, pan, and hover tooltips
3. Use better color schemes for different metrics
4. Add chart legends and proper axis labels
5. Make charts responsive to screen size
```

### UI/UX Improvements
```
Improve the overall UI/UX of TerraPulse AI:
1. Add a professional color theme (blues and greens for environmental theme)
2. Improve spacing and padding between elements
3. Add loading spinners for data processing
4. Add smooth transitions and animations
5. Make the layout mobile-responsive
6. Add helpful tooltips and info icons
```

### Real-Time Monitoring
```
Enhance the real-time monitoring features:
1. Make the auto-refresh more visible with a pulsing indicator
2. Add sound notifications for critical alerts (optional toggle)
3. Show a timeline of recent alerts
4. Add alert severity levels (info, warning, critical)
5. Create an alert dashboard showing all active alerts
```

### ML Model Improvements
```
Enhance the ML Models tab:
1. Add model performance comparison table
2. Show training progress with real-time charts
3. Add hyperparameter tuning interface
4. Include cross-validation results
5. Add model export functionality (save trained models)
6. Show prediction confidence scores
```

---

## 🎯 Step-by-Step Feature Requests

### Adding Download Buttons
**Step 1:**
```
Add a "Download Data" section to the sidebar with a CSV download button
```

**Step 2:**
```
Now add a PNG download button for the main chart in the Dashboard tab
```

**Step 3:**
```
Add a PDF report generator that includes:
- Summary statistics
- Key charts
- Alert history
- Location information
```

### Building Comparison Feature
**Step 1:**
```
Create a new tab called "City Comparison"
```

**Step 2:**
```
Add multi-select dropdown to choose 2-3 cities for comparison
```

**Step 3:**
```
Create a comparison table showing all metrics side-by-side
```

**Step 4:**
```
Add bar charts comparing AQI, temperature, and humidity across selected cities
```

---

## 💡 Pro Tips for Using Claude Code

### Be Specific
❌ Bad: "Make it better"
✅ Good: "Add a download CSV button below the data table in the Dashboard tab"

### Provide Context
❌ Bad: "Fix the error"
✅ Good: "Fix the KeyError in line 245 of app.py when selecting Mumbai from dropdown"

### Iterate Gradually
❌ Bad: "Rebuild the entire dashboard with all new features"
✅ Good: "First add the export button, then we'll add the comparison feature"

### Test After Each Change
```
After adding [feature], please verify:
1. No errors in the console
2. Feature works as expected
3. Existing features still work
4. UI looks good
```

### Ask for Explanations
```
Can you explain how the [feature/function] works?
What libraries are being used and why?
```

---

## 🔧 Debugging Prompts

### When Something Breaks
```
The [feature name] stopped working after the last change.
Error message: [paste error]
Please:
1. Identify what caused the issue
2. Fix it
3. Explain what went wrong
```

### Performance Issues
```
The dashboard is loading slowly when [specific action].
Please optimize:
1. Identify the bottleneck
2. Suggest improvements
3. Implement the best solution
```

### UI Issues
```
The [element] doesn't look right on [screen size/browser].
Please fix the layout and make it responsive.
```

---

## 📊 Data-Related Prompts

### Adding New Data Sources
```
Add support for [data source name]:
1. Create a function to fetch data from [API/file]
2. Transform it to match our DataFrame structure
3. Add error handling for failed requests
4. Display the data in [specific tab]
```

### Data Validation
```
Add data validation to ensure:
1. AQI values are between 0-500
2. Temperature is reasonable (-50 to 60°C)
3. Humidity is 0-100%
4. Handle missing or invalid data gracefully
```

---

## 🎨 Styling Prompts

### Custom Theme
```
Create a custom theme for TerraPulse AI:
1. Use environmental colors (greens, blues, earth tones)
2. Apply consistent styling across all tabs
3. Make metric cards more prominent
4. Add subtle shadows and borders
5. Use custom fonts if possible
```

### Responsive Design
```
Make the dashboard mobile-responsive:
1. Stack columns vertically on small screens
2. Adjust chart sizes for mobile
3. Make sidebar collapsible on mobile
4. Test on different screen sizes
```

---

## 🚨 Common Issues & Solutions

### Issue: Import Errors
```
I'm getting "ModuleNotFoundError: No module named '[library]'"
Please:
1. Add the library to requirements.txt
2. Show me the pip install command
3. Verify the import statement is correct
```

### Issue: Streamlit Rerun Loops
```
The page keeps refreshing infinitely.
Please identify and fix the rerun loop.
```

### Issue: Data Not Updating
```
The data doesn't update when I change the location dropdown.
Please fix the data refresh logic.
```

---

## 📝 Documentation Prompts

### README Update
```
Update the README.md with:
1. Project description and features
2. Installation instructions
3. Usage guide with screenshots
4. Technology stack
5. Future improvements
6. License and contact info
```

### Code Comments
```
Add comprehensive comments to [file/function]:
1. Explain what each section does
2. Document function parameters and returns
3. Add usage examples
4. Explain complex logic
```

---

## 🎯 Portfolio Enhancement Prompts

### Make It Impressive
```
Suggest 5 features that would make this project stand out to employers.
Focus on:
- Technical complexity
- Real-world applicability
- Visual appeal
- Innovation
```

### Best Practices
```
Review the code and suggest improvements for:
1. Code organization
2. Error handling
3. Performance optimization
4. Security best practices
5. Documentation
```

---

## ✨ Example Conversation

**You:** "Add a download CSV button to the Dashboard tab"

**Claude:** [Implements the button]

**You:** "Great! Now add a download button for charts as PNG"

**Claude:** [Adds PNG export]

**You:** "Can you make the buttons look better with icons?"

**Claude:** [Improves button styling]

**You:** "Perfect! Now test both buttons and show me how they work"

**Claude:** [Tests and explains]

---

## 🎓 Learning Prompts

### Understanding Code
```
Explain how [feature/function] works in simple terms.
What design patterns are being used?
```

### Best Practices
```
What are the best practices for [specific task] in Streamlit?
Show me examples.
```

### Alternatives
```
What are alternative ways to implement [feature]?
What are the pros and cons of each approach?
```

---

## 🚀 Next Steps

### Immediate (This Week)
- [ ] Add data export functionality
- [ ] Improve real-time alerts
- [ ] Enhance ML visualizations
- [ ] Add city comparison

### Short-term (This Month)
- [ ] Custom UI theme
- [ ] Mobile responsiveness
- [ ] Historical trends
- [ ] Performance optimization

### Long-term (Future)
- [ ] Database integration
- [ ] User authentication
- [ ] API endpoints
- [ ] Deployment automation

---

## 📚 Helpful Resources

- **Streamlit Docs**: https://docs.streamlit.io
- **Plotly Python**: https://plotly.com/python/
- **Folium Maps**: https://python-visualization.github.io/folium/
- **Prophet Forecasting**: https://facebook.github.io/prophet/
- **Scikit-learn**: https://scikit-learn.org/

---

## 💪 Remember

Claude Code is your AI pair programmer! Use it to:
- ✅ Implement features faster
- ✅ Learn best practices
- ✅ Debug issues quickly
- ✅ Improve code quality
- ✅ Build impressive projects

**Be specific, iterate gradually, and test everything!** 🚀
