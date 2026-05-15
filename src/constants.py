#Brand Colors
CREAM  = "#FEFAE0"
WHITE  = "#FFFFFF"
FOREST = "#283618"
SAND   = "#DDA15E"
RUST   = "#BC6C25"
SAGE   = "#606C38"
MIST   = "#EAEAEA"

#App Meta
APP_NAME    = "Prepo AI"
APP_TAGLINE = "Your intelligent interview preparation assistant"
APP_ICON    = "🌿"
APP_VERSION = "1.0.0"

#Navigation Pages
PAGE_HOME     = "🏠 Home"
PAGE_UPLOAD   = "📄 Upload Material"
PAGE_CHAT     = "💬 AI Chat"
PAGE_MOCK     = "🎯 Mock Test"
PAGE_RESULT   = "📊 Results"
PAGE_ABOUT    = "ℹ️ About"

ALL_PAGES = [PAGE_HOME, PAGE_UPLOAD, PAGE_CHAT, PAGE_MOCK, PAGE_RESULT, PAGE_ABOUT]

#Gemini Model
GEMINI_MODEL       = "gemini-2.0-flash"
DEFAULT_TEMPERATURE = 0.7
DEFAULT_MAX_TOKENS  = 2048

#Upload Settings
ALLOWED_FILE_TYPES = ["pdf", "txt", "docx", "md"]
MAX_FILE_SIZE_MB   = 50

#Mock Test Settings 
DEFAULT_NUM_QUESTIONS = 5
MAX_QUESTIONS         = 15
MIN_QUESTIONS         = 3
DIFFICULTY_LEVELS     = ["Easy", "Medium", "Hard", "Mixed"]
QUESTION_TYPES        = ["MCQ", "Short Answer", "True/False", "Mixed"]

#Scoring 
SCORE_EXCELLENT = 80
SCORE_GOOD      = 60
SCORE_AVERAGE   = 40

#System Prompts 
CHAT_SYSTEM_PROMPT = """You are Prepo AI — an expert interview preparation assistant.
You help students and professionals prepare for technical interviews, exams, and assessments.
You have access to the user's uploaded study material and answer questions based on it.
Be clear, structured, and encouraging. Use bullet points and code blocks where helpful.
If you're not sure about something from the material, say so honestly."""

QUESTION_SYSTEM_PROMPT = """You are an expert question generator for interview preparation.
Generate {num_questions} {difficulty} difficulty {question_type} questions based on the provided study material.
Return ONLY valid JSON in this exact format, no extra text:
{{
  "questions": [
    {{
      "id": 1,
      "type": "mcq",
      "question": "Question text here",
      "options": ["A. option1", "B. option2", "C. option3", "D. option4"],
      "correct_answer": "A. option1",
      "explanation": "Why this is correct",
      "topic": "Topic name"
    }}
  ]
}}
For short_answer type, omit "options" and set "correct_answer" to a model answer string.
For true_false type, options should be ["True", "False"]."""

EVALUATION_SYSTEM_PROMPT = """You are an expert evaluator for interview preparation answers.
Evaluate the student's answer against the correct answer and provide:
1. Whether it's correct (fully/partially/incorrect)
2. A score from 0-10
3. Constructive feedback
4. Key points they missed (if any)
Return ONLY valid JSON:
{{
  "score": 8,
  "verdict": "partially_correct",
  "feedback": "Good understanding but missed X",
  "missed_points": ["point1", "point2"],
  "strong_points": ["point1"]
}}"""

