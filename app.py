import streamlit as st
import requests as rq

# Function to fetch a random word
# Converts to uppercase for simpler comparisons
def get_word():
    response = rq.get("https://random-word-api.vercel.app/api?words=1")
    return response.json()[0].upper() if response.status_code == 200 else "HELLO"

# —– Initialize session state —–
if "word" not in st.session_state:
    st.session_state.word = get_word()
    st.session_state.tries = 0                  # Number of wrong attempts
    st.session_state.correct = {}               # Correct letters {index: letter}
    st.session_state.guessed = set()            # Letters already tried

# —– Function to process each guess —–
def guess_letter():
    # Get the input letter and convert to uppercase
    letter = st.session_state.letter_guess.upper()
    # Ignore empty input or repeated guesses
    if not letter or letter in st.session_state.guessed:
        return
    st.session_state.guessed.add(letter)

    # If the letter is in the word, reveal all matching positions
    if letter in st.session_state.word:
        for idx, char in enumerate(st.session_state.word):
            if char == letter:
                st.session_state.correct[idx] = char
    else:
        # Wrong guess: increment the try counter
        st.session_state.tries += 1

    # Clear the input field for the next guess
    st.session_state.letter_guess = ""

# —– App title —–
st.title("Hangman Game")

# —– Display hangman image based on number of wrong attempts —–
st.image(f"./images/hangman_{st.session_state.tries}.png", width=400)

# —– Form for guessing a letter —–
with st.form("guess_form", clear_on_submit=True):
    st.text_input("Enter a letter:", max_chars=1, key="letter_guess")
    st.form_submit_button("Submit Guess", on_click=guess_letter)

# —– Draw blanks and reveal correctly guessed letters —–
cols = st.columns(len(st.session_state.word))
for idx, char in enumerate(st.session_state.word):
    with cols[idx]:
        if idx in st.session_state.correct:
            st.markdown(f"**{char}**")
        else:
            st.markdown("▢")

# —– End-of-game conditions —–
if st.session_state.tries >= 6:
    st.error(f"Game Over! The word was **{st.session_state.word}**")
elif len(st.session_state.correct) == len(st.session_state.word):
    st.success("🎉 Congratulations, you won!")
