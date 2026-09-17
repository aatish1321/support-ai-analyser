import streamlit as st

st.set_page_config(
    page_title="AI Support Ticket Analyzer",
    page_icon="🎫",
    layout="wide",
)

st.title("AI Customer Support Ticket Analyzer")

st.write(
    "Analyze customer support tickets using generative AI."
)

ticket = st.text_area(
    "Enter a customer support ticket:",
    height=200,
    placeholder="Example: My package says delivered but I never received it..."
)

if st.button("Analyze Ticket", type="primary"):
    if not ticket.strip():
        st.warning("Please enter a customer support ticket.")
    else:
        st.success("Ticket received!")
        st.write(ticket)