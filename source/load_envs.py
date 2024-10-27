import os
from dotenv import load_dotenv

def load_env():
    if not os.path.exists('.env'):
        default_env = {
            'SAMPLE_KEY1': 'value1',
            'SAMPLE_KEY2': 'value2'
        }
        with open('.env', 'w') as f:
            for key, value in default_env.items():
                f.write(f'{key}={value}\n')
    
    load_dotenv()