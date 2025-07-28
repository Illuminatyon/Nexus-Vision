"""
Application Module
This module contains the Application class for coordinating hand gesture and facial expression recognition.
"""

import cv2
import numpy as np
import sys

from detectors.face_detector import FaceExpressionDetector
from detectors.hand_detector import HandDetector
from detectors.finger_counter import FingerCounter
from utils.video_processor import VideoProcessor


class Application:
    """Main application class for hand gesture and facial expression recognition."""

    def __init__(self, debug_mode=False):
        """
        Initialize the application.

        Args:
            debug_mode: Whether to show debug visualizations for facial expressions
        """
        self.hand_detector = HandDetector()
        self.finger_counter = FingerCounter()
        self.face_detector = FaceExpressionDetector(debug_mode=debug_mode)
        self.video_processor = VideoProcessor()
        self.debug_mode = debug_mode

        # Initialize webcam
        self.cap = cv2.VideoCapture(0)

        # Check if the webcam is opened correctly
        if not self.cap.isOpened():
            print("Error: Could not open webcam.")
            exit(1)

        self.prev_time = 0

    def print_instructions(self):
        """Print instructions for hand gestures and facial expressions to the console."""
        print("\n=== NEXUS VISION ===")
        print("Advanced hand gesture recognition and facial expression analysis system.")
        print("")
        print("HAND GESTURE RECOGNITION:")
        print("Show your hands to the camera to count extended fingers:")
        print("RIGHT HAND:")
        print("Show any number of fingers (0-5)")
        print("")
        print("LEFT HAND:")
        print("Show any number of fingers (0-5)")
        print("")
        print("ADDITION FEATURE:")
        print("The program will calculate and display the total sum")
        print("of all fingers extended on both hands.")
        print("")
        print("FACIAL EXPRESSION RECOGNITION:")
        print("The program will detect your facial expressions:")
        print("- Smile: Detected when you smile")
        print("- Surprise: Detected when you raise your eyebrows and open your mouth")
        print("- Neutral: Default expression when no specific expression is detected")
        print("")
        if self.debug_mode:
            print("DEBUG MODE IS ENABLED:")
            print("- Key facial landmarks are highlighted")
            print("- Mouth corners and eye measurements are visualized")
            print("- This helps troubleshoot facial expression recognition issues")
            print("")
        print("TROUBLESHOOTING:")
        print("If facial expressions aren't being detected correctly:")
        print("- Ensure good lighting on your face")
        print("- Position your face clearly in the center of the frame")
        print("- Make more pronounced expressions")
        print("- Try running with --debug flag for visualization: python main.py --debug")
        print("")
        print("Press 'q' to quit the program")
        print("=======================================\n")

    def run(self):
        """Run the application."""
        # Print instructions
        self.print_instructions()

        while True:
            # Read frame from webcam
            success, frame = self.cap.read()
            if not success:
                print("Error: Failed to capture image")
                break

            # Flip the frame horizontally for a more intuitive mirror view
            frame = cv2.flip(frame, 1)

            # Process the frame with MediaPipe Hands
            hand_results = self.hand_detector.find_hands(frame)

            # Process the frame with MediaPipe Face Mesh
            face_results = self.face_detector.find_faces(frame)

            # Create info panel
            info_panel = self.video_processor.create_info_panel(frame)

            # Variables to store finger counts for addition
            right_hand_fingers = 0
            left_hand_fingers = 0

            # Process facial expressions
            if face_results.multi_face_landmarks:
                for face_landmarks in face_results.multi_face_landmarks:
                    # Draw face landmarks
                    frame = self.face_detector.draw_landmarks(frame, face_landmarks)

                    # Detect facial expression
                    expression, confidence = self.face_detector.detect_expression(face_landmarks, frame.shape)

                    # Draw expression information
                    frame = self.face_detector.draw_expression(frame, expression, confidence, face_landmarks)

            # Draw hand landmarks and count fingers
            if hand_results.multi_hand_landmarks:
                # Process all detected hands
                for hand_landmarks in hand_results.multi_hand_landmarks:
                    # Determine if this is a left hand
                    is_left = self.hand_detector.is_left_hand(hand_landmarks)

                    # Draw hand landmarks
                    frame = self.hand_detector.draw_landmarks(frame, hand_landmarks, is_left)

                    # Count extended fingers
                    extended_fingers = self.finger_counter.count_fingers(hand_landmarks, is_left_hand=is_left)
                    finger_count = len(extended_fingers)

                    # Update finger counts
                    if is_left:
                        left_hand_fingers = finger_count
                    else:
                        right_hand_fingers = finger_count

                    # Draw finger status
                    frame = self.finger_counter.draw_finger_status(frame, hand_landmarks, extended_fingers, is_left)

                # Calculate the sum of fingers from both hands
                total_fingers = right_hand_fingers + left_hand_fingers

                # Display the total
                frame = self.video_processor.display_total_fingers(frame, total_fingers)

            # Display FPS
            frame, self.prev_time = self.video_processor.display_fps(frame, self.prev_time)

            # Display the frame and info panel side by side
            combined_frame = np.hstack((frame, info_panel))

            # Show the combined frame
            cv2.imshow('NEXUS VISION', combined_frame)

            # Check for key press
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break

        # Release resources
        self.cap.release()
        cv2.destroyAllWindows()
