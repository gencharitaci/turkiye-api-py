import os

import uvicorn
from dotenv import load_dotenv

load_dotenv()

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8181))
    host = os.getenv("HOST", "0.0.0.0")

    uvicorn.run("app.main:app", host=host, port=port, reload=True, log_level="info")
