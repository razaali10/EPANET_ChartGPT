from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import subprocess
import os

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to EPANET Simulation API"}

@app.post("/simulate")
async def simulate(inp_file: UploadFile = File(...)):
    try:
        filename = inp_file.filename
        file_location = f"/tmp/{filename}"
        with open(file_location, "wb") as f:
            f.write(await inp_file.read())

        result = subprocess.check_output(["epanet2", file_location], stderr=subprocess.STDOUT).decode()
        return JSONResponse(content={"report": result})
    except subprocess.CalledProcessError as e:
        return JSONResponse(content={"error": "EPANET simulation failed."}, status_code=500)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
       
