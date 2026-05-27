import re


STOP_WORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "by",
    "for",
    "from",
    "has",
    "have",
    "in",
    "is",
    "it",
    "of",
    "on",
    "or",
    "that",
    "the",
    "to",
    "with",
}


def clean_resume_text(text):
    text = text.lower()
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"[^a-zA-Z+#\s]", " ", text)

    tokens = text.split()
    filtered_tokens = [
        word for word in tokens
        if word not in STOP_WORDS and len(word) > 1
    ]

    return " ".join(filtered_tokens)
