# Pope - Python Scope
The idea is to make post-processing of measurements on scopes by different vendors easier and more interactive.

## State
Highly Experimental - Is not very useful yet.

## Development

### Download source
```bash
    git clone https://github.com/seimsel/pope.git
```

### Run backend
```bash 
    cd pope/backend
    pip install -r requirements.txt # requires python3
    uvicorn --reload --port 8000 main:app
```

### Run frontend
In a seperate terminal window:
```bash
    cd pope/frontend
    npm install

    export BACKEND_HTTP_URL=http://localhost:8000
    export BACKEND_WS_URL=ws://localhost:8000
    npm run dev
```
