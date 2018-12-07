import sys
from text2speech import text2speech



if len(sys.argv) != 2:
    tts = text2speech(firs_run=False)
else:
    tts = text2speech(firs_run=sys.argv[1])

tts.run()