import asyncio
import dotenv
import streamlit as st

from agents import (
    Runner,
    SQLiteSession,
    InputGuardrailTripwireTriggered,
    OutputGuardrailTripwireTriggered,
)
from models import RestaurantContext
from my_agents.triage_agent import triage_agent

dotenv.load_dotenv()

restaurant_ctx = RestaurantContext(
    customer_name="Guest",
    phone=None,
    dietary_preference=None,
)

st.set_page_config(page_title="Restaurant Bot", page_icon="🍽️")
st.title("🍽️ Restaurant Bot")
st.caption("Triage + Menu + Order + Reservation + Complaints + Guardrails")


if "session" not in st.session_state:
    st.session_state["session"] = SQLiteSession(
        "restaurant-chat-history",
        "restaurant-memory.db",
    )

if "handoff_log" not in st.session_state:
    st.session_state["handoff_log"] = []

session = st.session_state["session"]


async def paint_history():
    messages = await session.get_items()
    for message in messages:
        if "role" in message:
            role = "assistant" if message["role"] == "assistant" else "user"
            with st.chat_message(role):
                if message["role"] == "user":
                    st.write(message["content"])
                else:
                    if message.get("type") == "message":
                        content = message.get("content", [])
                        if content and "text" in content[0]:
                            st.write(content[0]["text"].replace("$", "\\$"))


asyncio.run(paint_history())

with st.sidebar:
    st.subheader("Handoff Log")
    if st.session_state["handoff_log"]:
        for item in st.session_state["handoff_log"]:
            st.info(item)
    else:
        st.write("아직 handoff가 없습니다.")

    if st.button("Reset memory"):
        asyncio.run(session.clear_session())
        st.session_state["handoff_log"] = []
        st.rerun()


async def run_agent(message: str):
    with st.chat_message("assistant"):
        handoff_placeholder = st.empty()
        text_placeholder = st.empty()
        response = ""

        previous_handoff_count = len(st.session_state["handoff_log"])

        try:
            stream = Runner.run_streamed(
                triage_agent,
                message,
                session=session,
                context=restaurant_ctx,
            )

            async for event in stream.stream_events():
                if len(st.session_state["handoff_log"]) > previous_handoff_count:
                    latest = st.session_state["handoff_log"][-1]
                    handoff_placeholder.info(latest)
                    previous_handoff_count = len(st.session_state["handoff_log"])

                if event.type == "raw_response_event":
                    if event.data.type == "response.output_text.delta":
                        response += event.data.delta
                        text_placeholder.write(response.replace("$", "\\$"))

        except InputGuardrailTripwireTriggered:
            text_placeholder.write(
                "저는 레스토랑 관련 질문에 대해서만 도와드리고 있어요. "
                "메뉴 확인, 주문, 예약, 불만 접수와 같은 요청을 도와드릴 수 있습니다."
            )

        except OutputGuardrailTripwireTriggered:
            text_placeholder.write(
                "죄송합니다. 방금 응답을 안전하게 제공할 수 없어 다시 정중하게 안내드릴게요. "
                "메뉴, 주문, 예약, 또는 불만 접수 중 원하시는 내용을 말씀해 주세요."
            )


message = st.chat_input(
    "예: 예약하고 싶어요 / 채식 메뉴 있나요? / 주문할게요 / 음식이 별로였어요"
)

if message:
    with st.chat_message("user"):
        st.write(message)
    asyncio.run(run_agent(message))