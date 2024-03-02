from app import create_app
import os
from dotenv import load_dotenv

dotenv_path = '/app/.env'

load_dotenv(dotenv_path)

if __name__ == '__main__':
    host = os.getenv('FLASK_RUN_HOST', '0.0.0.0')
    port = int(os.getenv('PORT', 80))

    app = create_app()

    app.secret_key = os.getenv('SECRET_KEY')

    app.run(host=host, port=port)
