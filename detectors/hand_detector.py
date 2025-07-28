"""
Hand Detector Module
This module contains the HandDetector class for detecting and analyzing hands.
"""

try:
    import cv2
except ImportError:
    print("Error: OpenCV (cv2) library not found.")
    print("Please install it using: pip install opencv-python")
    exit(1)

try:
    import mediapipe as mp
except ImportError:
    print("Error: MediaPipe library not found.")
    print("Please install it using: pip install mediapipe")
    exit(1)


class HandDetector:
    """Class for detecting and analyzing hands using MediaPipe."""

    def __init__(self, static_image_mode=False, max_num_hands=2, 
                 min_detection_confidence=0.5, min_tracking_confidence=0.5):
        """
        Initialize the hand detector.

        Args:
            static_image_mode: Whether to treat input as static images
            max_num_hands: Maximum number of hands to detect
            min_detection_confidence: Minimum confidence for detection
            min_tracking_confidence: Minimum confidence for tracking
        """
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=static_image_mode,
            max_num_hands=max_num_hands,
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence
        )
        self.mp_drawing = mp.solutions.drawing_utils

    def find_hands(self, frame):
        """
        Detect hands in the frame.

        Args:
            frame: BGR image frame from camera

        Returns:
            results: MediaPipe hand detection results
        """
        # Convert BGR to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Process the frame with MediaPipe
        results = self.hands.process(rgb_frame)

        return results

    def draw_landmarks(self, frame, hand_landmarks, is_left):
        """
        Draw hand landmarks on the frame.

        Args:
            frame: BGR image frame
            hand_landmarks: MediaPipe hand landmarks
            is_left: Whether this is a left hand

        Returns:
            frame: Frame with landmarks drawn
        """
        # Use different colors for left and right hands
        landmark_color = (0, 0, 255) if is_left else (0, 255, 0)  # Red for left, Green for right
        connection_color = (0, 0, 180) if is_left else (0, 180, 0)

        # Draw hand landmarks
        self.mp_drawing.draw_landmarks(
            frame, 
            hand_landmarks, 
            self.mp_hands.HAND_CONNECTIONS,
            self.mp_drawing.DrawingSpec(color=landmark_color, thickness=2, circle_radius=4),
            self.mp_drawing.DrawingSpec(color=connection_color, thickness=2, circle_radius=2)
        )

        return frame

    def is_left_hand(self, hand_landmarks):
        """
        Determine if the hand is a left hand using multiple methods for robustness,
        with additional checks to prevent misidentification of flipped hands.

        Args:
            hand_landmarks: MediaPipe hand landmarks

        Returns:
            bool: True if left hand, False if right hand
        """
        # Get key landmarks
        wrist = hand_landmarks.landmark[0]       # Wrist
        thumb_mcp = hand_landmarks.landmark[1]   # Thumb metacarpal
        thumb_tip = hand_landmarks.landmark[4]   # Thumb tip
        index_mcp = hand_landmarks.landmark[5]   # Index finger metacarpal
        middle_mcp = hand_landmarks.landmark[9]  # Middle finger metacarpal
        pinky_mcp = hand_landmarks.landmark[17]  # Pinky metacarpal

        # Method 1: Use the relative positions of pinky and thumb
        pinky_thumb_method = pinky_mcp.x < thumb_mcp.x

        # Method 2: Use the cross product of vectors to determine hand orientation
        # Vector from wrist to middle finger base
        vec_wrist_to_middle = [middle_mcp.x - wrist.x, middle_mcp.y - wrist.y]
        # Vector from wrist to thumb base
        vec_wrist_to_thumb = [thumb_mcp.x - wrist.x, thumb_mcp.y - wrist.y]
        # Cross product (in 2D, just need the z component)
        cross_product_z = vec_wrist_to_middle[0] * vec_wrist_to_thumb[1] - vec_wrist_to_middle[1] * vec_wrist_to_thumb[0]
        cross_product_method = cross_product_z > 0

        # Method 3: Thumb position relative to wrist
        thumb_method = thumb_tip.x < wrist.x

        # Method 4: Check palm orientation using depth (z-coordinate)
        # In a properly oriented hand, the MCP joints should have similar z-values
        # If the hand is flipped, there will be significant z-differences
        z_values = [thumb_mcp.z, index_mcp.z, middle_mcp.z, pinky_mcp.z]
        z_range = max(z_values) - min(z_values)
        palm_properly_oriented = z_range < 0.1  # Threshold for proper orientation

        # Method 5: Check finger order consistency
        # In a properly oriented hand, x-coordinates should be in order for MCP joints
        # For left hand: pinky < ring < middle < index < thumb
        # For right hand: thumb < index < middle < ring < pinky
        finger_mcps = [hand_landmarks.landmark[5].x, hand_landmarks.landmark[9].x, 
                      hand_landmarks.landmark[13].x, hand_landmarks.landmark[17].x]

        # Check if the x-coordinates are monotonically increasing or decreasing
        is_increasing = all(finger_mcps[i] <= finger_mcps[i+1] for i in range(len(finger_mcps)-1))
        is_decreasing = all(finger_mcps[i] >= finger_mcps[i+1] for i in range(len(finger_mcps)-1))
        finger_order_consistent = is_increasing or is_decreasing

        # Combine basic methods with a voting system
        basic_votes = [pinky_thumb_method, cross_product_method, thumb_method]
        basic_result = sum(basic_votes) >= 2

        # Only trust the basic result if the palm is properly oriented and finger order is consistent
        if not palm_properly_oriented or not finger_order_consistent:
            # If the hand appears to be in an unusual orientation, don't change its classification
            # This prevents a flipped right hand from being detected as a left hand
            return False

        return basic_result