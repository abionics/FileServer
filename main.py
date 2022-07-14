import uvicorn

if __name__ == '__main__':
    uvicorn.run('api:app', port=8000, log_level='debug', reload=True)
