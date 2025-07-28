"""
Finger Counter Module
This module contains the FingerCounter class for counting extended fingers on detected hands.
"""

import math
import cv2


class FingerCounter:
    """Class for counting extended fingers on detected hands."""

    def __init__(self):
        """Initialize the finger counter."""
        # Define landmark indices
        self.finger_tips = [4, 8, 12, 16, 20]  # Thumb, Index, Middle, Ring, Pinky
        self.finger_bases = [2, 5, 9, 13, 17]  # Base joints of each finger
        self.finger_mids = [3, 6, 10, 14, 18]  # Middle joints of each finger
        self.finger_names = ["Thumb", "Index", "Middle", "Ring", "Pinky"]

    def count_fingers(self, hand_landmarks, is_left_hand=False):
        """
        Count extended fingers on a hand.

        Args:
            hand_landmarks: MediaPipe hand landmarks
            is_left_hand: Whether this is the left hand

        Returns:
            list: List of indices of extended fingers
        """
        # Get hand landmarks
        landmarks = hand_landmarks.landmark

        # Check if fingers are extended
        extended_fingers = []

        # Improved thumb detection with adaptive thresholds
        # For thumb detection, we'll use relative distances instead of fixed thresholds

        # Get thumb landmarks
        thumb_tip = landmarks[self.finger_tips[0]]
        thumb_mid = landmarks[self.finger_mids[0]]
        thumb_base = landmarks[self.finger_bases[0]]

        # Calculate the distance between thumb base and middle joint
        # This will be used to create an adaptive threshold based on hand size
        base_to_mid_distance = self.calculate_distance(thumb_base, thumb_mid)

        # Adaptive threshold - scales with hand size
        thumb_extension_threshold = base_to_mid_distance * 0.6

        # Left hand thumb detection
        if is_left_hand:
            # For left hand, thumb is counted when NOT extended (inverted behavior)
            # Use the x-distance between tip and mid, normalized by the base-to-mid distance
            x_distance = thumb_mid.x - thumb_tip.x

            # Check if the thumb is NOT extended enough (inverted condition)
            if not (x_distance > thumb_extension_threshold and 
                   thumb_tip.x < thumb_base.x):
                extended_fingers.append(0)  # Thumb is counted when NOT extended
        else:
            # For right hand, thumb is counted when NOT extended (inverted behavior)
            # Use the x-distance between tip and mid, normalized by the base-to-mid distance
            x_distance = thumb_tip.x - thumb_mid.x

            # Check if the thumb is NOT extended enough (inverted condition)
            if not (x_distance > thumb_extension_threshold and 
                   thumb_tip.x > thumb_base.x):
                extended_fingers.append(0)  # Thumb is counted when NOT extended

        # Check other fingers with a more lenient threshold (same for both hands)
        for i in range(1, 5):
            # Get finger landmarks
            finger_tip = landmarks[self.finger_tips[i]]
            finger_mid = landmarks[self.finger_mids[i]]
            finger_base = landmarks[self.finger_bases[i]]

            # Calculate the distance between finger base and middle joint
            # This will be used to create an adaptive threshold based on hand size
            base_to_mid_distance = self.calculate_distance(finger_base, finger_mid)

            # Adaptive threshold - scales with hand size
            finger_extension_threshold = base_to_mid_distance * 0.3

            # Use a margin for more reliable detection
            # Check if the finger tip is above the middle joint
            if finger_tip.y < finger_mid.y - finger_extension_threshold:
                extended_fingers.append(i)  # Finger is extended

            # Additional check: if finger tip is significantly higher than base, consider it extended
            # This helps with cases where the finger is extended but not perfectly straight
            if finger_tip.y < finger_base.y - base_to_mid_distance * 0.7:
                if i not in extended_fingers:
                    extended_fingers.append(i)

        return extended_fingers

    def calculate_distance(self, point1, point2):
        """
        Calculate Euclidean distance between two points in 2D space.

        Args:
            point1: First point with x and y coordinates
            point2: Second point with x and y coordinates

        Returns:
            float: Euclidean distance between the two points
        """
        return math.sqrt((point1.x - point2.x)**2 + (point1.y - point2.y)**2)

    def draw_finger_status(self, frame, hand_landmarks, extended_fingers, is_left):
        """
        Draw finger status on the frame.

        Args:
            frame: BGR image frame
            hand_landmarks: MediaPipe hand landmarks
            extended_fingers: List of extended finger indices
            is_left: Whether this is a left hand

        Returns:
            frame: Frame with finger status drawn
        """
        # Get frame dimensions
        h, w, _ = frame.shape

        # Colors for different hands
        color_left = (0, 0, 255)    # Red for left hand
        color_right = (0, 255, 0)   # Green for right hand

        # Display hand info
        landmark_color = color_left if is_left else color_right
        finger_count = len(extended_fingers)
        hand_label = "L" if is_left else "R"

        # Display finger count with futuristic styling
        text = f"{hand_label}: {finger_count} fingers"
        text_pos = (int(hand_landmarks.landmark[0].x * w), int(hand_landmarks.landmark[0].y * h - 20))

        # Create a semi-transparent background for better visibility
        text_size = cv2.getTextSize(text, cv2.FONT_HERSHEY_TRIPLEX, 0.7, 1)[0]
        cv2.rectangle(frame, 
                     (text_pos[0] - 5, text_pos[1] - text_size[1] - 5),
                     (text_pos[0] + text_size[0] + 5, text_pos[1] + 5),
                     (0, 0, 40), -1)

        # Use modern font and futuristic color
        futuristic_color = (0, 200, 255) if is_left else (0, 255, 200)  # Blue-Cyan for left, Teal for right
        cv2.putText(frame, text, text_pos, cv2.FONT_HERSHEY_TRIPLEX, 0.7, futuristic_color, 1)

        # Debug for thumb if extended (with inverted behavior, thumb is in extended_fingers when NOT physically extended)
        if 0 in extended_fingers:  # If thumb is in the list (meaning it's NOT physically extended with inverted behavior)
            # Get thumb landmarks
            thumb_tip = hand_landmarks.landmark[self.finger_tips[0]]

            # Draw thumb landmarks in orange to indicate they're being analyzed
            for landmark_idx in [3, 4]:  # Thumb IP and tip landmarks
                lm = hand_landmarks.landmark[landmark_idx]
                lm_x = int(lm.x * w)
                lm_y = int(lm.y * h)
                cv2.circle(frame, (lm_x, lm_y), 8, (0, 165, 255), -1)  # Orange circle

            # Add thumb debug text with futuristic styling
            thumb_tip_x = int(thumb_tip.x * w)
            thumb_tip_y = int(thumb_tip.y * h)

            # Create a semi-transparent background
            text = "Thumb tucked in (counted)"
            text_size = cv2.getTextSize(text, cv2.FONT_HERSHEY_COMPLEX, 0.5, 1)[0]
            cv2.rectangle(frame, 
                         (thumb_tip_x - 65, thumb_tip_y - 30),
                         (thumb_tip_x - 65 + text_size[0] + 10, thumb_tip_y - 10),
                         (0, 0, 40), -1)

            # Use futuristic color
            debug_color = (0, 200, 255) if is_left else (0, 255, 200)  # Blue-Cyan for left, Teal for right
            cv2.putText(frame, text, 
                       (thumb_tip_x - 60, thumb_tip_y - 15), 
                       cv2.FONT_HERSHEY_COMPLEX, 0.5, debug_color, 1)

        # Highlight extended fingers with colored circles
        for finger_idx in extended_fingers:
            # Get the fingertip coordinates
            tip_landmark = hand_landmarks.landmark[self.finger_tips[finger_idx]]
            tip_x = int(tip_landmark.x * w)
            tip_y = int(tip_landmark.y * h)

            # Use different futuristic colors for fingers
            if finger_idx == 0:  # Thumb on either hand
                if is_left:
                    circle_color = (0, 200, 255)  # Blue-Cyan for left hand thumb
                else:
                    circle_color = (0, 255, 200)  # Teal for right hand thumb
            else:
                # Create a gradient of colors for other fingers
                if is_left:
                    # Blue to purple gradient for left hand
                    blue_intensity = max(100, 255 - finger_idx * 40)
                    circle_color = (180, 100, blue_intensity)  # Purple-Blue gradient
                else:
                    # Cyan to teal gradient for right hand
                    green_intensity = max(100, 255 - finger_idx * 40)
                    circle_color = (0, green_intensity, 255)  # Cyan-Blue gradient

            # Draw a circle on the fingertip
            cv2.circle(frame, (tip_x, tip_y), 12, circle_color, -1)  # Filled circle
            cv2.circle(frame, (tip_x, tip_y), 12, (0, 0, 0), 2)      # Black border

            # Add finger name with modern font
            cv2.putText(frame, self.finger_names[finger_idx][0], (tip_x - 4, tip_y + 4), 
                       cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0), 1)

        return frame
