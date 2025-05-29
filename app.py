import streamlit as st
import requests as rq


def get_word():
    url = "https://random-word-api.herokuapp.com/word"
    resp = rq.get(url)

    if resp.status_code == 200:
        return resp.json()[0]
    
    return "Hello"


def gen_cols(word, letter = ""):
    cols = st.columns(len(word))

    if "correct" not in st.session_state:
        st.session_state['correct'] = {}
        correct = {}
    
    else:
        correct = st.session_state['correct']


    for i, col in enumerate(cols):
        with col:
            if correct.get(str(i)):
                st.text_input(label = str(i), value = correct.get(str(i)), disabled = True)

            elif word[i] == letter:
                st.text_input(label = str(i), value = letter, disabled = True)
                correct[str(i)] = letter
                st.session_state["fails"] = False
            else:
                st.text_input(label = str(i), disabled = True)
    
    
    st.session_state["trys"] += 1


def get_answer(word):
    cols = st.columns(len(word))

    for i, letter in enumerate(word):
        with cols[i]:
            st.text_input(label = str(i), value = letter, disabled = True)


def main(word):
    st.write(word)
    if st.session_state["trys"] < 6:
        letter = st.text_input(label = "choise",value = "", max_chars = 1)

        # st.image(f"./images/hangman_{st.session_state["trys"]}.png", width = 400)

        gen_cols(word, letter)

    else:
        get_answer(word)



if __name__ == '__main__':
    word = get_word()
    if "word" not in st.session_state:
        st.session_state["word"] = word
        st.session_state["trys"] = 0
    else:
        word = st.session_state["word"]

    main(word)


