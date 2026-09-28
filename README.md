## Project: AI Support Ticket Analyzer

# A user pastes a customer complaint/support ticket, or uploads a CSV containing many tickets. Your application processes each ticket and generates:

- Issue category
- Short summary
- Urgency level
- Customer sentiment
- Key problem extracted
- Recommended action
- Draft response to the customer
- Optional grouping of multiple tickets into common problem areas

## Usage example

**Input**

> I ordered a keyboard two weeks ago. The tracking says delivered but I never received anything. This is the second time I'm contacting support and nobody has helped me.

**Output**

```text
Category: Delivery issue
Urgency: High
Sentiment: Frustrated

Summary:
Customer's keyboard is marked as delivered but was not received.
They have already contacted support once.

Recommended action:
1. Verify tracking information.
2. Confirm delivery address.
3. Contact courier.
4. Offer replacement/refund if delivery cannot be confirmed.

Suggested response:
Hi,
I'm sorry you've had to contact us again...
```
