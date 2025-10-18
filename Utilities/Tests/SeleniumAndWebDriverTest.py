from selenium import webdriver

# Set up Chrome WebDriver
driver = webdriver.Chrome()

# Open a website
driver.get('http://www.google.com')

# Print the title of the page
print(driver.title)

# Close the browser
driver.quit()
