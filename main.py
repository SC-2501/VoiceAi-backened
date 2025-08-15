# main.py
# To run this code:
# 1. Install the necessary libraries:
#    pip install fastapi "uvicorn[standard]"
# 2. Save the code as a file named `main.py`.
# 3. Open your terminal or command prompt.
# 4. Navigate to the directory where you saved the file.
# 5. Run the command: uvicorn main:app --reload

from fastapi import FastAPI
from pydantic import BaseModel
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- Pydantic Models for Request and Response ---
# This defines the structure of the data you expect to receive.
class QueryRequest(BaseModel):
    """Represents the user's query sent from the app."""
    language: str
    text: str

# This defines the structure of the data you will send back.
class SchemeResponse(BaseModel):
    """Represents the scheme information returned to the app."""
    name: str
    description: str
    eligibility: str
    link: str

# --- Initialize FastAPI App ---
app = FastAPI(
    title="VoiceAI Bharat API",
    description="API for providing information about government schemes.",
    version="1.0.0",
)

# --- Dummy Database ---
# In a real application, this data would come from a database like PostgreSQL, MongoDB, etc.
# This is a simplified example with a few schemes.
DUMMY_SCHEMES_DB = {
    "pradhan mantri kisan samman nidhi": {
        "name": "Pradhan Mantri Kisan Samman Nidhi (PM-KISAN)",
        "description": "A government scheme in which all small and marginal farmers will get up to ₹6,000 per year as minimum income support.",
        "eligibility": "All landholding farmer families.",
        "link": "https://pmkisan.gov.in/"
    },
    "beti bachao beti padhao": {
        "name": "Beti Bachao, Beti Padhao",
        "description": "A campaign of the Government of India that aims to generate awareness and improve the efficiency of welfare services intended for girls.",
        "eligibility": "Focused on the girl child.",
        "link": "https://wcd.nic.in/bbbp-schemes"
    },
    "pradhan mantri jan dhan yojana": {
        "name": "Pradhan Mantri Jan Dhan Yojana (PMJDY)",
        "description": "National Mission for Financial Inclusion to ensure access to financial services, namely, Banking/ Savings & Deposit Accounts, Remittance, Credit, Insurance, Pension in an affordable manner.",
        "eligibility": "Any Indian citizen above the age of 10 years.",
        "link": "https://www.pmjdy.gov.in/"
    }
}

# --- API Endpoints ---
@app.get("/")
def read_root():
    """A simple endpoint to check if the API is running."""
    logger.info("Root endpoint was accessed.")
    return {"status": "VoiceAI Bharat API is running!"}

@app.post("/query-schemes", response_model=list[SchemeResponse])
def query_schemes(request: QueryRequest):
    """
    This is the main endpoint for your app.
    It receives a user's query and returns matching schemes.
    """
    logger.info(f"Received query in {request.language}: '{request.text}'")

    query_text = request.text.lower().strip()
    matched_schemes = []

    # Simple keyword matching logic.
    # In your real app, you would use your NLP model (like IndicBERT) here
    # to understand the intent and find the best match.
    for keyword, scheme_data in DUMMY_SCHEMES_DB.items():
        if keyword in query_text:
            matched_schemes.append(SchemeResponse(**scheme_data))
            logger.info(f"Matched scheme: {scheme_data['name']}")

    if not matched_schemes:
        logger.warning(f"No schemes found for query: '{query_text}'")

    return matched_schemes

# To deploy this API, you would use a cloud provider like AWS, Google Cloud, or a service like Heroku.
# This would give you a public URL that your Flutter app can connect to.