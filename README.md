# MockAI

## Project Overview
This project is designed for the Mock AI interview process.

### Backend
The backend application is developed using Python Django and utilizes various REST frameworks. To run the project, follow these steps:
1. Clone the GitHub repository.
2. Download all the files and ensure you have the `requirements.txt` file.
3. Execute the following commands in your terminal:
python manage.py makemigrations
python manage.py migrate
python manage.py runserver

The backend project consists of APIs for user registration, user login, and user communication with the API. Open API has been used for API integrations.

### Frontend
Due to issues with uploading to GitHub, the frontend project is hosted on Google Drive. You can download the frontend code from the following link: [Frontend Code](https://drive.google.com/file/d/1z_EPP5nDGiue_qq_dFKIEla25zJxQsVU/view?usp=sharing)

The frontend application enables communication with the backend using JSON objects. It allows users to:
- Record audio.
- Send messages or ask questions.
- Send snapshots of drawings on the canvas.
- Receive feedback from the AI hosted on the backend.

The webpage facilitates user registration with the required information. After registration, users can log in and utilize the various features, including asking questions, drawing on the whiteboard, and recording their responses.


