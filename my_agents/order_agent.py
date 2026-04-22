from agents import Agent, RunContextWrapper
from models import RestaurantContext
from my_agents.guardrails import restaurant_output_guardrail


def dynamic_order_agent_instructions(
    wrapper: RunContextWrapper[RestaurantContext],
    agent: Agent[RestaurantContext],
):
    return f"""
You are an Order Specialist for a restaurant, helping {wrapper.context.customer_name}.

YOUR ROLE:
- Take food and drink orders.
- Ask for missing details.
- Confirm the order clearly.
- Be concise and polite.
"""


order_agent = Agent(
    name="Order Agent",
    handoff_description="Handles taking and confirming food and drink orders.",
    instructions=dynamic_order_agent_instructions,
    output_guardrails=[restaurant_output_guardrail],
)