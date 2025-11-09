# ai_cybersecurity_threat_detector


🚀 Project Setup & Run Guide

This project consists of three parts:

Model Training

Backend Server

Frontend (React App)

You’ll be running each part in separate terminals, so keep them open.

1️⃣ Train the AI Model (First Time Only)

Open a new terminal:

cd model


Install model dependencies:

pip install -r requirements.txt


Train the model:

python train_model.py


✅ After training, the model weights will be saved here:

model/pretrained/model_weights.pth

2️⃣ Start the Backend Server

Open a second terminal:

cd backend


Create and activate a virtual environment:

python -m venv venv


PowerShell (Windows):

venv\Scripts\Activate.ps1


Install dependencies:

pip install -r requirements.txt


Run the backend:

python app.py


✅ Backend is now running.

3️⃣ Start the Frontend (React App)

Open a third terminal:

cd frontend


Install UI dependencies (only needed once):

npm install


Start the React UI:

npm start


✅ Frontend will open automatically at:

http://localhost:3000
