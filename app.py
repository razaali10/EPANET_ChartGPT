from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import subprocess
import tempfile
import os

app = FastAPI()

@app.get("/")
def root():
    return {"message": "EPANET Simulation API is running"}

@app.post("/simulate")
async def simulate(inp_file: UploadFile = File(...)):
    try:
        # Save uploaded .inp file to a temp location
        with tempfile.NamedTemporaryFile(delete=False, suffix=".inp") as temp_inp:
            inp_content = await inp_file.read()
            temp_inp.write(inp_content)
            inp_path = temp_inp.name

        # Create temp file path for .rpt output
        rpt_path = inp_path.replace(".inp", ".rpt")

        # Run EPANET CLI (requires both input and output paths)
        subprocess.run(["epanet2", inp_path, rpt_path], check=True)

        # Check if .rpt was created and has content
        if not os.path.exists(rpt_path) or os.path.getsize(rpt_path) == 0:
            raise HTTPException(status_code=500, detail="Simulation failed: .rpt file not created.")

        # Read and return the report content
        with open(rpt_path, "r") as rpt_file:
            report_content = rpt_file.read()

        return JSONResponse(content={"report": report_content})

    except subprocess.CalledProcessError as e:
        return JSONResponse(
            content={"error": "EPANET execution failed.", "details": e.output.decode() if e.output else str(e)},
            status_code=500
        )
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

     

     
