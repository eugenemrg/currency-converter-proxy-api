from fastapi import FastAPI, Response, HTTPException
import uvicorn
import requests
import os

app = FastAPI()

APP_API_KEY = os.getenv('CONVERTER_API_KEY', None)

@app.get('/')
async def index():
    if not APP_API_KEY:
        raise HTTPException(
            status_code=500,
            detail='Server encountered an error and could unfortunately not complete the request'
        )
    else:
        r = requests.get(f'https://v6.exchangerate-api.com/v6/{APP_API_KEY}/latest/USD')
        if r.status_code == 200:
            return Response(r.content, status_code=200, media_type='application/json')
        else:
            raise HTTPException(
                status_code=502,
                detail='Server is unable to complete the request at the moment'
            )

if __name__ == '__main__':
    uvicorn.run('app:app', port=5555, log_level='info', reload=True)