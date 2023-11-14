# drivesage_app

## How to run the code:
- ensure docker is installed (for windows: https://docs.docker.com/desktop/install/windows-install/)
- build the docker image: `docker build -t my_app .`
- start the application `docker run my_app`


## Documentation

# File Structure:

drivesage_app/
|-- app.py
|-- templates/
|   |-- index.html
|-- requirements.txt
|-- API_config.yaml
|-- Dockerfile

- drivesage_app: The main folder for your project.
- app.py: Your Flask application.
- templates: Folder containing HTML templates.
- requirements.txt: File listing Python dependencies for your Flask app.
- API_config.yaml: Configuration file containing API keys.
- Dockerfile: File for Docker container configuration.