# AI Support Ticket Analyzer

A standalone Python application that helps customer support teams turn a complaint into an actionable analysis. Streamlit provides the web interface, and the Groq API generates the analysis using `openai/gpt-oss-20b`.

## Features

Paste one support ticket to generate:

- Issue category, such as Delivery, Billing, or Tech Support
- Urgency: Low, Medium, or High
- Customer sentiment: Positive, Neutral, or Negative
- A summary of one or two sentences
- Key issues as bullet points
- Recommended actions as numbered steps
- A polite, professional draft response to the customer

Results appear as readable text with Markdown formatting. The current application handles one pasted ticket at a time; CSV upload and ticket grouping are not implemented.

## Requirements

- Python 3.12
- uv installed and available in your terminal
- A Groq API key and an internet connection

## Setup and run

Run these commands from the project directory:

```bash
uv sync
```

Create a `.env` file in the project directory containing:

```dotenv
GROQ_API_KEY=your_groq_api_key_here
```

The app loads this file before creating the Groq client. You can also provide the key through your environment. `.env` is excluded from version control by `.gitignore`.

Start the application:

```bash
uv run streamlit run app.py
```

Open the local URL shown in the terminal, normally http://localhost:8501. Paste a ticket and click **Analyze Ticket**. Press **Ctrl+C** in the terminal to stop the application.

## How it works

1. Streamlit collects the ticket in a text area.
2. An empty or whitespace-only ticket triggers a warning without an API request.
3. The app sends a system message with analysis instructions and a user message containing the ticket to Groq.
4. A spinner is displayed while the request runs.
5. The generated answer is extracted from the first response choice and displayed using `st.markdown()`.

The application uses a pretrained model through an API; it does not train or fine-tune a model. It performs classification, summarization, sentiment analysis, issue extraction, action recommendation, and response drafting in a single request.

## Prompting techniques

| Technique | Use in this application |
|---|---|
| Role prompting | Assigns the model the role of an expert customer support operations analyst. |
| Zero-shot prompting | Requests an analysis without completed ticket-and-answer examples. |
| Output-format instructions | Requests named sections, bullet points, and numbered actions. |
| Constraints and tone guidance | Specifies urgency and sentiment labels, summary length, and a polite, professional reply. |

The system message defines the reusable instructions. The user message inserts the actual ticket through a Python f-string. The app does not explicitly request chain-of-thought reasoning or use few-shot examples.

## Model parameters

The request in `app.py` uses:

| Parameter | Value | Purpose |
|---|---|---|
| `model` | `openai/gpt-oss-20b` | Selects the model served by Groq. |
| `temperature` | `0.2` | Encourages less varied wording for support analysis; does not guarantee identical or correct answers. |
| `max_tokens` | `1000` | Limits generation length. Long responses can be cut off. |

These values are configured in code. Output is plain text rather than JSON, and its structure is guided by the prompt rather than validated against a schema.

## Error handling

- Empty input shows a warning.
- Groq API errors, including connection failures and rejected requests, show a friendly message asking the user to check their API key and connection and retry.

There is no explicit check for a missing API key. If no key is available when the Groq client is created, startup can fail before the request error handler runs.

## Example

**Input**

> I ordered a keyboard two weeks ago. The tracking says delivered but I never received anything. This is the second time I'm contacting support and nobody has helped me.

**Illustrative output — actual wording may vary:**

```text
Category: Delivery
Urgency: High
Sentiment: Negative

Summary:
The customer's keyboard is marked as delivered but has not been received.
They have already contacted support without a resolution.

Key issues:
- Package not received despite delivered status
- Previous support contact did not resolve the problem

Recommended actions:
1. Verify the delivery address and tracking details.
2. Request proof of delivery from the courier.
3. Review replacement or refund options under company policy.

Customer response:
I'm sorry your keyboard has not arrived and that your previous contact
has not resolved this. We will investigate the delivery details and
review the available next steps with you.
```

## Tests

```bash
uv run python -m unittest test_app.py
```

The tests use Streamlit's testing tools with mocked Groq responses to verify text rendering and API failure handling. They do not call the live API or require a real API key.

## Project files

| File | Purpose |
|---|---|
| `app.py` | Streamlit interface, prompt, API request, and error handling |
| `test_app.py` | Local tests with mocked API responses |
| `pyproject.toml` | Python version and dependencies |
| `uv.lock` | Locked dependency versions |
| `.gitignore` | Excludes local environments, secrets, and generated files |

## Limitations

The model's labels, recommendations, and draft replies may be incorrect and should be reviewed by a person. It has no access to order records, courier systems, or company policies. Ticket content is sent to the Groq API for processing. Results are not saved by this application.
