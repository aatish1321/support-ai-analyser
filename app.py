import streamlit as st
from dotenv import load_dotenv
import os
from groq import Groq
import json
from pydantic import BaseModel



class TicketAnalysis(BaseModel):
    category: str
    urgency: str
    sentiment: str
    summary: str
    key_issues: list[str]
    recommended_actions: list[str]
    customer_response: str



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
                        "role": "system",
                        "content":  """You are an expert customer support operations analyst. 
                     Analyze the ticket and output ONLY valid JSON using this exact structure:
                    {
                        "category": "Issue category (e.g., Delivery, Billing, Tech Support)",
                        "urgency": "Low, Medium, or High",
                        "sentiment": "Positive, Neutral, or Negative",
                        "summary": "1-2 sentence summary",
                        "key_issues": ["bullet 1", "bullet 2"],
                        "recommended_actions": ["step 1", "step 2"],
                        "customer_response": "A polite, professional draft reply to the customer"
                    }"""
                
                    },
                                   


                    {
                        "role": "user",
                        "content": f"Briefly summarize this customer support ticket: {ticket}",
                    }

                ],
                model="openai/gpt-oss-20b",
                temperature=0.2,
                max_tokens=800,
                response_format={"type": "json_object"},
            )
            
            raw_text = response.choices[0].message.content
            validated_data = TicketAnalysis.model_validate_json(raw_text)
            st.json(validated_data.model_dump())

