from taipy.gui import Gui, notify
from gpt_helpers import generate_review, generate_rating

text = "Write your review here!"
rating = None

# review vars
review_location = 3
review_cleanliness = 3
review_checkin_checkout = 3
review_service = 3
review_value = 3
review_amenities = 3

# review write control
review_iswritten = False
review_out = ""

# Add a navbar to switch from one page to the other
root_md = """
<|navbar|>
# AccurRate
**True Hotel Ratings Powered by AI**{: .padded-text }
"""

page1_md = """
## Making Reviews Accurate Again

**Do you ever have trouble deciding what to rate a hotel after your visit? Do you ever worry that the rating you give isn't truly indicative of your experience?**{: .padded-text }

**This is where AccurRate comes in. You simply write about your experience, and we use the power of machine learning to rate your stay for you. Our AI model has been trained on tens of thousands of reviews and ratings specifically so you can ensure your hotel rating is as accurate as possible!**{: .padded-text }

<br/><br/><br/>

<center><img src="static/goose.png" width="350px"/></center>

"""

page2_md = """

## Write Your Review Below

#### Your Rating: <|{rating}|id=rating|> / 5

<|{text}|input|multiline|fullwidth|class_name=fullwidth|>

<center><|Get Rating|button|on_action=on_button_action|></center>
"""

page3_md = """

## AI Powered Review Writer

**Are you confident in your ratings but not sure how to put them into words? Let AI do it for you!**{: .padded-text }

### Rate the following from 1 to 5:

<|layout|columns=1 1 1|
<|
Location: <|{review_location}|> / 5  
<|{review_location}|slider|min=1|max=5|>
|>
<|
Cleanliness: <|{review_cleanliness}|> / 5  
<|{review_cleanliness}|slider|min=1|max=5|>
|>
<|
Check In/Check Out: <|{review_checkin_checkout}|> / 5  
<|{review_checkin_checkout}|slider|min=1|max=5|>
|>  
<|
Service: <|{review_service}|> / 5  
<|{review_service}|slider|min=1|max=5|>
|>  
<|
Value For Money: <|{review_value}|> / 5  
<|{review_value}|slider|min=1|max=5|>
|>
<|
Amenities: <|{review_amenities}|> / 5  
<|{review_amenities}|slider|min=1|max=5|>
|>
|>
<center><|Write Review|button|on_action=on_write_review|></center>

<|part|render={review_iswritten}|
### Output: ### {: .text-center }

<|{review_out}|>{: .padded-text }

<br/><br/><br/><br/><br/><br/><br/>
|>

"""

def on_write_review(state):
    notify(state, 'info', 'Review Writing in Progress...')
    prompt = f"""
Write a review for a hotel given the following ratings:
Location: {state.review_location}/5, Cleanliness: {state.review_cleanliness}/5, Check in/check out: {state.review_checkin_checkout}/5, Service: {state.review_service}/5, Value for money: {state.review_value}/5, Amenities: {state.review_amenities}/5.
Write it in 3 sentences, and give an overall rating.
"""
    state.review_out = generate_review(prompt)
    state.review_iswritten = True

def on_button_action(state):
    notify(state, 'info', 'Analyzing review...')
    state.rating = generate_rating(state.text)

def on_change(state, var_name, var_value):
    if var_name == "text" and var_value == "Reset":
        state.text = ""
        return


pages = {
    "/": root_md,
    "Home": page1_md,
    "Rating_Tool": page2_md,
    "Review_Writer": page3_md,
}

Gui(pages=pages, css_file="static/style.css").run()
