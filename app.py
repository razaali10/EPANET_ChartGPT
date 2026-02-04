import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# -------------------------------------------------------------------
# App setup
# -------------------------------------------------------------------

app = FastAPI(
    title="EPANET ChartGPT API",
    description="Run EPANET models deployed on Render",
    version="1.0.0"
)

# -------------------------------------------------------------------
# Paths
# -------------------------------------------------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODELS_DIR = os.path.join(BASE_DIR, "models")

if not os.path.isdir(MODELS_DIR):
    os.makedirs(MODELS_DIR, exist_ok=True)

# -------------------------------------------------------------------
# Request schema
# -------------------------------------------------------------------

class EpanetRequest(BaseModel):
    inp_file: str

# -------------------------------------------------------------------
# Core EPANET runner (placeholder – keep your existing logic)
# -------------------------------------------------------------------

def run_epanet_model(inp_path: str) -> dict:
    """
    Run EPANET using an existing implementation.
    Replace the internals of this function with your current logic.
    """

    # ---------------------------------------------------------------
    # IMPORTANT:
    # Insert your existing EPANET execution code here.
    # This function MUST use inp_path as the full path.
    # ---------------------------------------------------------------

    # Example placeholder return structure
    return {
        "summary": "Simulation completed successfully",
        "status_report": "No hydraulic errors",
        "energy": "",
        "tanks": "",
        "quality": "",
        "controls": "",
        "raw_report": ""
    }

# -------------------------------------------------------------------
# Run simulation endpoint
# -------------------------------------------------------------------

@app.post("/run")
def run_epanet(request: EpanetRequest):
    inp_filename = request.inp_file

    # Block path traversal
    if "/" in inp_filename or "\\" in inp_filename:
        raise HTTPException(
            status_code=400,
            detail="Invalid filename. Only bare filenames are allowed."
        )

    inp_path = os.path.join(MODELS_DIR, inp_filename)

    if not os.path.isfile(inp_path):
        raise HTTPException(
            status_code=404,
            detail=f"Input file not found: {inp_filename}"
        )

    try:
        results = run_epanet_model(inp_path)
        return results

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"EPANET execution failed: {str(e)}"
        )

# -------------------------------------------------------------------
# List available models (recommended)
# -------------------------------------------------------------------

@app.get("/models")
def list_models():
    try:
        models = sorted(
            f for f in os.listdir(MODELS_DIR)
            if f.lower().endswith(".inp")
        )
        return {"models": models}

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

# -------------------------------------------------------------------
# Health check
# -------------------------------------------------------------------

@app.get("/")
def health_check():
    return {
        "status": "ok",
        "models_directory": MODELS_DIR
    }
