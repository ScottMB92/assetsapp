from app import create_app
import os
from dotenv import load_dotenv

# Specify the full file path to the .env file
dotenv_path = '/app/.env'  # Adjust the path as needed

load_dotenv(dotenv_path)

if __name__ == '__main__':
    # Access environment variables, including host and port, from the loaded .env file
    host = os.getenv('FLASK_RUN_HOST', '0.0.0.0')
    port = int(os.getenv('FLASK_RUN_PORT', 80))

    app = create_app()

    # Set the Flask app's secret key from the environment variable
    app.secret_key = os.getenv('SECRET_KEY')

    app.run(host=host, port=port)
