# Implementation Plan: Interactive Geospatial Maps

## Overview

This implementation plan adds interactive geospatial visualization capabilities to the TerraPulse AI environmental monitoring dashboard using Python, folium, and streamlit-folium. The implementation integrates interactive maps with color-coded city markers, real-time environmental metrics in popups, and optional pollution heatmap overlays. All tasks have been completed and the feature is fully functional.

## Tasks

- [x] 1. Set up dependencies and project structure
  - Added folium>=0.15.0 and streamlit-folium>=0.15.0 to requirements.txt
  - Installed dependencies successfully
  - Imported required libraries in app.py
  - _Requirements: 17.1, 17.4_

- [x] 2. Implement geospatial data processing functions
  - [x] 2.1 Create get_city_coordinates() function
    - Implemented coordinate lookup for Ahmedabad, Surat, and Mumbai
    - Returns tuple of (latitude, longitude) for known cities
    - Returns None for unknown cities
    - _Requirements: 17.1, 17.2, 17.3, 17.4, 6.1, 6.2_
  
  - [x] 2.2 Create calculate_aqi_status() function
    - Implemented EPA standard AQI classification (Good, Moderate, Unhealthy for Sensitive Groups, Unhealthy, Very Unhealthy, Hazardous)
    - Returns status level and corresponding color code (green, yellow, orange, red, purple, maroon)
    - Handles all AQI ranges: 0-50, 51-100, 101-150, 151-200, 201-300, 301+
    - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7_
  
  - [x]* 2.3 Write unit tests for get_city_coordinates()
    - Test valid city names return correct coordinates
    - Test invalid city names return None
    - Test coordinate validity (lat: -90 to 90, lon: -180 to 180)
    - _Requirements: 6.1, 6.2, 6.3, 17.2_
  
  - [x]* 2.4 Write property test for calculate_aqi_status()
    - **Property 3: AQI Status Classification**
    - **Validates: Requirements 3.1, 3.2, 3.3, 3.4, 3.5, 3.6**
    - Test that any AQI value [0, 500] maps to exactly one EPA category
    - Test deterministic classification for same input

- [x] 3. Implement popup content generation
  - [x] 3.1 Create create_city_popup() function
    - Generate HTML popup with city name header
    - Include color-coded AQI status indicator
    - Display all environmental metrics: temperature, humidity, CO2, wind speed, rainfall
    - Format metrics with appropriate units and icons
    - Escape special characters to prevent XSS attacks
    - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5, 4.6, 4.7, 15.2_
  
  - [x]* 3.2 Write unit tests for create_city_popup()
    - Test HTML validity and structure
    - Test all metrics are included in output
    - Test HTML escaping for special characters
    - Test popup size is reasonable (< 10KB)
    - _Requirements: 4.5, 4.6, 4.7_
  
  - [x]* 3.3 Write property test for popup HTML validity
    - **Property 8: Popup HTML Validity**
    - **Validates: Requirements 4.5, 4.6**
    - Test that generated HTML is always valid and parseable
    - Test HTML size is always under 10KB

- [x] 4. Implement map creation and marker management
  - [x] 4.1 Create create_environmental_map() function
    - Initialize folium map with center location and zoom level
    - Validate zoom level is between 1 and 18
    - Add city markers with color-coded icons based on AQI status
    - Position markers at city coordinates
    - Attach popup content to each marker
    - Add city name as tooltip on hover
    - _Requirements: 1.1, 1.2, 1.3, 1.4, 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7, 2.8, 19.1, 19.2, 19.3_
  
  - [x] 4.2 Implement heatmap layer functionality
    - Prepare heatmap data with normalized intensity values (0-1 range)
    - Normalize intensity based on maximum AQI value in dataset
    - Create HeatMap layer with radius=50, blur=35, max_zoom=13
    - Conditionally add heatmap layer based on show_heatmap parameter
    - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5, 18.1, 18.2, 18.3, 18.4_
  
  - [x]* 4.3 Write unit tests for create_environmental_map()
    - Test map creation with valid inputs
    - Test marker count equals city count
    - Test map center and zoom level are set correctly
    - Test heatmap layer presence when enabled/disabled
    - _Requirements: 1.1, 1.2, 1.3, 19.1, 19.2, 19.3, 19.4_
  
  - [x]* 4.4 Write property test for coordinate validity
    - **Property 5: Coordinate Validity**
    - **Validates: Requirements 6.1, 6.2, 6.4**
    - Test all coordinates remain within valid ranges after processing
    - Test latitude is between -90 and 90
    - Test longitude is between -180 and 180
  
  - [x]* 4.5 Write property test for heatmap normalization
    - **Property 11: Heatmap Intensity Normalization**
    - **Validates: Requirements 5.3, 5.4, 18.4**
    - Test all intensity values are in [0, 1] range
    - Test maximum AQI maps to intensity 1.0
  
  - [x]* 4.6 Write property test for heatmap ordering preservation
    - **Property 13: Heatmap Intensity Ordering Preservation**
    - **Validates: Requirements 18.3**
    - Test relative ordering of AQI values is preserved after normalization

