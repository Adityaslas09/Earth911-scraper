# 🌍 Earth911 Recycling Facilities Scraper

A Python web scraper that extracts recycling facility data from Earth911's public Recycling Center Search tool and outputs the results as a CSV file.

## 📋 Overview

This project scrapes recycling facility information for Electronics recycling centers within 100 miles of zip code 10001, extracting the following data fields:

- **Business Name**: Official facility name
- **Last Update Date**: Last update date of information
- **Street Address**: Full physical street address
- **Materials Accepted**: Materials listed as accepted by the facility

## 🚀 Features

- ✅ **Robust Scraping**: Handles dynamic JavaScript content and SPA behavior
- ✅ **Anti-Detection**: Custom user agent and automation hiding
- ✅ **Error Recovery**: Comprehensive error handling and retry mechanisms
- ✅ **Data Validation**: Filters out invalid data and duplicates
- ✅ **CSV Output**: Clean, formatted CSV file generation
- ✅ **Multiple Fallbacks**: Various selector strategies for reliable data extraction

## 📦 Requirements

- Python 3.7+
- Chrome browser installed
- ChromeDriver (automatically managed)

## 🛠️ Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/earth911-scraper.git
   cd earth911-scraper
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## 🎯 Usage

Run the scraper:
```bash
python earth911_scraper_final.py
```

The script will:
1. Navigate to Earth911 search page
2. Find recycling facilities
3. Extract data from each facility
4. Save results to `recycling_facilities.csv`

## 📊 Output Format

The script generates a CSV file with the following structure:

```csv
Business_name,last_update_date,street_address,materials_accepted
Recycling centers for "Electronics" near "10001",N/A,"New York, NY 10001","Dehumidifiers, Humidifiers, Air Conditioners, ..."
```

## 🔧 Technical Details

### Libraries Used
- **Selenium WebDriver**: For handling dynamic JavaScript content
- **Chrome WebDriver**: Reliable browser automation
- **CSV Module**: For data output formatting
- **Regex**: For date pattern matching

### Why Selenium over BeautifulSoup?
- Earth911 uses dynamic content loading with JavaScript
- Facility details are loaded via AJAX when clicking search results
- Selenium can handle user interactions and complex DOM structures
- Better for modern web applications with dynamic content

### Scraping Strategy
1. **Page Navigation**: Direct navigation to search URL with predefined parameters
2. **Facility Discovery**: Multiple CSS selectors with fallback strategies
3. **Data Extraction**: Multiple approaches for each data field
4. **Error Handling**: Comprehensive try-catch blocks and recovery mechanisms
5. **Data Cleaning**: Text normalization and duplicate removal

## 🛡️ Error Handling

- **Stale Element Protection**: Re-finds elements to avoid stale reference errors
- **Click Interception Handling**: Uses JavaScript clicks as fallback
- **Navigation Recovery**: Proper back navigation with waits
- **Timeout Management**: Extended timeouts for slow-loading content

## 📁 Project Structure

```
earth911-scraper/
├── earth911_scraper_final.py    # Main scraper script
├── requirements.txt              # Python dependencies
├── README.md                    # Project documentation
├── .gitignore                   # Git ignore rules
└── recycling_facilities.csv     # Output file (generated)
```

## 🔍 Challenges Solved

### 1. Dynamic Content Loading
**Challenge**: Earth911 loads facility details via JavaScript when clicking on search results
**Solution**: Selenium WebDriver with explicit waits and proper timing

### 2. Inconsistent Element Selectors
**Challenge**: Website may use different class names or structure variations
**Solution**: Multiple fallback selectors and robust error handling

### 3. Anti-Bot Detection
**Challenge**: Modern websites may detect automated browsers
**Solution**: Custom user agent, realistic timing, and proper browser options

### 4. Network Issues
**Challenge**: Slow loading times or connection problems
**Solution**: Extended timeouts and retry mechanisms

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

This scraper is for educational purposes only. Please respect the website's terms of service and robots.txt file. The script includes appropriate delays between requests to be respectful of the website's resources.

## 🐛 Troubleshooting

### Common Issues

1. **ChromeDriver not found**
   - Install Chrome browser
   - The script will automatically download ChromeDriver

2. **No facilities found**
   - Check internet connection
   - Verify the website structure hasn't changed
   - Try running the script again

3. **Stale element errors**
   - The script handles this automatically
   - If persistent, try increasing wait times

## 📞 Support

If you encounter any issues or have questions, please open an issue on GitHub.

---

**Made with ❤️ for environmental sustainability**
