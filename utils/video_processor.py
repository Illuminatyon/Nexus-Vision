"""
Video Processor Module
This module contains the VideoProcessor class for processing video input and displaying results.
"""

import cv2
import numpy as np
import time


class VideoProcessor:
    """Class for processing video input and displaying results."""

    def __init__(self):
        """Initialize the video processor."""
        # Define colors
        self.color_left = (0, 0, 255)    # Red for left hand
        self.color_right = (0, 255, 0)   # Green for right hand
        self.color_sum = (255, 0, 255)   # Magenta for sum

    def create_info_panel(self, frame):
        """
        Create an information panel for the frame.

        Args:
            frame: BGR image frame

        Returns:
            info_panel: Black background with instructions
        """
        # Get frame dimensions
        h, w, _ = frame.shape

        # Create a black background for instructions
        info_panel = np.zeros((h, w, 3), dtype=np.uint8)

        # Add title with a more futuristic font and color
        cv2.putText(info_panel, "NEXUS VISION", (10, 40), 
                   cv2.FONT_HERSHEY_TRIPLEX, 0.9, (0, 200, 255), 2)

        # Add facial expression section with futuristic styling
        cv2.putText(info_panel, "FACIAL EXPRESSIONS:", (10, 90), 
                   cv2.FONT_HERSHEY_TRIPLEX, 0.6, (0, 180, 255), 1)
        cv2.putText(info_panel, "- Smile: Show a happy expression", (20, 120), 
                   cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 255, 200), 1)  # Teal
        cv2.putText(info_panel, "- Surprise: Raise eyebrows, open mouth", (20, 150), 
                   cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 200, 255), 1)  # Blue-Cyan
        cv2.putText(info_panel, "- Neutral: Relaxed face", (20, 180), 
                   cv2.FONT_HERSHEY_COMPLEX, 0.5, (180, 180, 255), 1)  # Light Purple

        # Add a debug section to the info panel with futuristic styling
        cv2.putText(info_panel, "SYSTEM INFO:", (10, h - 240), 
                   cv2.FONT_HERSHEY_TRIPLEX, 0.6, (0, 180, 255), 1)
        cv2.putText(info_panel, "Red = Left Hand", (20, h - 210), 
                   cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 100, 255), 1)  # Blue-Red
        cv2.putText(info_panel, "Green = Right Hand", (20, h - 180), 
                   cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 255, 200), 1)  # Teal

        # Add hand orientation guide with futuristic styling
        cv2.putText(info_panel, "HAND ORIENTATION GUIDE:", (10, h - 150), 
                   cv2.FONT_HERSHEY_TRIPLEX, 0.6, (0, 180, 255), 1)
        cv2.putText(info_panel, "- Keep palm facing camera", (20, h - 120), 
                   cv2.FONT_HERSHEY_COMPLEX, 0.5, (100, 200, 255), 1)  # Light Blue
        cv2.putText(info_panel, "- For left hand: thumb should be on the left side", (20, h - 90), 
                   cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 100, 255), 1)  # Blue-Red
        cv2.putText(info_panel, "- For right hand: thumb should be on the right side", (20, h - 60), 
                   cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 255, 200), 1)  # Teal

        # Add quit instruction with futuristic styling
        cv2.putText(info_panel, "Press 'q' to exit", (10, h - 20), 
                   cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 200, 255), 1)  # Blue-Cyan

        return info_panel

    def display_fps(self, frame, prev_time):
        """
        Display FPS on the frame.

        Args:
            frame: BGR image frame
            prev_time: Previous time for FPS calculation

        Returns:
            frame: Frame with FPS displayed
            current_time: Current time for next FPS calculation
        """
        # Calculate and display FPS
        current_time = time.time()
        fps = 1 / (current_time - prev_time) if (current_time - prev_time) > 0 else 0
        prev_time = current_time

        # Display FPS with futuristic styling
        cv2.putText(frame, f"FPS: {int(fps)}", (10, 30), 
                   cv2.FONT_HERSHEY_TRIPLEX, 0.7, (0, 200, 255), 1)

        return frame, prev_time

    def display_total_fingers(self, frame, total_fingers):
        """
        Display the total number of extended fingers on the frame.

        Args:
            frame: BGR image frame
            total_fingers: Total number of extended fingers

        Returns:
            frame: Frame with total fingers displayed
        """
        # Display the sum prominently with futuristic styling
        if total_fingers > 0:
            # Create a semi-transparent background for the text
            text_size = cv2.getTextSize(f'Total fingers: {total_fingers}', cv2.FONT_HERSHEY_TRIPLEX, 1.2, 2)[0]
            cv2.rectangle(frame, (5, 70), (text_size[0] + 15, 105), (0, 0, 40), -1)

            # Display text with futuristic font and color
            cv2.putText(frame, f'Total fingers: {total_fingers}', (10, 100), 
                       cv2.FONT_HERSHEY_TRIPLEX, 1.2, (0, 200, 255), 2)

        return frame
