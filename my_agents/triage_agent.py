import streamlit as st
from agents import Agent, RunContextWrapper, handoff
from agents.extensions.handoff_prompt import RECOMMENDED_PROMPT_PREFIX
from agents.extensions import handoff_filters

from models import RestaurantContext, HandoffData
from my_agents.menu_agent import menu_agent
from my_agents.order_agent import order_agent
from my_agents.reservation_agent import reservation_agent
from my_agents.complaints_agent import complaints_agent
from my_agents.guardrails import (
    restaurant_input_guardrail,
    restaurant_output_guardrail,
)


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
- Route the guest to the right specialist.
- Before handoff, briefly explain who you are connecting them to.
- Be warm, concise, and professional.

ROUTING GUIDE:

1) MENU AGENT
For:
- menu items
- ingredients
- vegetarian / vegan / gluten-free options
- allergens
- recommendations

2) ORDER AGENT
For:
- placing an order
- modifying an order
- confirming an order

3) RESERVATION AGENT
For:
- booking a table
- changing reservation details
- reservation questions

4) COMPLAINTS AGENT
For:
- bad food experience
- rude staff
- long wait complaints
- wrong order complaints
- refund/discount/manager request
- dissatisfaction with service

Examples:
- "음식이 너무 별로였어"
- "직원이 너무 불친절했어"
- "환불 받고 싶어"
- "서비스가 엉망이었어"

IMPORTANT:
- If the user is off-topic, do not help with the off-topic request.
- If the request is ambiguous, ask one short clarifying question.
- If routing:
  - Menu -> "메뉴 전문가에게 연결해 드릴게요."
  - Order -> "주문 담당에게 연결해 드릴게요."
  - Reservation -> "예약 담당에게 연결해 드릴게요."
  - Complaints -> "불편을 드려 죄송합니다. 불만 처리 담당에게 연결해 드릴게요."
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
    input_guardrails=[restaurant_input_guardrail],
    output_guardrails=[restaurant_output_guardrail],
    handoffs=[
        make_handoff(menu_agent),
        make_handoff(order_agent),
        make_handoff(reservation_agent),
        make_handoff(complaints_agent),
    ],
)