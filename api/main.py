from fastapi import FastAPI, Response, BackgroundTasks
from cbm_dec import generate_steered_image, generate_interpretable_image
from fastapi.middleware.cors import CORSMiddleware
import base64
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.environ.get("WEBAPP_URL")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/steer")
async def steer(background_tasks: BackgroundTasks, number: int = 0, color: str = "green"):
    image_buf = generate_steered_image(number, color)
    background_tasks.add_task(image_buf.close)
    headers = {'Content-Disposition': 'inline; filename="out.png"'}
    return Response(image_buf.getvalue(), headers=headers, media_type='image/png')

@app.get("/interpret")
async def interpret(background_tasks: BackgroundTasks):
    image_buf, probs = generate_interpretable_image()
    image_b64 = base64.b64encode(image_buf.getvalue())
    background_tasks.add_task(image_buf.close)

    return {
        "mime": "image/png",
        "image": image_b64,
        "data": probs.tolist()
    }

