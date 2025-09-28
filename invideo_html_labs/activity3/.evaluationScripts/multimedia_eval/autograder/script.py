import json
from bs4 import BeautifulSoup
import os

file_path = '/home/labDirectory/multimedia_activity/index.html'
json_path = '/home/.evaluationScripts/evaluate.json'

marks = {
    'Total': {
        'Your Total': 0,
        'Maximum Marks': 10
    },
    'Audio': {
        'Element': 0,
        'Controls': 0,
        'Loop': 0,
        'Source': 0
    },
    'Video': {
        'Element': 0,
        'Controls': 0,
        'Autoplay': 0,
        'Muted': 0,
        'Width': 0
    }
}

feedback = {
    'Audio': {
        'Element': '',
        'Controls': '',
        'Loop': '',
        'Source': ''
    },
    'Video': {
        'Element': '',
        'Controls': '',
        'Autoplay': '',
        'Muted': '',
        'Width': ''
    }
}

def evaluate_html(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Check Audio Element
    audio = soup.find('audio')
    if audio:
        marks['Audio']['Element'] = 1
        marks['Total']['Your Total'] += 1
        feedback['Audio']['Element'] = 'Audio element is present'
        
        # Check audio attributes
        if audio.has_attr('controls'):
            marks['Audio']['Controls'] = 1
            marks['Total']['Your Total'] += 1
            feedback['Audio']['Controls'] = 'Controls attribute is present'
        else:
            feedback['Audio']['Controls'] = 'Missing controls attribute'
            
        if audio.has_attr('loop'):
            marks['Audio']['Loop'] = 1
            marks['Total']['Your Total'] += 1
            feedback['Audio']['Loop'] = 'Loop attribute is present'
        else:
            feedback['Audio']['Loop'] = 'Missing loop attribute'

        # Check audio source
        audio_source = audio.find('source')
        if audio_source and audio_source.has_attr('src') and 'audio.mp3' in audio_source['src']:
            marks['Audio']['Source'] = 1
            marks['Total']['Your Total'] += 1
            feedback['Audio']['Source'] = 'Audio source is correctly configured'
        else:
            feedback['Audio']['Source'] = 'Missing or incorrect audio source'
    else:
        feedback['Audio']['Element'] = 'Audio element is missing'
        feedback['Audio']['Controls'] = 'Cannot check - Audio element is missing'
        feedback['Audio']['Loop'] = 'Cannot check - Audio element is missing'
        feedback['Audio']['Source'] = 'Cannot check - Audio element is missing'

    # Check Video Element
    video = soup.find('video')
    if video:
        marks['Video']['Element'] = 1
        marks['Total']['Your Total'] += 1
        feedback['Video']['Element'] = 'Video element is present'
        
        # Check video attributes
        if video.has_attr('controls'):
            marks['Video']['Controls'] = 1
            marks['Total']['Your Total'] += 1
            feedback['Video']['Controls'] = 'Controls attribute is present'
        else:
            feedback['Video']['Controls'] = 'Missing controls attribute'
            
        if video.has_attr('autoplay'):
            marks['Video']['Autoplay'] = 1
            marks['Total']['Your Total'] += 1
            feedback['Video']['Autoplay'] = 'Autoplay attribute is present'
        else:
            feedback['Video']['Autoplay'] = 'Missing autoplay attribute'
            
        if video.has_attr('muted'):
            marks['Video']['Muted'] = 1
            marks['Total']['Your Total'] += 1
            feedback['Video']['Muted'] = 'Muted attribute is present'
        else:
            feedback['Video']['Muted'] = 'Missing muted attribute'
            
        if video.has_attr('width') and video['width'] == '640':
            marks['Video']['Width'] = 1
            marks['Total']['Your Total'] += 1
            feedback['Video']['Width'] = 'Width is correctly set to 640'
        else:
            feedback['Video']['Width'] = 'Missing or incorrect width attribute'
    else:
        feedback['Video']['Element'] = 'Video element is missing'
        feedback['Video']['Controls'] = 'Cannot check - Video element is missing'
        feedback['Video']['Autoplay'] = 'Cannot check - Video element is missing'
        feedback['Video']['Muted'] = 'Cannot check - Video element is missing'
        feedback['Video']['Width'] = 'Cannot check - Video element is missing'

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
        
        # Append results if JSON exists
        if os.path.exists(json_path):
            with open(json_path, 'r', encoding='utf-8') as f:
                existing_data = json.load(f)
            if isinstance(existing_data, dict) and 'data' in existing_data:
                existing_data['data'].extend(results['data'])
                results = existing_data

        # Write (or overwrite) results to JSON file
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=4)
            
    except Exception as e:
        print(f"Error running evaluation: {str(e)}")

if __name__ == "__main__":
    main()
