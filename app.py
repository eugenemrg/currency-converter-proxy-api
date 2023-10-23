from fastapi import FastAPI, Response, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import redis
import requests
import os

app = FastAPI()

APP_API_KEY = os.getenv('CONVERTER_API_KEY', None)

REDIS_URL = os.getenv('REDIS_URL')
store = redis.from_url(REDIS_URL)

"""
Allow CORS for API requests

Read more here: https://fastapi.tiangolo.com/tutorial/cors/
"""
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/')
async def index():
    # Check if rates are cached and return cached values if possible
    conversion_rates = store.get('USD')
    if conversion_rates:
        return Response(conversion_rates, status_code=200, media_type='application/json')
    
    if not APP_API_KEY:
        raise HTTPException(
            status_code=500,
            detail='Server encountered an error and could unfortunately not complete the request'
        )
    else:
        r = requests.get(f'https://v6.exchangerate-api.com/v6/{APP_API_KEY}/latest/USD')
        if r.status_code == 200:
            # Cache newly received rates
            store.set('USD', r.text)
            store.expire('USD', 43200)
            
            return Response(r.content, status_code=200, media_type='application/json')
        else:
            raise HTTPException(
                status_code=502,
                detail='Server is unable to complete the request at the moment'
            )

@app.get('/rates/{base_currency}')
async def get_rates(base_currency):
    # Check if rates are cached and return cached values if possible
    conversion_rates = store.get(base_currency)
    if conversion_rates:
        return Response(conversion_rates, status_code=200, media_type='application/json')
        
    if not APP_API_KEY:
        raise HTTPException(
            status_code=500,
            detail='Server encountered an error and could unfortunately not complete the request'
        )
    else:
        r = requests.get(f'https://v6.exchangerate-api.com/v6/{APP_API_KEY}/latest/{base_currency}')
        if r.status_code == 200:
            # Cache newly received rates
            store.set(base_currency, r.text)
            store.expire(base_currency, 43200)
            
            return Response(r.content, status_code=200, media_type='application/json')
        else:
            raise HTTPException(
                status_code=502,
                detail='Server is unable to complete the request at the moment'
            )

@app.get('/convert/{base_currency}/{target_currency}/{amount}')
async def convert(base_currency: str, target_currency: str, amount: float):
    if not APP_API_KEY:
        raise HTTPException(
            status_code=500,
            detail='Server encountered an error and could unfortunately not complete the request'
        )
    else:
        r = requests.get(f'https://v6.exchangerate-api.com/v6/{APP_API_KEY}/pair/{base_currency}/{target_currency}/{amount}')
        if r.status_code == 200:
            return Response(r.content, status_code=200, media_type='application/json')
        else:
            raise HTTPException(
                status_code=502,
                detail='Server is unable to complete the request at the moment'
            )

# if __name__ == '__main__':
#     port = os.getenv('PORT', 10000)
#     uvicorn.run('app:app', host='0.0.0.0', port=port, log_level='info', reload=True)