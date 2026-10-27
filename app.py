import os
import streamlit as st
from dotenv import load_dotenv
from groq import APIError, Groq

load_dotenv()
client = Groq()

st.set_page_config(
    page_title="AI Support Ticket Analyzer",
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
        with st.spinner("Analyzing with ai..."):
            try:
                response = client.chat.completions.create(
                    messages=[

                        {
                            "role": "system",
                            "content":  """You are an expert customer support operations analyst.
                            Analyze the ticket and respond in readable text with these headings:
                            Category: Issue category (e.g., Delivery, Billing, Tech Support)
                            Urgency: Low, Medium, or High
                            Sentiment: Positive, Neutral, or Negative
                            Summary: 1-2 sentences
                            Key issues: A bullet list of the main problems
                            Recommended actions: A numbered list of steps
                            Customer response: A polite, professional draft reply."""

                        },



                        {
                            "role": "user",
                            "content": f"Briefly summarize this customer support ticket: {ticket}",
                        }

                    ],
                    model="openai/gpt-oss-20b",
                    temperature=0.2,
                    max_tokens=1000,
                )

            except APIError:
                st.error("Could not analyze the ticket. Check your API key and connection, then try again.")
            else:
                text = response.choices[0].message.content
                st.markdown(text)
