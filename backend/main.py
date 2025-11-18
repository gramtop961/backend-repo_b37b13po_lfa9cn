from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

from schemas import Lead, IntentSignal, Campaign, MeetingRequest, PersonaWorkshopInput, CopywritingInput, ColdCallerMatchInput, LaunchInput
from database import db, create_document, get_documents  # provided by environment

app = FastAPI(title="Outbound AI Agency API", version="1.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health and DB test
@app.get("/test")
async def test():
    try:
        # Touch DB with a lightweight ping collection
        await create_document("health", {"status": "ok", "ts": datetime.utcnow().isoformat()})
        return {"ok": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Leads endpoints
@app.post("/leads")
async def add_lead(lead: Lead):
    doc = await create_document("lead", lead.model_dump())
    return {"inserted_id": str(doc.get("_id")), "lead": doc}

@app.get("/leads")
async def list_leads(limit: int = 50, tag: Optional[str] = None):
    filt = {}
    if tag:
        filt = {"tags": {"$in": [tag]}}
    docs = await get_documents("lead", filt, limit)
    return {"items": docs}

# Intent signals endpoints
@app.post("/intent-signals")
async def add_intent(signal: IntentSignal):
    doc = await create_document("intentsignal", signal.model_dump())
    return {"inserted_id": str(doc.get("_id")), "signal": doc}

@app.get("/intent-signals")
async def list_intents(company: Optional[str] = None, type: Optional[str] = None, limit: int = 50):
    filt = {}
    if company:
        filt["company"] = company
    if type:
        filt["type"] = type
    docs = await get_documents("intentsignal", filt, limit)
    return {"items": docs}

# Campaigns
@app.post("/campaigns")
async def create_campaign(c: Campaign):
    doc = await create_document("campaign", c.model_dump())
    return {"inserted_id": str(doc.get("_id")), "campaign": doc}

@app.get("/campaigns")
async def list_campaigns(limit: int = 50):
    docs = await get_documents("campaign", {}, limit)
    return {"items": docs}

# Methodology steps endpoints (intake forms)
@app.post("/workshops/1-meeting")
async def meeting(req: MeetingRequest):
    doc = await create_document("meetingrequest", req.model_dump())
    return {"inserted_id": str(doc.get("_id"))}

@app.post("/workshops/2-persona")
async def persona(ws: PersonaWorkshopInput):
    doc = await create_document("personaworkshopinput", ws.model_dump())
    return {"inserted_id": str(doc.get("_id"))}

@app.post("/workshops/3-copywriting")
async def copywriting(inp: CopywritingInput):
    doc = await create_document("copywritinginput", inp.model_dump())
    return {"inserted_id": str(doc.get("_id"))}

@app.post("/workshops/3-cold-caller")
async def coldcaller(inp: ColdCallerMatchInput):
    doc = await create_document("coldcallermatchinput", inp.model_dump())
    return {"inserted_id": str(doc.get("_id"))}

@app.post("/workshops/4-launch")
async def launch(inp: LaunchInput):
    doc = await create_document("launchinput", inp.model_dump())
    return {"inserted_id": str(doc.get("_id"))}
