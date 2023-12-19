from playwright.sync_api import sync_playwright
import os

email = os.environ.get('KDP_EMAIL')
password = os.environ.get('KDP_PASSWORD')

def login_and_save_state(playwright):
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()

    # Open new page
    page = context.new_page()

    # Navigate to the login page
    page.goto('https://kdp.amazon.com/fr_FR/bookshelf')

    # Fill the email and password fields
    page.fill('input[name="email"]', email)  # Replace with your email
    page.fill('input[name="password"]', password)       # Replace with your password

    # Check the "Rester connecté" checkbox
    page.check('input[name="rememberMe"]')

    # Submit the form
    page.click('input[id="signInSubmit"]')

    # two_factor_code = input("Enter the 2FA code: ")
    # page.fill('input[name="two_factor_input"]', two_factor_code)  # Adjust the input name as necessary

    # Wait for navigation to the KDP dashboard or a known element on the page after login
    page.wait_for_selector("#create-new-experience-button")  
    
    # Click on the 'Create' button
    try:
        page.click("id=create-new-experience-button")
        print("Button clicked successfully")
    except Exception as e:
        print(f"Error clicking the button: {e}")

    page.wait_for_selector("#selector")

    # Save the state to a file
    context.storage_state(path='state.json')

    # Close browser
    browser.close()


def run_with_saved_state(playwright):
    browser = playwright.chromium.launch(headless=False)
    # Load the saved state
    context = browser.new_context(storage_state='state.json')

    # Open new page
    page = context.new_page()

    # Navigate to the page
    page.goto('https://kdp.amazon.com/fr_FR/bookshelf')

    # Perform actions on the page
    page.wait_for_selector("#create-new-experience-button")  
    
    # Click on the 'Create' button
    try:
        page.click("id=create-new-experience-button")
        print("Button clicked successfully")
    except Exception as e:
        print(f"Error clicking the button: {e}")

    page.wait_for_selector("#selector")
    # Close browser
    browser.close()

"""
    data fields:

data-language-native
data-title (max 200)
data-subtitle
data-publisher-label
data-edition-number
data-primary-author-last-name
data-primary-author-first-name
non-public-domain
public-domain
data-is-adult-content name data[is_adult_content]-radio
name data[selected_browse_nodes][0][id]
data-keywords-0
data-keywords-1
data-keywords-2
?filterByFormula={encoded_formula}
"""