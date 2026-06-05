from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain_core.messages import HumanMessage
from .agent import agent_executor

app = FastAPI(title="Drive Agent API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, replace "*" with your Streamlit URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str

@app.get("/")
def read_root():
    return {"status": "Drive Agent is online"}

@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        input_message = HumanMessage(content=request.message)
        result_state = agent_executor.invoke({"messages": [input_message]})
        final_response = result_state["messages"][-1].content
        
        return {"response": final_response}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)