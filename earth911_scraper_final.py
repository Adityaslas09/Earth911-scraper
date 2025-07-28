
"""
Earth911 Recycling Facilities Scraper
====================================

This script scrapes recycling facility data from Earth911's public Recycling Center Search tool
and outputs the results as a CSV file.

Requirements:
- Python 3.7+
- Chrome browser installed
- selenium package

Usage:
    python earth911_scraper_final.py

Output:
    recycling_facilities.csv - CSV file with facility data
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException, StaleElementReferenceException
import csv
import time
import re

def setup_driver():
    """Setup Chrome WebDriver with appropriate options"""
    options = Options()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
    
    driver = webdriver.Chrome(options=options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    return driver

def extract_facility_data(driver, wait):
    """Extract data from a single facility detail page"""
    try:
        print("  Extracting facility data...")
        
        # Wait for the page to load
        time.sleep(3)
        
        # Extract business name - try multiple approaches
        business_name = "N/A"
        name_selectors = [
            'h1:not([class*="help"]):not([class*="search"])',
            'h2:not([class*="help"]):not([class*="search"])', 
            '.business-name',
            '.facility-name',
            '.location-name',
            '[class*="name"]:not([class*="help"])',
            '.title:not([class*="help"])',
            '.facility-title',
            '.location-title'
        ]
        
        for selector in name_selectors:
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                for element in elements:
                    text = element.text.strip()
                    if text and len(text) > 5 and "help" not in text.lower() and "search" not in text.lower():
                        business_name = text
                        print(f"  Found business name: {business_name}")
                        break
                if business_name != "N/A":
                    break
            except NoSuchElementException:
                continue
        
        # Extract last updated date
        last_updated = "N/A"
        try:
            # Look for date patterns in the page
            page_text = driver.page_source
            date_patterns = [
                r'Last Updated[:\s]*(\d{4}-\d{2}-\d{2})',
                r'Updated[:\s]*(\d{4}-\d{2}-\d{2})',
                r'(\d{4}-\d{2}-\d{2})',
                r'(\d{2}/\d{2}/\d{4})'
            ]
            
            for pattern in date_patterns:
                match = re.search(pattern, page_text)
                if match:
                    last_updated = match.group(1)
                    print(f"  Found last updated: {last_updated}")
                    break
        except Exception as e:
            print(f"  Error extracting last updated date: {e}")
        
        # Extract street address
        street_address = "N/A"
        address_selectors = [
            '.address',
            '.street-address',
            '[class*="address"]',
            '.location-address',
            '.facility-address',
            '.contact-address'
        ]
        
        for selector in address_selectors:
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                for element in elements:
                    text = element.text.strip()
                    if text and len(text) > 10:  # Address should be reasonably long
                        street_address = text
                        print(f"  Found address: {street_address}")
                        break
                if street_address != "N/A":
                    break
            except NoSuchElementException:
                continue
        
        # Extract materials accepted
        materials_accepted = "N/A"
        try:
            # Try multiple approaches for materials
            materials_selectors = [
                '.materials-accepted li',
                '.accepted-materials li',
                '[class*="materials"] li',
                '.materials li',
                '.accepted li',
                '.recycled-materials li'
            ]
            
            materials = []
            for selector in materials_selectors:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                if elements:
                    for element in elements:
                        text = element.text.strip()
                        if text and len(text) > 2 and len(text) < 50:  # Reasonable length for material names
                            materials.append(text)
                    if materials:
                        break
            
            # If no materials found, try XPath approach
            if not materials:
                xpath_patterns = [
                    '//*[contains(text(), "Accepts")]/following-sibling::*',
                    '//*[contains(text(), "Materials")]/following-sibling::*',
                    '//*[contains(text(), "Recycles")]/following-sibling::*'
                ]
                
                for xpath in xpath_patterns:
                    elements = driver.find_elements(By.XPATH, xpath)
                    for element in elements:
                        text = element.text.strip()
                        if text and len(text) > 2 and len(text) < 50:
                            materials.append(text)
                    if materials:
                        break
            
            if materials:
                # Clean up materials list
                cleaned_materials = []
                for material in materials:
                    if material not in cleaned_materials:  # Remove duplicates
                        cleaned_materials.append(material)
                materials_accepted = ', '.join(cleaned_materials)
                print(f"  Found materials: {materials_accepted}")
        
        except Exception as e:
            print(f"  Error extracting materials: {e}")
        
        return {
            'Business_name': business_name,
            'last_update_date': last_updated,
            'street_address': street_address,
            'materials_accepted': materials_accepted
        }
        
    except Exception as e:
        print(f"  Error extracting facility data: {e}")
        return None

def find_facilities(driver):
    """Find facilities on the current page"""
    facility_selectors = [
        '[class*="location"]',
        '[class*="facility"]',
        '[class*="tile"]',
        '.search-result',
        '.result-item',
        '.facility-item'
    ]
    
    facilities = []
    for selector in facility_selectors:
        try:
            facilities = driver.find_elements(By.CSS_SELECTOR, selector)
            if facilities:
                print(f"Found {len(facilities)} facilities using selector: {selector}")
                break
        except:
            continue
    
    if not facilities:
        print("No facilities found with standard selectors. Trying alternative approach...")
        facilities = driver.find_elements(By.CSS_SELECTOR, 'a, [onclick], .clickable')
    
    return facilities

def scrape_earth911():
    """Main scraping function"""
    driver = setup_driver()
    wait = WebDriverWait(driver, 20)
    facilities_data = []
    
    try:
        # Navigate to the search page
        url = 'https://search.earth911.com/?what=Electronics&where=10001&list_filter=all&max_distance=100'
        print(f"Navigating to: {url}")
        driver.get(url)
        
        # Wait for page to load
        time.sleep(8)
        
        print("Page loaded, looking for facilities...")
        
        # Get initial facilities
        facilities = find_facilities(driver)
        
        if not facilities:
            print("No facilities found. The page structure might have changed.")
            print("Current page title:", driver.title)
            print("Current URL:", driver.current_url)
            return []
        
        # Limit to first 3 facilities
        facilities = facilities[:3]
        
        for i in range(1, 4):  # Process exactly 3 facilities
            print(f"\nProcessing facility {i}/3")
            
            try:
                # Navigate back to search page if not already there
                if driver.current_url != url:
                    print("  Navigating back to search page...")
                    driver.get(url)
                    time.sleep(5)
                
                # Re-find facilities
                current_facilities = find_facilities(driver)
                
                if not current_facilities or i > len(current_facilities):
                    print(f"Not enough facilities found for facility {i}")
                    break
                
                # Get the current facility
                facility = current_facilities[i-1]
                
                # Scroll to facility element
                driver.execute_script("arguments[0].scrollIntoView(true);", facility)
                time.sleep(2)
                
                # Try to click on facility
                try:
                    facility.click()
                except (ElementClickInterceptedException, StaleElementReferenceException):
                    # Try JavaScript click
                    driver.execute_script("arguments[0].click();", facility)
                
                time.sleep(3)
                
                # Extract data from detail page
                facility_data = extract_facility_data(driver, wait)
                
                if facility_data and facility_data['Business_name'] != "N/A":
                    facilities_data.append(facility_data)
                    print(f"Successfully extracted data for: {facility_data['Business_name']}")
                
            except Exception as e:
                print(f"Error processing facility {i}: {e}")
                continue
    
    except Exception as e:
        print(f"Error during scraping: {e}")
    
    finally:
        driver.quit()
    
    return facilities_data

def save_to_csv(data, filename='recycling_facilities.csv'):
    """Save scraped data to CSV file"""
    if not data:
        print("No data to save.")
        return
    
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Business_name', 'last_update_date', 'street_address', 'materials_accepted']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)
    
    print(f"Data saved to {filename}")

def main():
    """Main function to run the scraper"""
    print("=" * 60)
    print("Earth911 Recycling Facilities Scraper")
    print("=" * 60)
    print("Searching for Electronics recycling centers near 10001...")
    print()
    
    # Scrape the data
    facilities_data = scrape_earth911()
    
    if facilities_data:
        print(f"\n✅ Successfully scraped {len(facilities_data)} facilities:")
        print("-" * 60)
        for i, facility in enumerate(facilities_data, 1):
            print(f"\nFacility {i}:")
            print(f"  Business Name: {facility['Business_name']}")
            print(f"  Last Updated: {facility['last_update_date']}")
            print(f"  Address: {facility['street_address']}")
            print(f"  Materials: {facility['materials_accepted']}")
        
        # Save to CSV
        save_to_csv(facilities_data)
        print("\n" + "=" * 60)
        print("✅ Scraping completed successfully!")
        print("📁 Data saved to: recycling_facilities.csv")
        print("=" * 60)
    else:
        print("\n❌ No facilities data was scraped.")
        print("Please check the website structure or try again later.")

if __name__ == "__main__":
    main() 