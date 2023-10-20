from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get('/')
async def index():
    return {'msg':'Hello, World!'}

if __name__ == '__main__':
    uvicorn.run('app:app', port=5555, log_level='info', reload=True)