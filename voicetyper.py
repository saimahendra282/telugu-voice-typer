import speech_recognition as sr
import pyautogui
import pyperclip
import time


def load_bad_words(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:  # Specify the encoding as 'utf-8'
        bad_words = [word.strip() for word in file.readlines()]
    return bad_words


def contains_bad_word(text, badwords):
    for word in bad_words:
        if word in text:
            return True
    return False


def voice_typing(badwords):
    recognizer = sr.Recognizer()

    while True:
        with sr.Microphone() as source:
            print("Listening... Speak something.")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)

        try:
            text = recognizer.recognize_google(audio, language='te-IN')
            print("Recognized:", text)

            # Check if recognized text contains a bad word
            if contains_bad_word(text, bad_words):
                print("Encountered a bad word:", text)
            else:
                # Simulate typing at the current cursor position
                current_pos = pyautogui.position()
                pyautogui.click(current_pos.x, current_pos.y)

                # Add a delay before typing to ensure the text box is ready
                time.sleep(1)

                pyperclip.copy(text)  # Copy recognized text to clipboard
                pyautogui.hotkey('space')  # Type using space
                pyautogui.hotkey('ctrl', 'v')  # Paste text using keyboard shortcut

        except sr.UnknownValueError:
            print("Sorry, could not understand audio.")
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))
        except Exception as e:
            print("An error occurred:", e)


if __name__ == "__main__":
    bad_words_file = "badwords.txt"  # Specify the path to your bad words file
    bad_words = load_bad_words(bad_words_file)
    voice_typing(bad_words)
