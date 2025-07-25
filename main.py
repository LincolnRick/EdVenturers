from taverna import app
from taverna.routes import *

# os cadastros utilizarão "SQL ALCHEMY DO FLASK"
# os formulários utilizarão "WTF FORMS FLASK"

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
