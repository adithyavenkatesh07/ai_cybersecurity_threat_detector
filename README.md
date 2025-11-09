# ai_cybersecurity_threat_detector

<h2 align="center">🚀 Project Setup & Run Guide</h2>

<p>This project has three main parts:</p>
<ol>
  <li><strong>Model Training</strong></li>
  <li><strong>Backend Server</strong></li>
  <li><strong>Frontend (React UI)</strong></li>
</ol>

<hr/>

<h3>1️⃣ Train the AI Model (First Time Only)</h3>

<pre>
<b>Open a new terminal:</b>
cd model

<b>Install dependencies:</b>
pip install -r requirements.txt

<b>Train the model:</b>
python train_model.py
</pre>

<p>✅ The trained model will be saved at:</p>
<pre>model/pretrained/model_weights.pth</pre>

<hr/>

<h3>2️⃣ Start the Backend Server</h3>

<pre>
<b>Open another terminal:</b>
cd backend

<b>Create Virtual Environment:</b>
python -m venv venv

<b>Activate (PowerShell on Windows):</b>
venv\Scripts\Activate.ps1

<b>Install backend dependencies:</b>
pip install -r requirements.txt

<b>Start the backend:</b>
python app.py
</pre>

<p>✅ Backend is now running.</p>

<hr/>

<h3>3️⃣ Start the Frontend (React App)</h3>

<pre>
<b>Open a third terminal:</b>
cd frontend

<b>Install dependencies (only once):</b>
npm install

<b>Start the development server:</b>
npm start
</pre>

<p>✅ App will be available at:</p>
<pre>http://localhost:3000</pre>

<hr/>

<h3>🎯 Summary</h3>

<table>
  <thead>
    <tr>
      <th>Component</th>
      <th>Command</th>
      <th>Terminal</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Model Training</td>
      <td><code>python train_model.py</code></td>
      <td>#1</td>
    </tr>
    <tr>
      <td>Backend Server</td>
      <td><code>python app.py</code></td>
      <td>#2</td>
    </tr>
    <tr>
      <td>Frontend UI</td>
      <td><code>npm start</code></td>
      <td>#3</td>
    </tr>
  </tbody>
</table>
