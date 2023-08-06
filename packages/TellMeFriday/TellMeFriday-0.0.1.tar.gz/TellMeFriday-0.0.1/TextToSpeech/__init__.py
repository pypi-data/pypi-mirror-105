from gtts import gTTS
import os
def voice_repeator():
    mytext=input("Enter the text:")
    language='en'
    myobj = gTTS(text=mytext, lang=language, slow=False)
    myobj.save("text.mp3")
    return(os.system("mpg321 text.mp3"))