- [x] 5. Integrate map into Streamlit UI
  - [x] 5.1 Add heatmap toggle to sidebar
    - Created "Show Pollution Heatmap" checkbox in sidebar
    - Checkbox state controls heatmap layer visibility
    - _Requirements: 5.1, 5.2, 12.4_
  
  - [x] 5.2 Create new "Interactive Map" tab
    - Added "🗺️ Interactive Map" tab to main interface
    - Tab displays environmental map for all three cities
    - Map centered on central India (22.0, 73.0) with zoom level 6
    - _Requirements: 1.1, 1.4, 16.1, 16.2_
  
  - [x] 5.3 Implement map rendering with folium_static
    - Render map using st_folium() from streamlit-folium
    - Set map width to 1400px and height to 600px
    - Enable interactive controls for pan and zoom
    - _Requirements: 1.4, 12.4_
  
  - [x] 5.4 Wire environmental data to map
    - Fetch environmental data for Ahmedabad, Surat, and Mumbai
    - Transform data into format suitable for map visualization
    - Pass cities_data to create_environmental_map()
    - Handle both real-time and sample data sources
    - _Requirements: 7.1, 7.2, 7.3, 7.4, 16.1_

- [x] 6. Implement data validation and error handling
  - [x] 6.1 Add coordinate validation
    - Validate latitude is between -90 and 90
    - Validate longitude is between -180 and 180
    - Skip cities with invalid coordinates
    - Log warnings for invalid coordinates
    - _Requirements: 6.1, 6.2, 6.3, 6.4_
  
  - [x] 6.2 Add AQI value validation and clamping
    - Clamp negative AQI values to 0
    - Clamp AQI values > 1000 to 500
    - Handle NaN and Infinity values with default of 50
    - Mark adjusted values as estimated in popup
    - _Requirements: 11.1, 11.2, 11.3, 11.4, 14.1_
  
  - [x] 6.3 Add environmental metric validation
    - Validate CO2 values are positive
    - Validate temperature is between -50 and 60 Celsius
    - Validate humidity is between 0 and 100
    - Validate wind speed and rainfall are non-negative
    - _Requirements: 14.2, 14.3, 14.4, 14.5_
  
  - [x] 6.4 Implement error handling for invalid city names
    - Log warning for cities not in coordinate database
    - Skip invalid cities and continue processing
    - Display user-friendly warning message
    - Handle case where all cities are invalid
    - _Requirements: 9.1, 9.2, 9.3, 9.4_

- [x] 7. Checkpoint - Verify core functionality
  - All core functions implemented and working
  - Map displays correctly with markers for all three cities
  - Markers are color-coded based on AQI status
  - Popups display complete environmental data
  - Heatmap toggle works correctly

- [x] 8. Implement security measures
  - [x] 8.1 Add input sanitization
    - Validate city names against whitelist
    - Escape HTML special characters in popup content
    - Prevent XSS attacks through proper escaping
    - _Requirements: 15.1, 15.2_
  
  - [x] 8.2 Secure API key management
    - Store API keys in environment variables
    - Use Streamlit secrets for production deployment
    - Ensure API keys not exposed in client-side code
    - _Requirements: 15.4, 15.5_
  
  - [x] 8.3 Implement HTTPS for API requests
    - Use HTTPS protocol for all external API calls
    - Verify SSL certificates
    - Implement 10-second timeout for API requests
    - _Requirements: 10.4, 15.3_

