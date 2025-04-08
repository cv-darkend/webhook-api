from fastapi import FastAPI, Query, Path, Request, Header
from typing import List, Annotated


app = FastAPI(root_path='/api')

@app.get("/")
async def read_root():
    return {"message": "Hello World"}


@app.get("/webhook")
async def webhook(
    request: Request,
    mode: Annotated[str, Query()],
    verify_token: Annotated[str, Query(alias="hub.verify_token")],
    challenge: Annotated[str, Query(alias="hub.challenge", required=False)] = None,
):
    # Verify the webhook
    if mode == "subscribe" and verify_token == "TESTING":
        if challenge:
            return int(challenge)
        return {"success": True}
    
    return {"error": "Invalid verification request"}

@app.post("/webhook")
async def webhook_post(request: Request):
    body = await request.json()
    
    # Check if this is an event from a page subscription
    if body.get("object") == "whatsapp_business_account":
        # Process the WhatsApp message
        for entry in body.get("entry", []):
            for change in entry.get("changes", []):
                if change.get("field") == "messages":
                    value = change.get("value", {})
                    if messages := value.get("messages", []):
                        # Process each message
                        for message in messages:
                            # Handle the message here
                            # Example: print(message)
                            pass
        
        # Return a 200 OK response to acknowledge receipt of the event
        return {"success": True}
    
    return {"error": "Unsupported request"}
    
