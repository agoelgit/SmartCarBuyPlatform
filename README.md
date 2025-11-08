# SmartCarBuyerPlatform

A conversational AI platform to help users explore, filter, and get insights about vehicles, including electric cars, MOT status, and specifications. The platform uses MongoDB for structured vehicle data, ChromaDB for semantic search, and OpenAI LLM for generating conversational summaries.

---

## Features

- Search vehicles by make, model, price, or specifications.
- Filter vehicles under a specified price.
- Identify electric vehicles and cars with specific features (e.g., heat pumps).
- Retrieve MOT status and compliance information.
- Generate user-friendly summaries of vehicles using a large language model (LLM).
- Supports natural language queries like:
  - "Show me Hyundai Kona under £20k and when its MOT is due"
  - "Show me electric vehicles"
  - "Show me cars with heat pumps"

---

## Architecture

The platform is orchestrated via **CrewAI-style agents**:

| Agent           | Responsibility |
|-----------------|----------------|
| **DataAgent**   | Retrieves vehicle data from MongoDB and performs semantic search using ChromaDB. |
| **SpecAgent**   | Extracts and analyzes vehicle specifications (fuel type, CO2, color, etc.). |
| **MOTAgent**    | Handles MOT, tax, and compliance-related queries. |
| **InsightAgent**| Summarizes and generates conversational responses using OpenAI LLM. |
| **ChatAgent**   | Main orchestrator that combines all agents and processes user queries. |

---

## Installation

1. **Clone the repository:**
```bash
git clone https://github.com/yourusername/SmartCarBuyerPlatform.git
cd SmartCarBuyerPlatform

2. **Create a Virtual Environment:**
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

3. **Install Dependencies:**
pip install -r requirements.txt

3. **Set Environment Variables**
# Windows
set OPENAI_API_KEY="your_openai_api_key"
# macOS/Linux
export OPENAI_API_KEY="your_openai_api_key"

4. **Database Setup**
{
  "make": "Hyundai",
  "model": "Kona EV",
  "modelDescription": "Hyundai Kona Electric Premium",
  "price": 19995,
  "fuel": "Electric",
  "co2": 0,
  "color": "Blue",
  "mileage": 5000,
  "extras": "Heat pump"
}

5. **ChromaDB: Used for semantic search.**
python sync_embeddings.py

6. **Run the App**
python app.py

7. **Programmatic Access (CrewAI-style)**
from crew.zorqk_crew import process_user_query

response = process_user_query("Show me electric vehicles under £25k")
print(response)

8. **Project Structure**
SmartCarBuyerPlatform/
│
├─ agents/
│  ├─ chat_agent.py
│  ├─ data_agent.py
│  ├─ spec_agent.py
│  ├─ mot_agent.py
│  └─ insight_agent.py
│
├─ crew/
│  └─ zorqk_crew.py
│
├─ services/
│  ├─ db_service.py
│  ├─ mongo_service.py
│  └─ openai_service.py
│
├─ sync_embeddings.py
├─ app.py
├─ requirements.txt
└─ README.md

9. **Chroma DB Structure**
SmartCarBuyerPlatform/
├─ data/
│  ├─ chroma_db/   # ChromaDB storage
│  └─ vehicles.json  # Optional JSON backup of vehicle data

License

## 🧑‍💻 Author
 
**👋 Developed by:** _[Aneesh Goel]_
📧 Email: [goel.aneesh@gmail.com](mailto:goel.aneesh@gmail.com)
 
---
 
## 🪪 License
 
This project is licensed under the **MIT License** – feel free to use, modify, and share!
 

