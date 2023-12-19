from playwright.sync_api import sync_playwright
import os
import requests
import urllib.parse

airtable_token = os.environ.get('AIRTABLE_TOKEN')

class Book:
    def __init__(self, id, title, subtitle, author_firstname, author_lastname, author_email,
                 publishing_rights, main_region, publication_date, book_description,
                 sexual_content, categories, minimum_age, maximum_age, keywords, submitted_at):
        self.id = id
        self.title = title
        self.subtitle = subtitle
        self.author_firstname = author_firstname
        self.author_lastname = author_lastname
        self.author_email = author_email
        self.publishing_rights = publishing_rights
        self.main_region = main_region
        self.publication_date = publication_date
        self.book_description = book_description
        self.sexual_content = sexual_content
        self.categories = categories
        self.minimum_age = minimum_age
        self.maximum_age = maximum_age
        self.keywords = keywords
        self.submitted_at = submitted_at

    def __str__(self):
        return f"Book(title={self.title}, author={self.author_firstname} {self.author_lastname})"


def fetch_record_from_airtable(submission_id):
    base_id = "app9w6oPEOlQzUN0I"  # Replace with your Airtable Base ID
    table_name = "MANUSCRIPT_SUBMISSIONS"  # Replace with your Table Name

    formula = f"{{Submission ID}} = '{submission_id}'"
    encoded_formula = urllib.parse.quote(formula)

    url = f"https://api.airtable.com/v0/{base_id}/{table_name}?filterByFormula={encoded_formula}"

    headers = {
        "Authorization": f"Bearer {airtable_token}"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        if len(data["records"])>1:
            print("More than one records found, taking the most recent")
            return data["records"][0]
        else:
            print("One record found")
            return data["records"]
    else:
        return None
    

wantedrecord = input()

record = fetch_record_from_airtable(wantedrecord)
if record:
    fields = record['fields']  # Assuming the first record is what you need
    book = Book(
        id=record['id'],
        title=fields.get('title'),
        subtitle=fields.get('subtitle'),
        author_firstname=fields.get('author_firstname'),
        author_lastname=fields.get('author_lastname'),
        author_email=fields.get('author_email'),
        publishing_rights=fields.get('publishing_rights'),
        main_region=fields.get('main_region'),
        publication_date=fields.get('publication_date'),
        book_description=fields.get('book_description'),
        sexual_content=fields.get('sexual_content'),
        categories=fields.get('categories', []),
        minimum_age=fields.get('minimum_age'),
        maximum_age=fields.get('maximum_age'),
        keywords=fields.get('keywords'),
        submitted_at=fields.get('Submitted at')
    )

    print(book)  # To check the created book object
else:
    print("Record not found.")



###with sync_playwright() as playwright:
   ### try:
      ###  run_with_saved_state(playwright)
    ### except Exception as e:
        ### print("Error with run state login: {e}")
        ### login_and_save_state(playwright)    


