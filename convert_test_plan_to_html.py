#!/usr/bin/env python3
"""
Script to convert test_plan.txt to a nicely formatted HTML file
"""

import re
import os
import webbrowser
from pathlib import Path


def parse_test_plan(file_path):
    """Parse the test plan text file into structured data"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract header information - more flexible matching
    header_match = re.search(r'TEST PLAN FOR (.+?)\n.*?URL:\s*(.+)', content, re.DOTALL)
    title = header_match.group(1).strip() if header_match else "Test Plan"
    url = header_match.group(2).strip() if header_match else ""
    
    # Extract description text (between header separator and first TEST CASE)
    desc_match = re.search(r'={10,}\n\n(.+?)\n\n={10,}\nTEST CASE', content, re.DOTALL)
    description = desc_match.group(1).strip() if desc_match else ""
    
    # Extract test cases
    test_cases = []
    test_case_pattern = r'TEST CASE (\d+): (.+?)\n(.*?)(?=TEST CASE \d+:|END OF TEST PLAN|$)'
    matches = re.finditer(test_case_pattern, content, re.DOTALL)
    
    for match in matches:
        case_num = match.group(1)
        case_title = match.group(2).strip()
        case_content = match.group(3).strip()
        
        # Extract sections
        objective_match = re.search(r'OBJECTIVE:\s*(.+?)(?=TEST STEPS:|$)', case_content, re.DOTALL)
        objective = objective_match.group(1).strip() if objective_match else ""
        
        steps_match = re.search(r'TEST STEPS:\s*(.+?)(?=EXPECTED RESULTS:|$)', case_content, re.DOTALL)
        steps_text = steps_match.group(1).strip() if steps_match else ""
        
        expected_match = re.search(r'EXPECTED RESULTS:\s*(.+?)(?=TEST CASE|END OF TEST PLAN|$)', case_content, re.DOTALL)
        expected_raw = expected_match.group(1).strip() if expected_match else ""
        
        # Parse steps into list - handle indented sub-steps
        steps = []
        step_lines = steps_text.split('\n')
        current_step = None
        
        for line in step_lines:
            # Check if it's a numbered step (not indented)
            step_match = re.match(r'^(\d+)\.\s*(.+)$', line)
            if step_match:
                # Save previous step if exists
                if current_step:
                    steps.append(current_step)
                current_step = {
                    'number': step_match.group(1),
                    'text': step_match.group(2).strip(),
                    'substeps': []
                }
            elif line.strip():  # Non-empty line
                # Check if it's a sub-step (starts with - or * after optional whitespace)
                stripped = line.strip()
                if (stripped.startswith('-') or stripped.startswith('*')) and current_step:
                    # Remove leading - or * and any extra spaces
                    substep_text = re.sub(r'^[-*]\s*', '', stripped)
                    current_step['substeps'].append(substep_text)
                elif current_step and not (stripped.startswith('-') or stripped.startswith('*')):
                    # Continuation of current step text (not a sub-step)
                    current_step['text'] += ' ' + stripped
        
        # Add last step
        if current_step:
            steps.append(current_step)
        
        # Parse expected results into list items
        expected_items = []
        if expected_raw:
            expected_lines = expected_raw.split('\n')
            for line in expected_lines:
                line = line.strip()
                if line:
                    # Skip separator lines (lines with only =, -, or _ characters)
                    if re.match(r'^[=_-]+$', line):
                        continue
                    # Remove leading - or * if present
                    cleaned = re.sub(r'^[-*]\s*', '', line)
                    if cleaned and not re.match(r'^[=_-]+$', cleaned):
                        expected_items.append(cleaned)
        
        test_cases.append({
            'number': case_num,
            'title': case_title,
            'objective': objective,
            'steps': steps,
            'expected': expected_items if expected_items else [expected_raw] if expected_raw else []
        })
    
    # Extract notes
    notes_match = re.search(r'Notes:\s*(.+?)$', content, re.DOTALL)
    notes = notes_match.group(1).strip() if notes_match else ""
    
    return {
        'title': title,
        'url': url,
        'description': description,
        'test_cases': test_cases,
        'notes': notes
    }


def format_text_as_html(text):
    """Convert plain text to HTML with proper formatting"""
    if not text:
        return ""
    
    # Convert numbered lists
    text = re.sub(r'^(\d+)\.\s+(.+)$', r'<li>\2</li>', text, flags=re.MULTILINE)
    
    # Convert bullet points
    text = re.sub(r'^[-*]\s+(.+)$', r'<li>\1</li>', text, flags=re.MULTILINE)
    
    # Wrap consecutive list items in <ul>
    lines = text.split('\n')
    html_lines = []
    in_list = False
    
    for line in lines:
        if '<li>' in line:
            if not in_list:
                html_lines.append('<ul>')
                in_list = True
            html_lines.append(line)
        else:
            if in_list:
                html_lines.append('</ul>')
                in_list = False
            if line.strip():
                html_lines.append(f'<p>{line.strip()}</p>')
    
    if in_list:
        html_lines.append('</ul>')
    
    result = '\n'.join(html_lines)
    
    # Convert line breaks to <br> for paragraphs
    result = result.replace('\n', '<br>\n')
    
    return result


def generate_html(data):
    """Generate HTML from parsed test plan data"""
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{data['title']} - Test Plan</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            background-color: #f5f5f5;
            padding: 20px;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background-color: white;
            padding: 40px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        
        h1 {{
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
            margin-bottom: 10px;
        }}
        
        .header-info {{
            background-color: #ecf0f1;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 30px;
        }}
        
        .url {{
            color: #3498db;
            font-weight: bold;
            margin-top: 5px;
        }}
        
        .test-case {{
            margin-bottom: 40px;
            border: 1px solid #ddd;
            border-radius: 5px;
            padding: 25px;
            background-color: #fafafa;
        }}
        
        .test-case-header {{
            background-color: #3498db;
            color: white;
            padding: 15px;
            margin: -25px -25px 20px -25px;
            border-radius: 5px 5px 0 0;
        }}
        
        .test-case-title {{
            font-size: 1.3em;
            font-weight: bold;
        }}
        
        .section {{
            margin-bottom: 20px;
        }}
        
        .section-title {{
            color: #2c3e50;
            font-size: 1.1em;
            font-weight: bold;
            margin-bottom: 10px;
            padding-bottom: 5px;
            border-bottom: 2px solid #3498db;
        }}
        
        .objective {{
            background-color: #e8f5e9;
            padding: 15px;
            border-left: 4px solid #4caf50;
            border-radius: 3px;
            margin-bottom: 15px;
        }}
        
        .steps {{
            background-color: #fff3e0;
            padding: 15px;
            border-left: 4px solid #ff9800;
            border-radius: 3px;
            margin-bottom: 15px;
        }}
        
        .step {{
            margin-bottom: 15px;
        }}
        
        .step-number {{
            font-weight: bold;
            color: #ff9800;
        }}
        
        .step-text {{
            margin-left: 5px;
        }}
        
        .substeps {{
            margin-left: 20px;
            margin-top: 8px;
        }}
        
        .substeps li {{
            margin-bottom: 5px;
            color: #666;
        }}
        
        .expected {{
            background-color: #e3f2fd;
            padding: 15px;
            border-left: 4px solid #2196f3;
            border-radius: 3px;
            margin-bottom: 15px;
        }}
        
        .notes {{
            background-color: #fce4ec;
            padding: 20px;
            border-left: 4px solid #e91e63;
            border-radius: 3px;
            margin-top: 30px;
        }}
        
        ul {{
            margin-left: 20px;
            margin-top: 10px;
        }}
        
        li {{
            margin-bottom: 8px;
        }}
        
        p {{
            margin-bottom: 10px;
        }}
        
        .toc {{
            background-color: #f0f0f0;
            padding: 20px;
            border-radius: 5px;
            margin-bottom: 30px;
        }}
        
        .toc-title {{
            font-weight: bold;
            font-size: 1.2em;
            margin-bottom: 15px;
            color: #2c3e50;
        }}
        
        .toc ul {{
            list-style-type: none;
        }}
        
        .toc li {{
            margin-bottom: 8px;
        }}
        
        .toc a {{
            color: #3498db;
            text-decoration: none;
        }}
        
        .toc a:hover {{
            text-decoration: underline;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>TEST PLAN FOR {data['title'].replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')}</h1>
        <div class="header-info">
"""
    
    # Add description if present
    if data['description']:
        escaped_desc = data['description'].replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        html += f'            <p>{escaped_desc}</p>\n'
    
    html += """        </div>
"""
    
    # Add test cases
    for tc in data['test_cases']:
        escaped_tc_title = tc['title'].replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        html += f"""        <div class="test-case" id="test-case-{tc['number']}">
            <div class="test-case-header">
                <div class="test-case-title">TEST CASE {tc['number']}: {escaped_tc_title}</div>
            </div>
            
            <div class="section">
                <div class="section-title">OBJECTIVE</div>
                <div class="objective">
                    <p>{tc['objective'].replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')}</p>
                </div>
            </div>
            
            <div class="section">
                <div class="section-title">TEST STEPS</div>
                <div class="steps">
"""
        
        for step in tc['steps']:
            # Escape HTML in step text
            escaped_text = step['text'].replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            html += f"""                    <div class="step">
                        <span class="step-number">{step['number']}.</span>
                        <span class="step-text">{escaped_text}</span>
"""
            if step['substeps']:
                html += '                        <ul class="substeps">\n'
                for substep in step['substeps']:
                    # Escape HTML in substeps
                    escaped_substep = substep.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
                    html += f'                            <li>{escaped_substep}</li>\n'
                html += '                        </ul>\n'
            html += '                    </div>\n'
        
        html += """                </div>
            </div>
            
            <div class="section">
                <div class="section-title">EXPECTED RESULTS</div>
                <div class="expected">
"""
        
        if isinstance(tc['expected'], list) and tc['expected']:
            html += '                    <ul>\n'
            for item in tc['expected']:
                # Escape HTML special characters
                escaped_item = item.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
                html += f'                        <li>{escaped_item}</li>\n'
            html += '                    </ul>\n'
        elif tc['expected']:
            # Fallback for string format
            escaped_expected = str(tc['expected']).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            html += f'                    <p>{escaped_expected.replace(chr(10), "<br>")}</p>\n'
        
        html += """                </div>
            </div>
        </div>
"""
    
    html += """    </div>
</body>
</html>"""
    
    return html


def main():
    """Main function to convert test plan and open HTML"""
    # Get the script directory
    script_dir = Path(__file__).parent
    test_plan_path = script_dir / 'test_plan.txt'
    output_path = script_dir / 'test_plan.html'
    
    if not test_plan_path.exists():
        print(f"Error: {test_plan_path} not found!")
        return
    
    print(f"Reading test plan from: {test_plan_path}")
    data = parse_test_plan(test_plan_path)
    
    print(f"Found {len(data['test_cases'])} test cases")
    print("Generating HTML...")
    
    html = generate_html(data)
    
    print(f"Writing HTML to: {output_path}")
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"HTML file created successfully!")
    print(f"Opening {output_path} in browser...")
    
    # Open in default browser
    webbrowser.open(f'file://{output_path.absolute()}')


if __name__ == '__main__':
    main()

