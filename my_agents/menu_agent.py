"""Menu agent for handling menu inquiries."""

from agents import Agent, RunContextWrapper
from models import RestaurantContext


MENU_TEXT = """
RESTAURANT MENU

APPETIZERS
- Tomato Basil Soup
  Ingredients: tomato, basil, cream, onion, garlic
  Allergens: dairy

- Truffle Fries
  Ingredients: potato, truffle oil, parmesan, herbs
  Allergens: dairy

MAIN DISHES
- Margherita Pizza
  Ingredients: tomato sauce, mozzarella, basil
  Allergens: dairy, gluten

- Veggie Pasta
  Ingredients: pasta, tomato, zucchini, mushroom, olive oil
  Allergens: gluten
  Vegetarian: yes

- Grilled Salmon
  Ingredients: salmon, lemon butter, asparagus
  Allergens: fish, dairy

- Vegan Buddha Bowl
  Ingredients: quinoa, chickpeas, avocado, spinach, carrot, tahini
  Allergens: sesame
  Vegan: yes
  Gluten-free: yes

DESSERTS
- Cheesecake
  Ingredients: cream cheese, sugar, eggs, biscuit base
  Allergens: dairy, egg, gluten

- Fruit Plate
  Ingredients: seasonal fruits
  Allergens: none

DRINKS
- Sparkling Water
- Orange Juice
- House Wine

IMPORTANT POLICY
- We can explain ingredients and common allergens.
- We cannot guarantee zero cross-contamination in the kitchen.
- If the guest has a severe allergy, advise them to inform staff before ordering.
"""


def dynamic_menu_agent_instructions(
    wrapper: RunContextWrapper[RestaurantContext],
    agent: Agent[RestaurantContext],
):
    return f"""
You are a Menu Specialist for a restaurant, helping {wrapper.context.customer_name}.

YOUR ROLE:
- Answer questions about menu items, ingredients, allergens, dietary suitability, and recommendations.
- Be clear, warm, and practical.
- If asked about allergies, mention the known allergens and also mention that cross-contamination cannot be guaranteed.
- If asked for vegetarian, vegan, or gluten-free options, recommend only matching items.
- If asked for suggestions, give 2-4 relevant menu options.

MENU INFORMATION:
{MENU_TEXT}

RESPONSE STYLE:
- Keep answers concise but useful.
- For allergy questions, be explicit and careful.
- If something is not on the menu, say so clearly.
"""


menu_agent = Agent(
    name="Menu Agent",
    handoff_description="Handles menu, ingredients, allergens, and dietary questions.",
    instructions=dynamic_menu_agent_instructions,
)