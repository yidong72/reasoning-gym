from fastapi import FastAPI, HTTPException
from reasoning_gym.utils import ScoreAnswer
from pydantic import BaseModel
import uvicorn


class ScoreRequest(BaseModel):
    answer: str
    entry: str
    task: str


app = FastAPI(title="Reward Server")
score_answer = ScoreAnswer()
@app.post("/score")
async def score(request: ScoreRequest):
    score = score_answer.score_answer(request.answer, request.entry, request.task)
    return {"score": score}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8288)
