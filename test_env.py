from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv(dotenv_path='backend/.env')

print('BACKEND_HOST:', os.getenv('BACKEND_HOST'))
print('BACKEND_PORT:', os.getenv('BACKEND_PORT'))
print('FRONTEND_PATH:', os.getenv('FRONTEND_PATH'))
