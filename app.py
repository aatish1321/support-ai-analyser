import streamlit as st
from dotenv import load_dotenv
import os
from groq import Groq

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
            response = client.chat.completions.create(
                messages=[

                    {
                        "role":"system",
                        "content":"""You are an expert customer support operations analyst. Your job is to analyze customer support tickets and provide a brief summary of the issue, the urgency, 
                        and any recommended actions. Please provide a concise summary in strict formatting using markdown and use use bold labels or bullet points for the Summary, Urgency, and Recommended Actions."""
                    },
                                   


                    {
                        "role": "user",
                        "content": f"Briefly summarize this customer support ticket: {ticket}",
                    }

                ],
                model="openai/gpt-oss-20b",
                temperature=0.2,
                max_tokens=300
            )
            
            st.write(response.choices[0].message.content)

