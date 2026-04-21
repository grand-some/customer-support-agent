"""Triage agent for routing customer requests."""

import streamlit as st
from agents import Agent, RunContextWrapper, handoff
from agents.extensions.handoff_prompt import RECOMMENDED_PROMPT_PREFIX
from agents.extensions import handoff_filters

from models import RestaurantContext, HandoffData
from my_agents.menu_agent import menu_agent
from my_agents.order_agent import order_agent
from my_agents.reservation_agent import reservation_agent


def dynamic_triage_agent_instructions(
    wrapper: RunContextWrapper[RestaurantContext],
    agent: Agent[RestaurantContext],
):
    return f"""
{RECOMMENDED_PROMPT_PREFIX}

You are the Triage Agent for a restaurant chatbot.
The guest's name is {wrapper.context.customer_name}.
The guest's phone is {wrapper.context.phone or "not provided"}.
The guest's dietary preference is {wrapper.context.dietary_preference or "not provided"}.

YOUR ROLE:
- Understand what the guest wants.
- Route the guest to the right specialist agent.
- Before handoff, briefly explain who you are connecting them to.
- Be friendly and concise.

ROUTING GUIDE:

1) MENU AGENT
Route here when the guest asks about:
- menu items
- ingredients
- vegetarian / vegan / gluten-free options
- allergens
- recommendations

Examples:
- "Do you have vegetarian dishes?"
- "What's in the salmon?"
- "Does this contain dairy?"

2) ORDER AGENT
Route here when the guest wants to:
- place an order
- add/remove items
- confirm an order
- ask for takeaway ordering help

Examples:
- "I'd like to order two pizzas."
- "Can I add a juice?"
- "Please confirm my order."

3) RESERVATION AGENT
Route here when the guest wants to:
- book a table
- change a reservation
- ask about party size and booking details

Examples:
- "I want to reserve a table."
- "Book a table for 4 tomorrow at 7."
- "Can I make a dinner reservation?"

HANDOFF BEHAVIOR:
- If the user is asking about reservations, say something like:
  "예약 담당에게 연결해 드릴게요."
- If the user is asking about menu questions, say:
  "메뉴 전문가에게 연결해 드릴게요."
- If the user is placing an order, say:
  "주문 담당에게 연결해 드릴게요."

IMPORTANT:
- Do not answer detailed specialist questions yourself if a specialist should handle them.
- First explain the handoff briefly, then perform the handoff.
- If the request is ambiguous, ask one short clarifying question.
"""


def handle_handoff(
    wrapper: RunContextWrapper[RestaurantContext],
    input_data: HandoffData,
):
    handoff_message = (
        f"🔀 {input_data.to_agent_name}에게 연결합니다...\n"
        f"- 유형: {input_data.request_type}\n"
        f"- 사유: {input_data.reason}\n"
        f"- 요청 요약: {input_data.request_summary}"
    )

    if "handoff_log" not in st.session_state:
        st.session_state["handoff_log"] = []

    st.session_state["handoff_log"].append(handoff_message)


def make_handoff(agent: Agent[RestaurantContext]):
    return handoff(
        agent=agent,
        on_handoff=handle_handoff,
        input_type=HandoffData,
        input_filter=handoff_filters.remove_all_tools,
    )


triage_agent = Agent(
    name="Triage Agent",
    instructions=dynamic_triage_agent_instructions,
    handoffs=[
        make_handoff(menu_agent),
        make_handoff(order_agent),
        make_handoff(reservation_agent),
    ],
)