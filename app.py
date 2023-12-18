from playwright.sync_api import sync_playwright
import os
import requests
import urllib.parse

email = os.environ.get('KDP_EMAIL')
password = os.environ.get('KDP_PASSWORD')
airtable_token = os.environ.get('AIRTABLE_TOKEN')

def fetch_record_from_airtable(submission_id):
    base_id = "app9w6oPEOlQzUN0I"  # Replace with your Airtable Base ID
    table_name = "MANUSCRIPT_SUBMISSIONS"  # Replace with your Table Name

    formula = f"{{Submission ID}} = '{submission_id}'"
    encoded_formula = urllib.parse.quote(formula)

    url = f"https://api.airtable.com/v0/{base_id}/{table_name}"

    headers = {
        "Authorization": f"Bearer {airtable_token}"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        return None
    

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

wantedrecord = input()

record = fetch_record_from_airtable('your_submission_id')
if record:
    print(record)  # This will contain the data from the columns
else:
    print("Record not found.")



###with sync_playwright() as playwright:
   ### try:
      ###  run_with_saved_state(playwright)
    ### except Exception as e:
        ### print("Error with run state login: {e}")
        ### login_and_save_state(playwright)    


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