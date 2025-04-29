from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import subprocess
import os
import tempfile

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to EPANET Simulation API"}

@app.post("/simulate")
async def simulate(inp_file: UploadFile = File(...)):
    try:
        # Save uploaded file to temp location
        with tempfile.NamedTemporaryFile(delete=False, suffix=".inp", dir="/tmp") as temp_inp:
            inp_content = await inp_file.read()
            temp_inp.write(inp_content)
            inp_path = temp_inp.name

        # Prepare a temporary file for output report
        with tempfile.NamedTemporaryFile(delete=False, suffix=".rpt", dir="/tmp") as temp_rpt:
            rpt_path = temp_rpt.name

        # Run EPANET simulation (pass both input and output paths)
        result = subprocess.check_output(
            ["epanet2", inp_path, rpt_path],
            stderr=subprocess.STDOUT
        ).decode()

        # Read the generated report file
        with open(rpt_path, "r") as f:
            report_content = f.read()

        # Return the report content
        return JSONResponse(content={"report": report_content})

    except subprocess.CalledProcessError as e:
        return JSONResponse(content={"error": f"EPANET simulation failed: {e.output.decode()}"}, status_code=500)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

