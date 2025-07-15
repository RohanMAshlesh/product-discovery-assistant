# Product Discovery Assistant

## Demo

[Watch the demo on Loom](https://www.loom.com/share/8c424cc8c0e64463b91c8daeaaa7e418?sid=e887722e-c13d-4a87-9800-53ed48fcd523)

AI-powered, one-page Streamlit web app to guide users through product discovery frameworks and dynamic seat pricing.

## Features
- **Framework Analysis:** Jobs to Be Done, Value Proposition Canvas, Opportunity Solution Tree, 4-Fit Model
- **Case Study Mode:** Compare your idea with real companies
- **Dynamic Seat Pricing:** PM-style logic for per-seat pricing based on view, distance, demand, and more
- **Price Drop Notification:** Ribbon appears when the highest-priced seat drops in price
- **Downloadable Reports:** Export strategy reports as TXT or PDF
- **Modern UI:** Clean, responsive, and professional design

## Setup
1. **Clone the repo:**
   ```bash
   git clone https://github.com/RohanMAshlesh/product-discovery-assistant.git
   cd product-discovery-assistant
   ```
2. **Create and activate a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Set your OpenRouter API key:**
   - Add your key to `.env` as `OPENROUTER_API_KEY="sk-..."`

## Usage
```bash
streamlit run app.py
```
- Open the app in your browser (usually at http://localhost:8501)
- Enter your product idea, answer follow-up questions, and explore analyses
- Try Case Study Mode for company comparisons
- Use the seat pricing demo to see dynamic pricing and notifications

## Author
**Rohan M Ashlesh**

---

*Built with Streamlit, OpenAI, and love.* 