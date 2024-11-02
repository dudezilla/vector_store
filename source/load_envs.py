import os
from dotenv import load_dotenv

def load_env():
    if not os.path.exists('.env'):
        default_env = {
            'NOMIC_API_KEY': 'YOUR SECRET KEY GOES HERE'
        }
        with open('.env', 'w') as f:
            for key, value in default_env.items():
                f.write(f'{key}={value}\n')
    
    load_dotenv()