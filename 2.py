from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import time

# Function to search for a blog
def search_cfi_blog(search_query, tag_filter, club_filter):
    # Set up the Chrome webdriver
    driver = webdriver.Chrome()

    # Open the CFI website
    driver.get("https://cfi.iitm.ac.in/blog")  # Replace with the actual CFI website URL

    # Find the search input element and enter the search query
    search_input = driver.find_element(By.ID, "search")  # Replace with the actual search input element
    search_input.send_keys(search_query)
    search_input.send_keys(Keys.RETURN)

    # Wait for the search results to load (you may need to adjust the sleep time)
    time.sleep(5)

    # Apply tag and club filters (if provided)
    if tag_filter:
        # Find and click the tag filter element
        tag_filter_element = driver.find_element(By.XPATH, "//label[text()='Tags']")
        tag_filter_element.click()
        # Find and select the tag(s) based on user input
        tag_input = driver.find_element(By.ID, "tag-filter")  # Replace with the actual tag input element
        tag_input.send_keys(tag_filter)
        tag_input.send_keys(Keys.RETURN)

    if club_filter:
        # Find and click the club filter element
        club_filter_element = driver.find_element(By.XPATH, "//label[text()='Clubs']")
        club_filter_element.click()
        # Find and select the club(s) based on user input
        club_input = driver.find_element(By.ID, "club-filter")  # Replace with the actual club input element
        club_input.send_keys(club_filter)
        club_input.send_keys(Keys.RETURN)

    # Wait for the filtered results to load (you may need to adjust the sleep time)
    time.sleep(5)

    # Parse the search results page
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Extract and print the best match (you may need to adjust the parsing logic)
    best_match = None
    search_results = soup.find_all("div", class_="MuiCardContent-root css-1ceuuo3")

    for result in search_results:
        if "MuZero" in result.text:  # Modify this condition to match your best match criteria
            best_match = result
            break

    if best_match:
        print("Best Match:")
        print(best_match.text.strip())

        # Click on the best match
        best_match_link = best_match.find("a")
        if best_match_link:
            relative_link = best_match_link.get("href")
            if relative_link:
                # Combine the relative URL with the base URL to form a complete URL
                complete_link = urljoin(driver.current_url, relative_link)
                driver.get(complete_link)

                input("Press Enter to close the browser...")
            else:
                print("No URL found in the best match.")

    else:
        print("No matching blog found.")

    driver.quit()

# Main function
if __name__ == "__main__":
    search_query = input("Enter your blog search query: ")
    tag_filter = input("Enter tag filter (optional): ")
    club_filter = input("Enter club filter (optional): ")

    search_cfi_blog(search_query, tag_filter, club_filter)
