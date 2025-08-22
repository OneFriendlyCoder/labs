import json
from bs4 import BeautifulSoup
import os

file_path = '/home/labDirectory/meta_iframe_labs/index.html'
json_path = '/home/.evaluationScripts/evaluate.json'

marks = {
    'Total': {
        'Your Total': 0,
        'Maximum Marks': 10
    },
    'Meta-Tags': {
        'Charset': 0,
        'Viewport': 0,
        'Description': 0,
        'Keywords': 0,
        'Author': 0,
        'Robots': 0
    },
    'IFrame': {
        'Presence': 0,
        'Attributes': 0
    },  
    'Special-Characters': {
        'Copyright': 0,
        'Registered': 0,
        'Euro': 0,
        'Trademark': 0
    }
}

feedback = {
    'Meta-Tags': {
        'Charset': '',
        'Viewport': '',
        'Description': '',
        'Keywords': '',
        'Author': '',
        'Robots': ''
    },
    'IFrame': {
        'Presence': '',
        'Attributes': ''
    },
    'Special-Characters': {
        'Copyright': '',
        'Registered': '',
        'Euro': '',
        'Trademark': ''
    }
}

def evaluate_html(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Check Meta Tags
    meta_tags = soup.find_all('meta')
    
    # Check charset
    charset = soup.find('meta', attrs={'charset': 'UTF-8'})
    if charset:
        marks['Meta-Tags']['Charset'] = 1
        marks['Total']['Your Total'] += 1
        feedback['Meta-Tags']['Charset'] = 'Charset meta tag is correctly set to UTF-8'
    else:
        feedback['Meta-Tags']['Charset'] = 'Missing or incorrect charset meta tag'

    # Check viewport
    viewport = soup.find('meta', attrs={'name': 'viewport', 'content': 'width=device-width, initial-scale=1.0'})
    if viewport:
        marks['Meta-Tags']['Viewport'] = 1
        marks['Total']['Your Total'] += 1
        feedback['Meta-Tags']['Viewport'] = 'Viewport meta tag is correctly configured'
    else:
        feedback['Meta-Tags']['Viewport'] = 'Missing or incorrect viewport meta tag'

    # Check description
    description = soup.find('meta', attrs={'name': 'description', 'content': 'The Description'})
    if description:
        marks['Meta-Tags']['Description'] = 1
        marks['Total']['Your Total'] += 1
        feedback['Meta-Tags']['Description'] = 'Description meta tag is present and correct'
    else:
        feedback['Meta-Tags']['Description'] = 'Missing or incorrect description meta tag'

    # Check keywords
    keywords = soup.find('meta', attrs={'name': 'keywords', 'content': 'HTML, CSS, Viewport, Metadata'})
    if keywords:
        marks['Meta-Tags']['Keywords'] = 1
        marks['Total']['Your Total'] += 1
        feedback['Meta-Tags']['Keywords'] = 'Keywords meta tag is present and correct'
    else:
        feedback['Meta-Tags']['Keywords'] = 'Missing or incorrect keywords meta tag'

    # Check author
    author = soup.find('meta', attrs={'name': 'author', 'content': 'Hacker'})
    if author:
        marks['Meta-Tags']['Author'] = 1
        marks['Total']['Your Total'] += 1
        feedback['Meta-Tags']['Author'] = 'Author meta tag is present and correct'
    else:
        feedback['Meta-Tags']['Author'] = 'Missing or incorrect author meta tag'

    # Check robots
    robots = soup.find('meta', attrs={'name': 'robots', 'content': 'index, follow'})
    if robots:
        marks['Meta-Tags']['Robots'] = 1
        marks['Total']['Your Total'] += 1
        feedback['Meta-Tags']['Robots'] = 'Robots meta tag is present and correct'
    else:
        feedback['Meta-Tags']['Robots'] = 'Missing or incorrect robots meta tag'

    # Check IFrame
    iframe = soup.find('iframe')
    if iframe:
        marks['IFrame']['Presence'] = 1
        marks['Total']['Your Total'] += 1
        feedback['IFrame']['Presence'] = 'IFrame element is present'
        
        # Check iframe attributes
        expected_attrs = {
            'src': 'https://cse.iitb.ac.in',
            'width': '600',
            'height': '315',
            'title': 'IITB Website'
        }
        
        if all(iframe.get(attr) == value for attr, value in expected_attrs.items()):
            marks['IFrame']['Attributes'] = 1
            marks['Total']['Your Total'] += 1
            feedback['IFrame']['Attributes'] = 'All iframe attributes are correct'
        else:
            feedback['IFrame']['Attributes'] = 'One or more iframe attributes are incorrect'
    else:
        feedback['IFrame']['Presence'] = 'IFrame element is missing'
        feedback['IFrame']['Attributes'] = 'Cannot check attributes - IFrame is missing'

    # Check Special Characters
    paragraphs = soup.find_all('p')
    special_chars = {
        'copyright': False,
        'registered': False,
        'euro': False,
        'trademark': False
    }
    
    # for p in paragraphs:
    #     text = p.text.lower()
    #     if '&copy' in text:
    #         special_chars['copyright'] = True
    #     if '&reg' in text:
    #         special_chars['registered'] = True
    #     if '&euro' in text:
    #         special_chars['euro'] = True
    #     if '&trade' in text:
    #         special_chars['trademark'] = True

    for p in paragraphs:
        text = p.text  # already un-escaped
        if '©' in text:
            special_chars['copyright'] = True
        if '®' in text:
            special_chars['registered'] = True
        if '€' in text:
            special_chars['euro'] = True
        if '™' in text:
            special_chars['trademark'] = True

    if special_chars['copyright']:
        marks['Special-Characters']['Copyright'] = 1
        marks['Total']['Your Total'] += 1
        feedback['Special-Characters']['Copyright'] = 'Copyright symbol reference is present'
    else:
        feedback['Special-Characters']['Copyright'] = 'Copyright symbol reference is missing'

    if special_chars['registered']:
        marks['Special-Characters']['Registered'] = 1
        marks['Total']['Your Total'] += 1
        feedback['Special-Characters']['Registered'] = 'Registered trademark symbol reference is present'
    else:
        feedback['Special-Characters']['Registered'] = 'Registered trademark symbol reference is missing'

    if special_chars['euro']:
        marks['Special-Characters']['Euro'] = 1
        marks['Total']['Your Total'] += 1
        feedback['Special-Characters']['Euro'] = 'Euro symbol reference is present'
    else:
        feedback['Special-Characters']['Euro'] = 'Euro symbol reference is missing'

    if special_chars['trademark']:
        marks['Special-Characters']['Trademark'] = 1
        marks['Total']['Your Total'] += 1
        feedback['Special-Characters']['Trademark'] = 'Trademark symbol reference is present'
    else:
        feedback['Special-Characters']['Trademark'] = 'Trademark symbol reference is missing'

    # Prepare output
    overall = {'data': []}
    for category, subcategories in feedback.items():
        for subcat, message in subcategories.items():
            score = marks[category][subcat]
            status = "success" if score == 1 else "fail"
            overall['data'].append({
                'testid': f'{category}/{subcat}',
                'status': status,
                'score': marks[category][subcat],
                'maximum marks': 1,
                'message': message
            })
    
    return overall

def main():
    try:
        # Read the HTML file
        with open(file_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # Evaluate the HTML
        results = evaluate_html(html_content)

        if os.path.exists(json_path):
            with open(json_path, 'r', encoding='utf-8') as f:
                existing_data = json.load(f)
            if isinstance(existing_data, dict) and 'data' in existing_data:
                existing_data['data'].extend(results['data'])
                results = existing_data

        # Write results to JSON file
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=4)
            
    except Exception as e:
        print(f"Error running evaluation: {str(e)}")

if __name__ == "__main__":
    main()
