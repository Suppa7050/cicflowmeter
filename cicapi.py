from fastapi import FastAPI, Response
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import subprocess
import time

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"Hello": "World"}

@app.get("/generate-csv")
def generate_csv():
    try:
        # Run cicflowmeter command to collect logs for 30 seconds and generate CSV file
        command = f"cicflowmeter -i Wi-Fi -c output.csv"
        process = subprocess.Popen(command.split(" "))

        time.sleep(120)

        process.terminate()

        # Return the generated CSV file as a response
        return FileResponse("output.csv", media_type="text/csv", filename="output.csv")
    except Exception as e:
        return Response(str(e), status_code=500)
