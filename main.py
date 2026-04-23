from fastapi import FastAPI


app = FastAPI(title='FunPayCopy')

@app.get('/')
async def ping_status():
    return 200