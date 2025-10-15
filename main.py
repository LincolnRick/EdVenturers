try:
    from taverna import app
except Exception:
    try:
        from taverna import create_app
        app = create_app()
    except Exception:
        from flask import Flask
        app = Flask(__name__)

from taverna.routes import *

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
