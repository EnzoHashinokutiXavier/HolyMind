# HolyMind

A project developed for biblical learning.
With several features, the project currently includes an AI assistant that explains Bible passages in various ways, useful for both laymen and those looking to deepen their knowledge.
Find Bible passages by book, chapter, and verse!

## Requirements

- Python 3.8+
- An [OpenAI API key](https://platform.openai.com/)
- The packages listed in `requirements.txt`

---

## Installation

1. **Clone the repository:**
   ```sh
   git clone https://github.com/EnzoHashinokutiXavier/HolyMind.git
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

<img width="1098" height="323" alt="image" src="https://github.com/user-attachments/assets/818dcff7-7f56-40cd-9e84-8cd1d4b69ccd" />


## Usage

1. **Start the backend server:**
   ```sh
   uvicorn backend.main:app --reload
   ```

2. **Access the frontend:**  
   Open [http://localhost:8000](http://localhost:8000) in your browser.

<img width="1914" height="630" alt="image" src="https://github.com/user-attachments/assets/ab932efd-bf16-44f7-b94a-aca5916a9d0f" />
