<h1 align="center">🤖 AI Interview Preparation Assistant</h1>

<p align="center">
An AI-powered web application that generates structured interview questions and answers based on job role and experience level.
</p>

<hr>

<h2>👨‍💻 Author</h2>
<p><b>Sk Aminur Rahman</b></p>

<hr>

<h2>🚀 Features</h2>
<ul>
  <li>🎯 Generate interview questions (Easy, Medium, Hard)</li>
  <li>🧠 AI-powered responses using local LLM (Ollama)</li>
  <li>🔐 User Authentication (Register, Login, Logout)</li>
  <li>🔑 JWT Authentication System</li>
  <li>🔁 Password Reset (Token-based)</li>
  <li>📝 Interview History Tracking</li>
  <li>📄 Detailed View of Past Sessions</li>
  <li>🧪 Unit Testing for Models & APIs</li>
</ul>

<hr>

<h2>🛠️ Tech Stack</h2>
<ul>
  <li><b>Backend:</b> Django, Django REST Framework</li>
  <li><b>Database:</b> SQLite</li>
  <li><b>Authentication:</b> JWT (JSON Web Tokens)</li>
  <li><b>AI Model:</b> Ollama (llama3.2:1b)</li>
  <li><b>Frontend:</b> HTML, CSS, JavaScript (AJAX)</li>
</ul>

<hr>

<h2>⚙️ Complete Setup Guide</h2>

<h3>1️⃣ Clone the Repository</h3>
<pre>
git clone https://github.com/your-username/ai-interview-assistant.git
cd ai-interview-assistant
</pre>

<h3>2️⃣ Create Virtual Environment</h3>
<pre>
python -m venv env
</pre>

<h3>Activate Virtual Environment:</h3>
<ul>
  <li><b>Windows:</b></li>
  <pre>env\Scripts\activate</pre>
  <li><b>Mac/Linux:</b></li>
  <pre>source env/bin/activate</pre>
</ul>

<h3>3️⃣ Install Dependencies</h3>
<pre>
pip install -r requirements.txt
</pre>

<h3>4️⃣ Apply Migrations</h3>
<pre>
python manage.py makemigrations
python manage.py migrate
</pre>

<hr>

<h2>🤖 Install & Setup Ollama (VERY IMPORTANT)</h2>

<h3>Step 1: Install Ollama</h3>
<p>Download and install Ollama from the official website:</p>

<p>
👉 https://ollama.com/download
</p>

<h3>Step 2: Verify Installation</h3>
<pre>
ollama --version
</pre>

<h3>Step 3: Pull the Required Model</h3>
<pre>
ollama pull llama3.2:1b
</pre>

<h3>Step 4: Run the Model</h3>
<pre>
ollama run llama3.2:1b
</pre>

<p>
⚠️ This step is <b>mandatory</b>. The AI will NOT work if Ollama is not running.
</p>

<p>
The application sends requests to:
</p>
<pre>
http://localhost:11434/api/chat
</pre>

<hr>

<h2>▶️ Run the Project</h2>

<pre>
python manage.py runserver
</pre>

<p>Open your browser and go to:</p>

<pre>
http://127.0.0.1:8000/
</pre>

<hr>

<h2>📌 How to Use</h2>

<ol>
  <li>Register a new account</li>
  <li>Login to the system</li>
  <li>Select:
    <ul>
      <li>Job Role</li>
      <li>Experience Level</li>
    </ul>
  </li>
  <li>Click Generate</li>
  <li>View AI-generated:
    <ul>
      <li>Easy Question + Answer</li>
      <li>Medium Question + Answer</li>
      <li>Hard Question + Answer</li>
    </ul>
  </li>
  <li>Access previous results in <b>History</b></li>
</ol>

<hr>

<h2>🔌 API Endpoints</h2>

<table border="1" cellpadding="8">
<tr>
<th>Method</th>
<th>Endpoint</th>
<th>Description</th>
</tr>

<tr>
<td>POST</td>
<td>/api/register/</td>
<td>Register new user</td>
</tr>

<tr>
<td>POST</td>
<td>/api/login/</td>
<td>Login user</td>
</tr>

<tr>
<td>POST</td>
<td>/api/logout/</td>
<td>Logout user</td>
</tr>

<tr>
<td>POST</td>
<td>/api/token/refresh/</td>
<td>Refresh JWT token</td>
</tr>

<tr>
<td>GET</td>
<td>/api/history/</td>
<td>Get user history</td>
</tr>

<tr>
<td>POST</td>
<td>/api/history/</td>
<td>Generate interview questions</td>
</tr>

<tr>
<td>GET</td>
<td>/api/details/&lt;id&gt;/</td>
<td>Get specific interview details</td>
</tr>

</table>

<hr>

<h2>🧪 Run Tests</h2>

<pre>
python manage.py test
</pre>

<p>Includes testing for:</p>
<ul>
  <li>User Model</li>
  <li>History Model</li>
  <li>Authentication APIs</li>
  <li>Password Reset Flow</li>
  <li>Protected Routes</li>
</ul>

<hr>

<h2>⚠️ Important Notes</h2>

<ul>
  <li>Ollama must be running before generating questions</li>
  <li>Ensure port <b>11434</b> is not blocked</li>
  <li>Project will not generate AI responses without the model</li>
</ul>

<hr>

<h2>⭐ Support</h2>

<p>If you found this project useful, consider giving it a ⭐ on GitHub.</p>

<hr>