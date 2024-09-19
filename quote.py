from fasthtml.common import *
import random

app, rt = fast_app()

# In-memory database for quotes
quotes = [
    {"text": "Be the change you wish to see in the world.", "author": "Mahatma Gandhi", "votes": 0},
    {"text": "Stay hungry, stay foolish.", "author": "Steve Jobs", "votes": 0},
    {"text": "The only way to do great work is to love what you do.", "author": "Steve Jobs", "votes": 0},
]

@rt('/')
def get():
    content = Container(
        # H1("Random Quote Generator"),  # Keep only this title
        Div(id="quote-display"),
        Button("Get Random Quote", hx_post="/random-quote", hx_target="#quote-display"),
        H2("Add a New Quote"),
        Form(
            Input(name="text", placeholder="Enter quote text"),
            Input(name="author", placeholder="Enter author name"),
            Button("Add Quote", type="submit"),
            hx_post="/add-quote",
            hx_target="#quote-list",
            hx_swap="beforeend"
        ),
        H2("All Quotes"),
        Ul(id="quote-list", *[quote_item(i, q) for i, q in enumerate(quotes)])
    )
    return Titled("Random Quote Generator", content)  # This sets the page title

def quote_item(index, quote):
    return Li(
        P(f'"{quote["text"]}" - {quote["author"]}'),
        Div(
            f"Votes: {quote['votes']}",
            Button("👍", hx_post=f"/vote/{index}/up", hx_target="closest li"),
            Button("👎", hx_post=f"/vote/{index}/down", hx_target="closest li"),
            id=f"vote-count-{index}"
        )
    )

@rt('/random-quote')
def post():
    if quotes:
        quote = random.choice(quotes)
        return Div(
            H3(f'"{quote["text"]}"'),
            P(f"- {quote['author']}"),
            P(f"Votes: {quote['votes']}")
        )
    else:
        return P("No quotes available. Add some!")

@rt('/add-quote')
def post(text: str, author: str):
    new_quote = {"text": text, "author": author, "votes": 0}
    quotes.append(new_quote)
    return quote_item(len(quotes) - 1, new_quote)

@rt('/vote/{index}/{direction}')
def post(index: int, direction: str):
    if 0 <= index < len(quotes):
        if direction == "up":
            quotes[index]["votes"] += 1
        elif direction == "down":
            quotes[index]["votes"] = max(0, quotes[index]["votes"] - 1)
    return quote_item(index, quotes[index])

serve()