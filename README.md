```
uvicorn backend.main:app --reload
```


## Requirements

- Python 3.8+
- An [OpenAI API key](https://platform.openai.com/)
- The packages listed in `requirements.txt`

---

## Installation

1. **Clone the repository:**
   ```sh
   git clone https://github.com/EnzoHashinokutiXavier/HolyMind.git
   cd ScripturaAI
   ```

2. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

3. **Set your OpenAI API key as an environment variable:**

   On Windows (Command Prompt):
   ```sh
   setx OPENAI_API_KEY "your-openai-key"
   ```
   Note: After running this command, close your terminal and open a new one before starting the backend, so the environment variable is recognized.
   
   On Linux/Mac:
   ```sh
   export OPENAI_API_KEY="your-openai-key"
   ```

---

## Usage

1. **Start the backend server:**
   ```sh
   uvicorn backend.main:app --reload
   ```

2. **Access the frontend:**  
   Open [http://localhost:8000](http://localhost:8000) in your browser.

3. **Enter a Bible excerpt and choose the type of explanation.**
