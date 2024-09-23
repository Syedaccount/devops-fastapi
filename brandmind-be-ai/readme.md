# Brandmind

Brandmind is an innovative AI-powered project developed using FastAPI. This project aims to leverage artificial intelligence to provide advanced functionalities and solutions in automatic creation of content for diferrent brands.
## Features

- **AI Integration:** Utilize cutting-edge AI models and algorithms for automatic content generation with help of some text.
- **FastAPI Framework:** Leverage FastAPI for high-performance APIs with easy integration.
- **Scalability:** Designed to handle high loads with efficient resource management.
- **Modular Architecture:** Easily extendable and customizable based on specific needs.

## Getting Started

### Prerequisites

Ensure you have the following installed:

- Python 3.11
- Pip (Python package installer)

### Installation

1. **Clone the repository:**

    ```bash
    git clone https://xevenrepositories/brandmind-be-ai.git
    ```

2. **Navigate to the project directory:**

    ```bash
    cd brandmind
    ```

3. **Create a virtual environment:**

    ```bash
    python -m venv venv
    ```

4. **Activate the virtual environment:**

    - On Windows:

      ```bash
      venv\Scripts\activate
      ```

    - On macOS/Linux:

      ```bash
      source venv/bin/activate
      ```

5. **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

### Configuration

Configure environment variables as needed. Example configuration might include API keys, model paths, etc.

Create a `.env` file in the root directory with the following variables:

    ```dotenv
    OPENAI_API_KEY=your_api_key
    ```

### Running the Application

To start the FastAPI server, use:

```bash
uvicorn main:app --reload