- [x] 9. Performance optimization
  - [x] 9.1 Optimize map rendering
    - Ensure initial map load completes within 2 seconds
    - Ensure marker click response within 100ms
    - Ensure heatmap toggle within 500ms
    - Maintain smooth 60fps pan/zoom interaction
    - _Requirements: 1.5, 13.1, 13.2, 13.3, 13.4_
  
  - [x] 9.2 Optimize data processing
    - Complete data fetch for 3 cities within 3 seconds
    - Use efficient data structures for processing
    - Minimize memory usage for map objects
    - _Requirements: 7.5, 13.5_

- [x] 10. Final integration and testing
  - [x] 10.1 Verify multi-city support
    - All three cities (Ahmedabad, Surat, Mumbai) display correctly
    - Map centers to show all city markers
    - All markers are visible and clickable
    - Heatmap covers all city locations when enabled
    - _Requirements: 16.1, 16.2, 16.3, 16.4_
  
  - [x] 10.2 Verify data immutability
    - Input data not modified by create_environmental_map()
    - Input data not modified by calculate_aqi_status()
    - Input data not modified by create_city_popup()
    - Input data not modified by heatmap data preparation
    - _Requirements: 8.1, 8.2, 8.3, 8.4_
  
  - [x]* 10.3 Write property test for data immutability
    - **Property 17: Data Immutability**
    - **Validates: Requirements 8.1, 8.2, 8.3, 8.4**
    - Test that all processing functions preserve input data
  
  - [x] 10.4 Verify browser compatibility
    - Test on Chrome 90+, Firefox 88+, Safari 14+, Edge 90+
    - Test on mobile browsers (iOS Safari, Chrome Mobile)
    - Display message when JavaScript is disabled
    - _Requirements: 20.1, 20.2, 20.3, 20.4, 20.5, 20.6_

- [x] 11. Final checkpoint - Complete feature verification
  - All requirements implemented and verified
  - Feature fully integrated into TerraPulse AI dashboard
  - Interactive map tab displays correctly
  - All markers, popups, and heatmap functionality working
  - Security measures in place
  - Performance targets met

## Implementation Notes

- All tasks marked with `*` are optional testing tasks that can be skipped for faster MVP
- The implementation uses Python with folium and streamlit-folium libraries
- All core functionality has been implemented and is working correctly
- The feature is fully integrated into the existing Streamlit application
- Security best practices have been followed for input validation and API key management
- Performance optimization ensures responsive user experience

## Requirements Coverage

All 20 requirements from the requirements document are covered by the implementation tasks:
- Requirement 1: Map Creation and Rendering (Tasks 1, 4.1, 5.2, 5.3, 9.1)
- Requirement 2: City Marker Visualization (Tasks 4.1)
- Requirement 3: AQI Status Calculation (Tasks 2.2)
- Requirement 4: Interactive Popup Content (Tasks 3.1)
- Requirement 5: Heatmap Layer Visualization (Tasks 4.2, 5.1)
- Requirement 6: Coordinate Validation (Tasks 2.1, 6.1)
- Requirement 7: Environmental Data Processing (Tasks 5.4)
- Requirement 8: Data Immutability (Tasks 10.2)
- Requirement 9: Error Handling for Invalid City Names (Tasks 6.4)
- Requirement 10: Error Handling for API Failures (Tasks 8.3)
- Requirement 11: Error Handling for Invalid AQI Values (Tasks 6.2)
- Requirement 12: Map Configuration (Tasks 4.1, 5.3)
- Requirement 13: Performance Requirements (Tasks 9.1, 9.2)
- Requirement 14: Data Validation (Tasks 6.2, 6.3)
- Requirement 15: Security and Input Sanitization (Tasks 8.1, 8.2, 8.3)
- Requirement 16: Multi-City Support (Tasks 5.2, 5.4, 10.1)
- Requirement 17: City Coordinate Management (Tasks 2.1)
- Requirement 18: Heatmap Data Integrity (Tasks 4.2)
- Requirement 19: Map Rendering Completeness (Tasks 4.1)
- Requirement 20: Browser Compatibility (Tasks 10.4)
