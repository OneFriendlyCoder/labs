import json
from bs4 import BeautifulSoup
import os

file_path = '/home/labDirectory/div_labs/index.html'
json_path = '/home/.evaluationScripts/evaluate.json'

marks = {
    'Total': {
        'Your Total': 0,
        'Maximum Marks': 12
    },
    'Container': {
        'Presence': 0,
        'Styling': 0
    },
    'Div-Usage': {
        'Sections': 0,
        'Nesting': 0
    },
    'Span-Usage': {
        'Highlight': 0,
        'Important': 0
    },
    'CSS-Classes': {
        'Definition': 0,
        'Application': 0
    },
    'Structure': {
        'Headings': 0,
        'Lists': 0
    },
    'ID-Usage': {
        'Presence': 0,
        'Styling': 0
    }
}

feedback = {
    'Container': {
        'Presence': '',
        'Styling': ''
    },
    'Div-Usage': {
        'Sections': '',
        'Nesting': ''
    },
    'Span-Usage': {
        'Highlight': '',
        'Important': ''
    },
    'CSS-Classes': {
        'Definition': '',
        'Application': ''
    },
    'Structure': {
        'Headings': '',
        'Lists': ''
    },
    'ID-Usage': {
        'Presence': '',
        'Styling': ''
    }
}

def evaluate_html(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Check Container
    container = soup.find('div', class_='container')
    if container:
        marks['Container']['Presence'] = 1
        marks['Total']['Your Total'] += 1
        feedback['Container']['Presence'] = 'Container div is present'
        
        # Check container styling
        style_tag = soup.find('style')
        if style_tag and '.container' in style_tag.text:
            container_style = style_tag.text
            required_styles = ['width', 'margin', 'padding', 'border']
            if all(style in container_style for style in required_styles):
                marks['Container']['Styling'] = 1
                marks['Total']['Your Total'] += 1
                feedback['Container']['Styling'] = 'Container has required styling'
            else:
                feedback['Container']['Styling'] = 'Container missing some required styles'
    else:
        feedback['Container']['Presence'] = 'Container div is missing'
        feedback['Container']['Styling'] = 'Cannot check styling - Container is missing'

    # Check Div Usage
    content_divs = soup.find_all('div')
    if len(content_divs) >= 3:  # Container + 2 content sections
        marks['Div-Usage']['Sections'] = 1
        marks['Total']['Your Total'] += 1
        feedback['Div-Usage']['Sections'] = 'Required content sections are present'
    else:
        feedback['Div-Usage']['Sections'] = 'Missing required content sections'

    # Check proper nesting
    if container and any(div.parent == container for div in content_divs if div != container):
        marks['Div-Usage']['Nesting'] = 1
        marks['Total']['Your Total'] += 1
        feedback['Div-Usage']['Nesting'] = 'Proper div nesting structure'
    else:
        feedback['Div-Usage']['Nesting'] = 'Incorrect div nesting'

    # Check Span Usage
    highlight_spans = soup.find_all('span', class_='highlight')
    important_spans = soup.find_all('span', class_='important')
    
    if len(highlight_spans) >= 2:
        marks['Span-Usage']['Highlight'] = 1
        marks['Total']['Your Total'] += 1
        feedback['Span-Usage']['Highlight'] = 'Highlight spans are properly used'
    else:
        feedback['Span-Usage']['Highlight'] = 'Missing required highlight spans'

    if len(important_spans) >= 1:
        marks['Span-Usage']['Important'] = 1
        marks['Total']['Your Total'] += 1
        feedback['Span-Usage']['Important'] = 'Important spans are properly used'
    else:
        feedback['Span-Usage']['Important'] = 'Missing required important spans'

    # Check CSS Classes
    style_tag = soup.find('style')
    if style_tag:
        css_text = style_tag.text
        required_classes = ['.highlight', '.important']
        if all(cls in css_text for cls in required_classes):
            marks['CSS-Classes']['Definition'] = 1
            marks['Total']['Your Total'] += 1
            feedback['CSS-Classes']['Definition'] = 'Required CSS classes are defined'
        else:
            feedback['CSS-Classes']['Definition'] = 'Missing required CSS class definitions'
        
        # Check if classes are properly applied
        if highlight_spans and important_spans:
            marks['CSS-Classes']['Application'] = 1
            marks['Total']['Your Total'] += 1
            feedback['CSS-Classes']['Application'] = 'CSS classes are properly applied'
        else:
            feedback['CSS-Classes']['Application'] = 'CSS classes not properly applied'
    else:
        feedback['CSS-Classes']['Definition'] = 'No style tag found'
        feedback['CSS-Classes']['Application'] = 'Cannot check class application - no styles defined'

    # Check ID Usage
    # Presence of <h1 id="main-title">
    id_element = soup.find('h1', id='main-title')
    if id_element:
        marks['ID-Usage']['Presence'] = 1
        marks['Total']['Your Total'] += 1
        feedback['ID-Usage']['Presence'] = 'H1 element has correct id'
    else:
        feedback['ID-Usage']['Presence'] = 'Missing h1 with id="main-title"'

    # Check id styling in CSS
    if style_tag and '#main-title' in style_tag.text:
        marks['ID-Usage']['Styling'] = 1
        marks['Total']['Your Total'] += 1
        feedback['ID-Usage']['Styling'] = 'ID selector styling is defined'
    else:
        feedback['ID-Usage']['Styling'] = 'Missing styling for #main-title in CSS'

    # Check Structure
    headings = soup.find_all(['h1', 'h2'])
    if len(headings) >= 2 and soup.find('h1') and soup.find('h2'):
        marks['Structure']['Headings'] = 1
        marks['Total']['Your Total'] += 1
        feedback['Structure']['Headings'] = 'Proper heading structure'
    else:
        feedback['Structure']['Headings'] = 'Missing required headings'

    lists = soup.find('ul')
    if lists and len(lists.find_all('li')) >= 3:
        marks['Structure']['Lists'] = 1
        marks['Total']['Your Total'] += 1
        feedback['Structure']['Lists'] = 'List structure is correct'
    else:
        feedback['Structure']['Lists'] = 'Missing required list structure'

    # Prepare output
    overall = {'data': []}
    for category, subcategories in feedback.items():
        for subcat, message in subcategories.items():
            score = marks[category][subcat]
            status = "success" if score == 1 else "fail"
            overall['data'].append({
                'testid': f'{category}/{subcat}',
                'status': status,
                'score': score,
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
        
        # Write results to JSON file
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=4)
            
    except Exception as e:
        print(f"Error running evaluation: {str(e)}")

if __name__ == "__main__":
    main()
