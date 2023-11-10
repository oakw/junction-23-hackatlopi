from app.routes import app
from config import OriginalConfig

from dotenv import load_dotenv

load_dotenv()

if __name__ == '__main__':
  host, port = OriginalConfig.get_server_data()
  app.run(
    debug=True,
    host=host,
    port=int(port)
  )