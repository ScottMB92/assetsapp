from app import create_app
import os

host = os.getenv('FLASK_RUN_HOST', '0.0.0.0')
port = int(os.getenv('FLASK_RUN_PORT', 80))

app = create_app()

app.secret_key = os.getenv('SECRET_KEY')

if __name__ == '__main__':
    app.run(host=host, port=port)