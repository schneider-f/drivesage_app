# drivesage_app

## How to run the code:
- ensure docker is installed (for windows: https://docs.docker.com/desktop/install/windows-install/)
- create an API_config.yaml file containing your API keys
```
# API key configuration
openai:
  api_key: YOUR_OPENAI_API_KEY_HERE

google:
  api_key: YOUR_GOOGLE_API_KEY_HERE
```
- start docker desktop to start docker daemon
- build the docker image: `docker build -t my_app .`
- start the application `docker run -p 5000:5000 -it my_app`

- useful for debug a running container: docker exec -it <container_id_or_name> /bin/bash


## Documentation

### File Structure:

```plaintext
drivesage_app/
|-- app.py
|-- pipeline.py
|-- templates/
|-- static/
|-- requirements.txt
|-- API_config.yaml
|-- Dockerfile
```

- app.py: Main Flask application.
- pipeline.py: Pipeline code for route optimization.
- templates: Folder containing HTML files.
- static: Folder containing CSS files
- requirements.txt: File listing Python dependencies for your Flask app.
- API_config.yaml: Configuration file containing API keys.
- Dockerfile: File for Docker container configuration.

### Pending modifications
- deal with cache error
- modify maps link function to cut it in part if too long
- api latency?
- generation of direction link, add time of day