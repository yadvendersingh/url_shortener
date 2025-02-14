# URL Shortener

This is a URL Shortener application that consists of a backend API built with FastAPI and a frontend UI built with Streamlit. The application can be containerized using Docker.

## Files

- `backend.py`: Contains the FastAPI code to create the API for the URL shortener.
- `frontend.py`: Contains the Streamlit code to create the UI for the URL shortener.

## Running the Application

### Using Docker

1. Build the Docker image:

    ```sh
    docker build -t url_shortener .
    ```

2. Run the Docker container:

    ```sh
    docker run -p 8000:8000 -p 8501:8501 url_shortener
    ```

### Without Docker

1. Install the required dependencies:

    ```sh
    pip install -r requirements.txt
    ```

3. Run the backend:

    ```sh
    uvicorn backend:app --host 0.0.0.0 --port 8000 
    ```

3. Run the frontend:

    ```sh
    streamlit run frontend.py --server.port 8501
    ```

## Accessing the Application

- Backend API: `http://localhost:8000`
- Frontend UI: `http://localhost:8501`

## License

This project is licensed under the MIT License.
