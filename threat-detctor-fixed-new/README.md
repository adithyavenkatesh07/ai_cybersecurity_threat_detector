

### 4.2 Train the AI Model (First Time Only)

Open **ANOTHER NEW terminal** window and run:

cd model

# Install model dependencies
pip install -r requirements.txt

# Train the model
python train_model.py



✅ **Model trained and saved to `model/pretrained/model_weights.pth`**

--------------------------------------------------------------------------------------

### 4.3 Start the Backend in new terminal (now you should have 2 terminals):

cd backend

# Create virtual environment
python -m venv venv

# Activate (PowerShell)
venv\Scripts\Activate.ps1

pip install -r requirements.txt

python app.py

-----------------------------------------------------------------------------------------

### 4.4 Start the Frontend

Open **ANOTHER NEW terminal** window (you should now have 3 terminals open):

cd frontend

# Install dependencies (if not done already)
npm install

# Start the React development server
npm start





