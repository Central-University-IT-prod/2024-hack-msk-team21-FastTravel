from src.server.server import app
from pathlib import Path
ssl_context = ["/etc/letsencrypt/live/prod.merzlikinmatvey.ru/fullchain.pem", "/etc/letsencrypt/live/prod.merzlikinmatvey.ru/privkey.pem"]
if __name__ == "__main__":
    print(Path(ssl_context[0]).is_file(),Path(ssl_context[1]).is_file())
    if Path(ssl_context[0]).is_file() and Path(ssl_context[1]).is_file():
        app.run(host="0.0.0.0", port=8000,ssl_context='adhoc')
    else:
        app.run(host="0.0.0.0", port=8000)