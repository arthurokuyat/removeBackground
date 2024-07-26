# Background Removal Web Application

This project is a web application that removes the background from uploaded images using the `rembg` library. It's built with Flask and can be containerized with Docker for easy deployment, including to Google Cloud Run.

## Features

- Upload an image file
- Remove the background from the uploaded image
- Download the processed image with a transparent background

## Prerequisites

- Python 3.9+
- Docker (for containerization and deployment)
- Google Cloud account (for deployment to Cloud Run)

## Local Setup

1. Clone the repository:
   ```
   git clone <repository-url>
   cd <repository-name>
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Run the application:
   ```
   python app.py
   ```

5. Open a web browser and navigate to `http://localhost:5000`

## Docker Build and Run

1. Build the Docker image:
   ```
   docker build -t remove_bg .
   ```

2. Run the Docker container:
   ```
   docker run -p 5000:5000 remove_bg
   ```

3. Access the application at `http://localhost:5000`

## Deploying to Google Cloud Run

1. Install and initialize the [Google Cloud SDK](https://cloud.google.com/sdk/docs/install)

2. Authenticate with Google Cloud:
   ```
   gcloud auth login
   ```

3. Set your project ID:
   ```
   gcloud config set project YOUR_PROJECT_ID
   ```

4. Build and push the Docker image to Google Container Registry:
   ```
   gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/remove-bg
   ```

5. Deploy to Cloud Run:
   ```
   gcloud run deploy remove-bg --image gcr.io/YOUR_PROJECT_ID/remove-bg --platform managed --region YOUR_REGION --allow-unauthenticated
   ```

6. Follow the prompts to complete the deployment

7. Once deployed, Cloud Run will provide a URL to access your application

## Project Structure

- `app.py`: Main Flask application
- `requirements.txt`: Python dependencies
- `Dockerfile`: Instructions for building the Docker image
- `templates/`: Directory containing HTML templates
- `uploads/`: Directory for storing uploaded and processed images

## Notes

- The application uses the `rembg` library, which requires the `u2net.onnx` model file. Make sure this file is present in the `/home/.u2net/` directory within the Docker container.
- The Dockerfile uses `gunicorn` as the WSGI HTTP server for production deployment.
- Ensure that your Google Cloud project has the necessary APIs enabled (Cloud Run, Container Registry, etc.)

## License

MIT License
