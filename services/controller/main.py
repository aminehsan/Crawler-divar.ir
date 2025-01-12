import uvicorn

if __name__ == '__main__':
    uvicorn.run(app='config:app', host='0.0.0.0')
