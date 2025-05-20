import os
import xml.etree.ElementTree as ET
from pathlib import Path
from openai import OpenAI


def get_coverage_percentage():
    tree = ET.parse('coverage.xml')
    root = tree.getroot()
    return float(root.attrib['line-rate']) * 100

def generate_tests(source_code):
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

    prompt = f"""
    Given the following Python code, generate comprehensive pytest unit tests.
    Return ONLY the test code, no explanations or comments about what you're going to do.
    Each test function should start with 'def test_' and use proper pytest assertions.
    Use MagicMock if needed to mock the response. 
    All required imports are already present, so no need to add import statements.
    
    {source_code}
    """
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a Python testing expert. Provide only valid Python test code."},
            {"role": "user", "content": prompt}
        ]
    )

     # Clean up the response to ensure it's valid Python code
    generated_tests = response.choices[0].message.content.strip()
    
    # Remove any markdown formatting if present
    if generated_tests.startswith("```python"):
        generated_tests = generated_tests.replace("```python", "").replace("```", "")
    
    return generated_tests.strip()

def push_changes():
    pat_token = os.getenv('PAT_TOKEN')
    repo_url = os.getenv('GITHUB_REPOSITORY')
    
    # Set up git with PAT
    os.system('git config --global user.email "ai-agent@example.com"')
    os.system('git config --global user.name "AI Test Generator"')
    
    # Create new branch
    branch_name = f"feature/add-tests-{os.getenv('GITHUB_SHA', '')[:7]}"
    os.system(f'git checkout -b {branch_name}')
    
    # Add and commit changes
    os.system('git add tests/test_main.py')
    os.system('git commit -m "Add generated tests to improve coverage"')
    
    # Push using PAT
    push_url = f"https://x-access-token:{pat_token}@github.com/{repo_url}.git"
    os.system(f'git push {push_url} {branch_name}')

def main():
    coverage = get_coverage_percentage()
    
    if coverage < 80:
        print(f"Current coverage: {coverage}%. Generating additional tests...")
        
        # Read source code
        with open('src/main.py', 'r') as f:
            source_code = f.read()
        
        # Generate new tests
        new_tests = generate_tests(source_code)
        
        # Validate the generated tests
        try:
            compile(new_tests, '<string>', 'exec')
        except SyntaxError as e:
            print(f"Generated tests contain syntax errors: {e}")
            return
        
        # Append new tests to existing test file
        test_file = Path('tests/test_main.py')
        with open(test_file, 'a') as f:
            f.write('\n\n# Auto-generated tests\n')
            f.write(new_tests)
        
        print("New tests have been generated and added to test_main.py")
        
        # Push changes
        push_changes()
        
    else:
        print(f"Current coverage: {coverage}%. No additional tests needed.")

if __name__ == "__main__":
    main()