"""
Lightweight AI quick-reply / FAQ assistant for the chat widget.

This starts as a rule-based FAQ matcher so the feature works with zero
external dependencies or API keys. When you're ready, replace the body
of `generate_quick_replies` / `answer_faq` with a call to an LLM (e.g.
the Anthropic Messages API) — keep the same function signatures so the
views and templates don't need to change.
"""

FAQ_KEYWORDS = {
    "financing": "We offer flexible financing plans with competitive rates. "
                 "You can apply directly from the vehicle page — approval decisions "
                 "are typically instant.",
    "finance": "We offer flexible financing plans with competitive rates. "
               "You can apply directly from the vehicle page — approval decisions "
               "are typically instant.",
    "shipping": "Velora Motors ships worldwide via air and ocean freight, with full "
                "tracking and customs support. Use the Shipping Calculator on the "
                "vehicle page for an instant estimate.",
    "warranty": "Most certified pre-owned vehicles include an extended warranty. "
                "Warranty terms vary by dealer and vehicle — ask the dealer directly "
                "in this chat for the specifics on this listing.",
    "insurance": "We partner with several insurers to get you a quote in minutes — "
                 "look for the Insurance Quote button on the vehicle page.",
    "trade-in": "You can get an instant AI-estimated trade-in value from your "
                "Buyer Dashboard, then apply it toward this vehicle.",
    "trade in": "You can get an instant AI-estimated trade-in value from your "
                "Buyer Dashboard, then apply it toward this vehicle.",
    "test drive": "You can request a test drive directly from the vehicle page — "
                  "the dealer will confirm a time with you here in chat.",
    "vin": "You can decode any VIN using the VIN Verification tool on the vehicle "
           "page to confirm its history and specifications.",
}

DEFAULT_SUGGESTIONS = [
    "Is this vehicle still available?",
    "Can you share the full vehicle history report?",
    "Would you consider a reasonable offer?",
    "What financing options are available?",
]


def answer_faq(message_text: str) -> str | None:
    text = message_text.lower()
    for keyword, answer in FAQ_KEYWORDS.items():
        if keyword in text:
            return answer
    return None


def generate_quick_replies(vehicle=None) -> list[str]:
    if vehicle is None:
        return DEFAULT_SUGGESTIONS
    return [
        f"Is the {vehicle.year} {vehicle.make} {vehicle.model} still available?",
        "Can I schedule a test drive?",
        "Would you consider financing options?",
        "Can you share the vehicle history report?",
    ]
