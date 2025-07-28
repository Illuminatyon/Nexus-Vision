"""
Reconnaissance Vidéo Python v1
Hand gesture recognition and finger counting application using OpenCV and MediaPipe.

This program uses your webcam to detect hands and count extended fingers.
It can detect both hands simultaneously and calculate the total sum of extended fingers.
It can also detect facial expressions like smile and surprise.
"""

import sys
from application import Application

if __name__ == '__main__':
    # Check for debug mode command-line argument
    debug_mode = '--debug' in sys.argv

    if debug_mode:
        print("Debug mode enabled. Facial expression detection visualization will be shown.")
        print("This mode helps troubleshoot issues with facial expression recognition.")

    app = Application(debug_mode=debug_mode)
    app.run()
    print("Program terminated.")
