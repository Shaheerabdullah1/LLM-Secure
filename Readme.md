# LLM-Secure

## Overview
This project serves as a testing phase for multiple Large Language Models providing security while utilizing the forefront of innovation that can achieved through propietary LLMs.


The repository consists of both a **backend API** (written in Python) and a **frontend** (built with Node.js and Vite).

## Folder Structure

```
LLM-Privacy/
│── src/                  # Source code directory
│── myenv/                # Python virtual environment
│── node_modules/         # Node.js dependencies
│── api-final-bot.py      # Final API bot
│── api-middle-bot.py     # Middleware API bot
│── client.py             # Client-side script
│── index.html            # Main HTML file
│── package.json          # Node.js dependencies
│── postcss.config.js     # PostCSS configuration
│── tailwind.config.js    # Tailwind CSS configuration
│── vite.config.js        # Vite configuration
│── run.py                # Main script to start the backend API
│── requirements.txt      # Python dependencies
```

## Installation and Setup

### Backend (Python API)

#### 1. Create and Activate a Virtual Environment
```sh
python -m venv myenv  # Create virtual environment
source myenv/bin/activate  # Activate on macOS/Linux
myenv\Scripts\activate  # Activate on Windows
```

#### 2. Install Dependencies
```sh
pip install -r requirements.txt
```

#### 3. Run the API Server
```sh
python run.py
```

### Frontend (Node.js with Vite)

#### 1. Install Dependencies
```sh
npm install
```

#### 2. Start the Frontend
```sh
npm run dev
```
This will start the development server for the frontend.

## Environment Variables

Ensure you set up your `.env` file with the necessary configurations before running the project.

### Example `.env` File
```env
MIDDLE_BOT_API_KEY=your_middle_bot_api_key_here  # Groq API Key
TARGET_CHATBOT_API_KEY=your_target_chatbot_api_key_here  # Groq API Key
```
These API keys are required for interacting with the Groq API services.

## Contributing

Feel free to **fork this project** and make improvements. If you encounter any issues, please open a **pull request** or create an **issue**.

## License

This project is open-source and available under the **Apache 2.0 License**.


