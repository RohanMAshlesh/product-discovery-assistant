import os
from openai import OpenAI
from typing import Dict, List, Optional
import json

# Initialize OpenAI client with API key from environment variable
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

class ProductDiscoveryAnalyzer:
    def __init__(self):
        self.system_prompt = """You are an expert product strategist with experience from top business schools.
        Analyze the provided product idea or customer problem using various frameworks.
        Provide clear, actionable insights and maintain a professional tone."""
        
        self.case_study_companies = [
            "Uber",
            "Figma",
            "Zepto",
            "Amazon",
            "Tesla",
            "Notion",
            "Airbnb",
            "Stripe",
            "Slack",
            "Zoom"
        ]

    def _call_gpt(self, prompt: str, max_tokens: int = 1000) -> str:
        try:
            response = client.chat.completions.create(
                model="openai/gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_tokens
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error in analysis: {str(e)}"

    def prompt_jtbd(self, user_input: str) -> str:
        return f"""
You are a product strategist trained in the Jobs to Be Done (JTBD) framework.

Here is the user input describing a problem or product idea:
\"\"\"
{user_input}
\"\"\"

Please:
1. Identify the functional, emotional, and social jobs the user is trying to get done
2. Break down the job into: 
   - Main Job
   - Related Jobs
   - Emotional Jobs
3. Identify the struggling moments (where the user fails)
4. Present your answer in clear bullet points under each section
"""

    def prompt_value_prop_canvas(self, user_input: str) -> str:
        return f"""
You are an expert in using the Value Proposition Canvas to guide product discovery.

Based on this product idea or customer problem:
\"\"\"
{user_input}
\"\"\"

Please complete both sides of the canvas:
- Customer Profile:
  - Customer Jobs
  - Pains
  - Gains
- Value Map:
  - Products and Services
  - Pain Relievers
  - Gain Creators

Structure the output as clearly labeled sections with short bullet points under each.
"""

    def prompt_opp_tree(self, user_input: str) -> str:
        return f"""
You are using the Opportunity Solution Tree framework created by Teresa Torres.

For this product idea or user problem:
\"\"\"
{user_input}
\"\"\"

Do the following:
1. Define the clear product outcome or goal
2. List opportunities (user needs, pain points)
3. Brainstorm possible solutions (not full features, just ideas)
4. Suggest 1–2 experiments or small tests to validate the biggest assumptions

Present your answer in the format:
- Outcome:
- Opportunities:
- Solutions:
- Tests:
"""

    def prompt_4_fit_model(self, user_input: str) -> str:
        return f"""
Act as a product strategist evaluating an idea using the 4-Fit Model.

Given this user input:
\"\"\"
{user_input}
\"\"\"

Analyze it using these four fits:
1. Problem-Solution Fit
2. Product-Market Fit
3. Channel Fit
4. Revenue Model Fit

For each one:
- Assess the current status (Validated / Unclear / Risky)
- Explain why
- Suggest next steps or validation methods

Use bullet points and clear section headings.
"""

    def analyze_jtbd(self, product_idea: str, user_inputs: Dict) -> Dict:
        combined_input = f"{product_idea}\n\nAdditional Context:\n{json.dumps(user_inputs, indent=2)}"
        return {
            "analysis": self._call_gpt(self.prompt_jtbd(combined_input)),
            "framework": "Jobs to Be Done"
        }

    def analyze_value_proposition(self, product_idea: str, user_inputs: Dict) -> Dict:
        combined_input = f"{product_idea}\n\nAdditional Context:\n{json.dumps(user_inputs, indent=2)}"
        return {
            "analysis": self._call_gpt(self.prompt_value_prop_canvas(combined_input)),
            "framework": "Value Proposition Canvas"
        }

    def analyze_opportunity_solution(self, product_idea: str, user_inputs: Dict) -> Dict:
        combined_input = f"{product_idea}\n\nAdditional Context:\n{json.dumps(user_inputs, indent=2)}"
        return {
            "analysis": self._call_gpt(self.prompt_opp_tree(combined_input)),
            "framework": "Opportunity Solution Tree"
        }

    def analyze_four_fit(self, product_idea: str, user_inputs: Dict) -> Dict:
        combined_input = f"{product_idea}\n\nAdditional Context:\n{json.dumps(user_inputs, indent=2)}"
        return {
            "analysis": self._call_gpt(self.prompt_4_fit_model(combined_input)),
            "framework": "4-Fit Model"
        }

    def analyze_case_study(self, product_idea: str, selected_company: str, user_inputs: Dict) -> Dict:
        """Generate a case study comparison between the user's idea and a selected company."""
        prompt = f"""Compare the following product idea to {selected_company}:

Product Idea:
{product_idea}

Additional Context:
{json.dumps(user_inputs, indent=2)}

Please provide a detailed analysis in the following structure:

1. {selected_company}'s Product Strategy
   - Core value proposition
   - Key customer segments
   - Main competitive advantages

2. Strategic Comparison
   - Similarities in customer jobs and value proposition
   - Key differences in approach and positioning
   - Market overlap and potential competition

3. Strategic Lessons
   - What can be learned from {selected_company}'s approach
   - Potential pitfalls to avoid
   - Opportunities for differentiation

Format the response with clear section headers and bullet points for easy reading."""

        return {
            "analysis": self._call_gpt(prompt),
            "company": selected_company
        }

    def get_follow_up_questions(self, product_idea: str) -> List[str]:
        prompt = f"""Based on this product idea: {product_idea}
        Generate 5-7 follow-up questions that will help deepen understanding of:
        1. User pain points
        2. Current solutions
        3. Target segment
        4. Unmet needs
        Format as a numbered list."""
        
        return self._call_gpt(prompt).split('\n')

    def analyze_all_frameworks(self, product_idea: str, user_inputs: Dict) -> Dict:
        return {
            "jtbd": self.analyze_jtbd(product_idea, user_inputs),
            "value_proposition": self.analyze_value_proposition(product_idea, user_inputs),
            "opportunity_solution": self.analyze_opportunity_solution(product_idea, user_inputs),
            "four_fit": self.analyze_four_fit(product_idea, user_inputs)
        }

    def get_case_study_companies(self) -> List[str]:
        """Return the list of available case study companies."""
        return self.case_study_companies 

    def calculate_seat_price(self, base_price, view_quality, distance, section_popularity, demand_factor, accessibility):
        """
        Calculate the dynamic price for a seat based on multiple factors.
        base_price: float, the minimum price for any seat
        view_quality: float, multiplier (e.g., 1.2 for best view, 0.8 for partially obstructed)
        distance: int, number of rows from stage/screen (closer = higher price)
        section_popularity: float, multiplier (e.g., 1.3 for center, 1.0 for side)
        demand_factor: float, multiplier (e.g., 1.5 if selling fast, 1.0 if normal)
        accessibility: float, multiplier (e.g., 1.1 for aisle, 0.9 for hard-to-reach)
        """
        distance_multiplier = max(1.0, 1.5 - (distance * 0.05))
        price = base_price * view_quality * distance_multiplier * section_popularity * demand_factor * accessibility
        return round(price, 2)

    def price_seats(self, seats: list, base_price: float = 100.0) -> list:
        """
        seats: list of dicts, each with keys: view_quality, distance, section_popularity, demand_factor, accessibility
        Returns a list of dicts with seat info and calculated price.
        """
        priced_seats = []
        for seat in seats:
            price = self.calculate_seat_price(
                base_price=base_price,
                view_quality=seat.get('view_quality', 1.0),
                distance=seat.get('distance', 1),
                section_popularity=seat.get('section_popularity', 1.0),
                demand_factor=seat.get('demand_factor', 1.0),
                accessibility=seat.get('accessibility', 1.0)
            )
            seat_with_price = seat.copy()
            seat_with_price['price'] = price
            priced_seats.append(seat_with_price)
        return priced_seats

    def detect_highest_price_drop(self, old_seats, new_seats):
        """
        Returns the seat (or seats) where the highest price dropped, and the amount.
        old_seats/new_seats: list of dicts with 'id' and 'price'
        """
        old_prices = {seat['id']: seat['price'] for seat in old_seats}
        new_prices = {seat['id']: seat['price'] for seat in new_seats}
        if not old_prices or not new_prices:
            return None, 0
        old_highest_id = max(old_prices, key=old_prices.get)
        old_highest_price = old_prices[old_highest_id]
        new_highest_id = max(new_prices, key=new_prices.get)
        new_highest_price = new_prices[new_highest_id]
        # If the same seat is still the highest, but price dropped
        if old_highest_id == new_highest_id and new_highest_price < old_highest_price:
            return new_highest_id, old_highest_price - new_highest_price
        # If a different seat is now highest, check if the old highest dropped
        elif new_prices.get(old_highest_id, 0) < old_highest_price:
            return old_highest_id, old_highest_price - new_prices.get(old_highest_id, 0)
        return None, 0

    # Example usage:
    # seats = [
    #     {'view_quality': 1.2, 'distance': 1, 'section_popularity': 1.3, 'demand_factor': 1.5, 'accessibility': 1.1},
    #     {'view_quality': 0.9, 'distance': 10, 'section_popularity': 1.0, 'demand_factor': 1.0, 'accessibility': 1.0},
    # ]
    # analyzer = ProductDiscoveryAnalyzer()
    # priced = analyzer.price_seats(seats)
    # print(priced) 