# VJUBOT Project

A robust, multi-component chatbot application utilizing **Rasa** for intent recognition, **RAG** (Retrieval Augmented Generation) for knowledge retrieval, and **Streamlit** for an interactive frontend interface.

## Project Structure

* **Rag:** Contains the retrieval augmented generation component.
* **Rasa:** Houses the Rasa chatbot framework.
* **VJU_chatbot:** Contains the Streamlit web application for the chatbot interface.

## Setup and Installation

### Prerequisites

- **Docker** and **Docker Compose** are required for containerized setup.
- **Python 3.8+** if setting up dependencies locally instead of using Docker.

### Step 1: Clone the Repository

```bash
git clone https://github.com/Trungnef/VJUBOT.git
cd VJUBOT
```
### Step 2: Environment Configuration
Navigate to each subdirectory (Rag, Rasa, and VJU_chatbot) and create a .env file based on the .env_example file in each directory. Fill in the required environment variables for each component.

### Step 3: Install Dependencies (Optional)
For local setup, navigate to each subdirectory and install the required dependencies:

```bash
cd Rag
pip install -r requirements.txt

cd ../Rasa
pip install -r requirements.txt

cd ../VJU_chatbot
pip install -r requirements.txt
```

## Running the Project
### Starting the Services
- Start all services using Docker Compose:
```bash
docker-compose up -d
```
This command will build and start the following services:

- vju_chatbot: Streamlit application (accessible at http://localhost:8501).
- rag-server: RAG server for retrieval (port 8002).
- rasa-server: Rasa server for intent handling (port 5005).
- rasa-actions-server: Rasa actions server for custom actions (port 5055).
- duckling-server: Duckling server for entity extraction (port 8000).

### Stopping the Services
- To stop the services:
```bash
docker-compose down
```

## Troubleshooting
- Port Conflicts: If ports are in use, modify port mappings in the docker-compose.yml file.
- Dependency Issues: Ensure all dependencies are installed as outlined in each component’s requirements.txt.
- Docker Issues: Verify Docker is running and you have the necessary permissions.
## Contributing
We welcome contributions! Please open an issue or submit a pull request to contribute to this project.

## License
This project is licensed under the MIT License.
