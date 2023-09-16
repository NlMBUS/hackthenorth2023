from taipy.gui import Gui, notify

text = "Write your review here!"
rating = None

# Add a navbar to switch from one page to the other
root_md = """
<|navbar|>
# AccurRate
**True Hotel Ratings Powered by AI**
"""

page1_md = """
## Making Reviews Accurate Again

**Do you ever have trouble deciding what to rate a hotel after your visit? Do you ever worry that the rating you give isn't truly indicative of your experience?**

This is where AccurRate comes in. You simply write about your experience, and we use the power of machine learning to rate your stay for you. Our AI model has been trained on tens of thousands of reviews and ratings specifically so you can ensure your hotel rating is as accurate as possible!
"""

page2_md = """

## Write Your Review Below

#### Your Rating: <|{rating}|>

<|{text}|input|multiline|fullwidth|class_name=fullwidth|>

<|Run local|button|on_action=on_button_action|>
"""

def on_button_action(state):
    notify(state, 'info', f'The text is: {state.text}')
    state.text = "Button Pressed"

def on_change(state, var_name, var_value):
    if var_name == "text" and var_value == "Reset":
        state.text = ""
        return


pages = {
    "/": root_md,
    "Home": page1_md,
    "Rating_Tool": page2_md
}

Gui(pages=pages, css_file="static/style.css").run()
