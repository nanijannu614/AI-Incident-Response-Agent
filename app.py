import streamlit as st

from incident_agent import analyze_incident
from hindsight_memory import record_incident_outcome


st.set_page_config(
    page_title="AI Incident Response Agent",
    page_icon="🚨",
    layout="wide"
)


st.title("🚨 AI Incident Response Agent")

st.write(
    "An AI agent that remembers previous production incidents, "
    "reasons over experience, and learns from new outcomes using Hindsight."
)


# ---------------------------------
# Hindsight Memory Loop
# ---------------------------------

st.subheader("🧠 Hindsight Memory Loop")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("1", "Remember", "Past incidents")

with col2:
    st.metric("2", "Reason", "Current incident")

with col3:
    st.metric("3", "Learn", "New outcomes")


# ---------------------------------
# Analyze Incident
# ---------------------------------

st.subheader("🔍 Analyze a Production Incident")

incident = st.text_area(
    "Describe the production incident",
    placeholder=(
        "Example: The payment provider is experiencing heavy traffic "
        "and our API has started returning Service Unavailable responses."
    ),
    height=120
)


if st.button(
    "🔍 Analyze Incident",
    use_container_width=True
):

    if incident.strip():

        with st.spinner(
            "Hindsight is recalling experience and analyzing the incident..."
        ):

            analysis = analyze_incident(incident)

        st.session_state["incident"] = incident
        st.session_state["analysis"] = analysis

    else:

        st.warning(
            "Please describe the production incident first."
        )


# ---------------------------------
# AI Analysis
# ---------------------------------

if "analysis" in st.session_state:

    st.subheader("🤖 AI Incident Analysis")

    st.markdown(
        st.session_state["analysis"]
    )


    # ---------------------------------
    # Memory Evidence
    # ---------------------------------

    st.divider()

    st.subheader("🧠 Hindsight Memory Evidence")

    st.info(
        "The analysis above was generated using Hindsight's stored "
        "incident experiences. Relevant past incidents are used as "
        "evidence, while unrelated incidents are explicitly rejected."
    )

    st.write(
        "**Memory behavior demonstrated:**"
    )

    st.markdown(
        """
        - 🔎 **Recall:** Finds relevant previous incident experience
        - 🧩 **Compare:** Compares the current incident with past incidents
        - ✅ **Reuse:** Uses proven solutions when the incident is sufficiently similar
        - 🚫 **Reject:** Avoids applying unrelated incident solutions
        - 🧠 **Learn:** Stores new outcomes for future incidents
        """
    )


    # ---------------------------------
    # Teach Agent
    # ---------------------------------

    st.divider()

    st.subheader("🧠 Teach the Agent What Happened")

    st.write(
        "After applying the recommendation, record the actual outcome. "
        "Hindsight will retain this experience for future incidents."
    )


    root_cause = st.text_input(
        "Confirmed root cause",
        placeholder="Example: Upstream payment service overload"
    )


    solution = st.text_input(
        "Action taken",
        placeholder=(
            "Example: Enabled circuit breaker and exponential backoff"
        )
    )


    outcome = st.text_area(
        "Outcome",
        placeholder=(
            "Example: 503 errors stopped and the payment service recovered."
        ),
        height=100
    )


    if st.button(
        "🧠 Store Incident Experience",
        use_container_width=True
    ):

        if (
            root_cause.strip()
            and solution.strip()
            and outcome.strip()
        ):

            record_incident_outcome(
                st.session_state["incident"],
                root_cause,
                solution,
                outcome
            )

            st.success(
                "✅ Experience stored in Hindsight. "
                "The agent can use it for future incidents."
            )

            st.session_state["learned"] = True

        else:

            st.warning(
                "Please fill in the root cause, action taken, "
                "and outcome."
            )


# ---------------------------------
# Learning Confirmation
# ---------------------------------

if st.session_state.get("learned"):

    st.divider()

    st.success(
        "🔄 Learning complete — this incident outcome is now part "
        "of the agent's future experience."
    )