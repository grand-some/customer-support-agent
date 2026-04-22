from agents import Agent, RunContextWrapper
from models import RestaurantContext
from my_agents.guardrails import restaurant_output_guardrail


def dynamic_reservation_agent_instructions(
    wrapper: RunContextWrapper[RestaurantContext],
    agent: Agent[RestaurantContext],
):
    return f"""
You are a Reservation Specialist for a restaurant, helping {wrapper.context.customer_name}.

YOUR ROLE:
- Help guests reserve a table.
- Collect date, time, party size, name, and phone if missing.
- Confirm reservation details clearly.
- Do not pretend a real back-end booking is guaranteed.
"""


reservation_agent = Agent(
    name="Reservation Agent",
    handoff_description="Handles table reservations and booking details.",
    instructions=dynamic_reservation_agent_instructions,
    output_guardrails=[restaurant_output_guardrail],
)