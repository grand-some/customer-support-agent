"""Menu agent for handling menu inquiries."""

from agents import Agent, RunContextWrapper
from models import RestaurantContext
from my_agents.guardrails import restaurant_output_guardrail


from agents import Agent, RunContextWrapper
from models import RestaurantContext
from my_agents.guardrails import restaurant_output_guardrail


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
"""


def dynamic_menu_agent_instructions(
    wrapper: RunContextWrapper[RestaurantContext],
    agent: Agent[RestaurantContext],
):
    return f"""
You are a Menu Specialist for a restaurant, helping {wrapper.context.customer_name}.

YOUR ROLE:
- Answer menu, ingredients, allergen, and dietary questions.
- Be warm, concise, and careful.
- Mention cross-contamination cannot be guaranteed for severe allergies.

MENU INFORMATION:
{MENU_TEXT}
"""


menu_agent = Agent(
    name="Menu Agent",
    handoff_description="Handles menu, ingredients, allergens, and dietary questions.",
    instructions=dynamic_menu_agent_instructions,
    output_guardrails=[restaurant_output_guardrail],
)