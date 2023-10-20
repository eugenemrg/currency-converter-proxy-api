from fastapi import FastAPI, Response
import uvicorn
import requests

app = FastAPI()

@app.get('/')
async def index():
    r = requests.get('https://v6.exchangerate-api.com/v6/1234456789/latest/USD')
    return Response(r.content, status_code=200, media_type='application.json')

if __name__ == '__main__':
    uvicorn.run('app:app', port=5555, log_level='info', reload=True)