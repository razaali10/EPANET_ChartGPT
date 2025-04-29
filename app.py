from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import subprocess
import tempfile

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "EPANET Simulation API is running"}

@app.post("/simulate")
async def simulate(inp_file: UploadFile = File(...)):
    try:
        # Save uploaded .inp file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".inp") as temp_inp:
            temp_inp.write(await inp_file.read())
            inp_path = temp_inp.name

        # Create temp file for the report
        with tempfile.NamedTemporaryFile(delete=False, suffix=".rpt") as temp_rpt:
            rpt_path = temp_rpt.name

        # Run EPANET CLI (epanet2)
        subprocess.run(["epanet2", inp_path, rpt_path], check=True)

        # Read the output report
        with open(rpt_path, "r") as rpt_file:
            report = rpt_file.read()

        return JSONResponse(content={"report": report})

    except subprocess.CalledProcessError:
        raise HTTPException(status_code=500, detail="EPANET simulation failed.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


     
