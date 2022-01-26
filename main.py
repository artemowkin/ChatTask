from fastapi import FastAPI, WebSocket, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

app.mount('/static', StaticFiles(directory='static'), name='static')

templates = Jinja2Templates(directory='templates')


@app.get('/', response_class=HTMLResponse)
async def index_page(request: Request):
    return templates.TemplateResponse('index.html', {'request': request})


@app.websocket('/ws')
async def websocket_messages_endpoint(websocket: WebSocket):
    await websocket.accept()
    message_id = 1
    while True:
        data = await websocket.receive_json()
        data['order'] = message_id
        await websocket.send_json(data)
        message_id += 1
