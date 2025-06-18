from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI()

# Define the input schema
class DataPayload(BaseModel):
    user_id: int
    action: str
    details: dict

@app.post("/log")
async def log_data(payload: DataPayload):
    log_message = f"Received data: user_id={payload.user_id}, action={payload.action}, details={payload.details}"
    
    # Log to console
    print(log_message)
    
    # # Log to file
    # logging.info(log_message)

    return {"status": "logged", "received": payload}
