"""
Face Expression Detector Module
This module contains the FaceExpressionDetector class for detecting and analyzing facial expressions.
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

try:
    import numpy as np
except ImportError:
    print("Error: NumPy library not found.")
    print("Please install it using: pip install numpy")
    exit(1)

import math


class FaceExpressionDetector:
    """Class for detecting and analyzing facial expressions using MediaPipe."""

    def __init__(self, static_image_mode=False, max_num_faces=1,
                 min_detection_confidence=0.5, min_tracking_confidence=0.5, debug_mode=False):
        """
        Initialize the face expression detector.

        Args:
            static_image_mode: Whether to treat input as static images
            max_num_faces: Maximum number of faces to detect
            min_detection_confidence: Minimum confidence for detection
            min_tracking_confidence: Minimum confidence for tracking
            debug_mode: Whether to show debug visualizations
        """
        self.debug_mode = debug_mode
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            static_image_mode=static_image_mode,
            max_num_faces=max_num_faces,
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence
        )
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles

        # Define facial expression landmarks
        # These are indices of landmarks that are useful for expression detection
        # Based on MediaPipe Face Mesh topology
        self.landmarks = {
            # Eyes
            'left_eye': [33, 7, 163, 144, 145, 153, 154, 155, 133, 173, 157, 158, 159, 160, 161, 246],
            'right_eye': [362, 382, 381, 380, 374, 373, 390, 249, 263, 466, 388, 387, 386, 385, 384, 398],
            # Eyebrows
            'left_eyebrow': [70, 63, 105, 66, 107, 55, 65, 52, 53, 46],
            'right_eyebrow': [300, 293, 334, 296, 336, 285, 295, 282, 283, 276],
            # Mouth
            'mouth_outline': [61, 146, 91, 181, 84, 17, 314, 405, 321, 375, 291, 409, 270, 269, 267, 0, 37, 39, 40, 185],
            'mouth_inner': [78, 95, 88, 178, 87, 14, 317, 402, 318, 324, 308, 415, 310, 311, 312, 13, 82, 81, 80, 191]
        }

        # Expression thresholds and parameters
        self.expression_params = {
            'smile_threshold': 2.0,  # Threshold for smile detection (mouth width to height ratio)
            'surprise_threshold': 0.12,  # Threshold for surprise detection (eye height to face height ratio)
            'mouth_openness_threshold': 0.2,  # Threshold for mouth openness in surprise detection
            'neutral_range': 0.1,  # Range for neutral expression
            'min_confidence': 0.4,  # Minimum confidence to detect an expression
        }

    def find_faces(self, frame):
        """
        Detect faces in the frame.

        Args:
            frame: BGR image frame from camera

        Returns:
            results: MediaPipe face mesh detection results
        """
        # Convert BGR to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Process the frame with MediaPipe
        results = self.face_mesh.process(rgb_frame)

        return results

    def draw_landmarks(self, frame, face_landmarks):
        """
        Draw face landmarks on the frame.

        Args:
            frame: BGR image frame
            face_landmarks: MediaPipe face landmarks

        Returns:
            frame: Frame with landmarks drawn
        """
        h, w = frame.shape[:2]
        landmarks = face_landmarks.landmark

        if not self.debug_mode:
            # Standard mode: Draw the full face mesh
            self.mp_drawing.draw_landmarks(
                image=frame,
                landmark_list=face_landmarks,
                connections=self.mp_face_mesh.FACEMESH_TESSELATION,
                landmark_drawing_spec=None,
                connection_drawing_spec=self.mp_drawing_styles.get_default_face_mesh_tesselation_style()
            )

            # Draw the face contours
            self.mp_drawing.draw_landmarks(
                image=frame,
                landmark_list=face_landmarks,
                connections=self.mp_face_mesh.FACEMESH_CONTOURS,
                landmark_drawing_spec=None,
                connection_drawing_spec=self.mp_drawing_styles.get_default_face_mesh_contours_style()
            )
        else:
            # Debug mode: Draw only the key landmarks used for expression detection
            # Convert normalized coordinates to pixel coordinates
            points = {}
            for region, indices in self.landmarks.items():
                points[region] = [(int(landmarks[idx].x * w), int(landmarks[idx].y * h)) for idx in indices]

            # Draw mouth landmarks
            mouth_left = points['mouth_outline'][0]
            mouth_right = points['mouth_outline'][10]
            mouth_top = points['mouth_outline'][3]
            mouth_bottom = points['mouth_outline'][13]

            # Calculate mouth dimensions
            mouth_width = abs(mouth_right[0] - mouth_left[0])
            mouth_height = abs(mouth_bottom[1] - mouth_top[1])

            # Calculate face dimensions for more robust normalization
            # Use the distance between eyes as a horizontal reference
            inter_eye_distance = abs(points['left_eye'][0][0] - points['right_eye'][8][0])

            # Use a combination of vertical and horizontal face dimensions for normalization
            # This makes the detection more invariant to head tilt
            face_height = abs(points['left_eyebrow'][0][1] - points['mouth_outline'][13][1])
            face_diagonal = math.sqrt(face_height**2 + inter_eye_distance**2)

            # Calculate mouth openness metrics
            mouth_openness_ratio = mouth_height / mouth_width if mouth_width > 0 else 0
            normalized_mouth_openness = mouth_height / (face_diagonal * 0.3) if face_diagonal > 0 else 0

            # Determine if mouth is open enough for surprise
            is_mouth_open = normalized_mouth_openness > self.expression_params['mouth_openness_threshold']

            # Draw mouth rectangle with color based on openness
            mouth_rect_color = (0, 165, 255) if is_mouth_open else (0, 255, 0)  # Orange if open, green if not

            # Draw mouth rectangle (hidden as per requirements)
            # cv2.line(frame, mouth_left, mouth_right, mouth_rect_color, 2)
            # cv2.line(frame, mouth_top, mouth_bottom, mouth_rect_color, 2)
            cv2.circle(frame, mouth_left, 5, (0, 0, 255), -1)
            cv2.circle(frame, mouth_right, 5, (0, 0, 255), -1)
            cv2.circle(frame, mouth_top, 5, (0, 0, 255), -1)
            cv2.circle(frame, mouth_bottom, 5, (0, 0, 255), -1)

            # Add mouth openness measurements
            cv2.putText(frame, f"Mouth open: {is_mouth_open}", (10, 280), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, mouth_rect_color, 1)
            cv2.putText(frame, f"Openness: {normalized_mouth_openness:.3f}", (10, 310), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, mouth_rect_color, 1)

            # Calculate lip midpoint
            lip_midpoint_y = (mouth_top[1] + mouth_bottom[1]) // 2
            lip_midpoint_x = (mouth_left[0] + mouth_right[0]) // 2
            lip_midpoint = (lip_midpoint_x, lip_midpoint_y)

            # Draw lip midpoint
            cv2.circle(frame, lip_midpoint, 5, (255, 255, 0), -1)

            # Draw lines from midpoint to corners to show corner elevation (hidden as per requirements)
            # cv2.line(frame, lip_midpoint, mouth_left, (255, 0, 255), 2)
            # cv2.line(frame, lip_midpoint, mouth_right, (255, 0, 255), 2)

            # Draw eye landmarks
            left_eye_top = points['left_eye'][3]
            left_eye_bottom = points['left_eye'][5]
            right_eye_top = points['right_eye'][3]
            right_eye_bottom = points['right_eye'][5]

            # Calculate eye heights
            left_eye_height = abs(left_eye_bottom[1] - left_eye_top[1])
            right_eye_height = abs(right_eye_bottom[1] - right_eye_top[1])
            avg_eye_height = (left_eye_height + right_eye_height) / 2

            # Normalize eye height using face diagonal
            normalized_eye_height = avg_eye_height / (face_diagonal * 0.5) if face_diagonal > 0 else 0

            # Determine if eyes are open enough for surprise
            eyes_open_enough = normalized_eye_height > self.expression_params['surprise_threshold'] * 0.8

            # Set color based on eye openness
            eye_line_color = (0, 165, 255) if eyes_open_enough else (0, 255, 255)  # Orange if open enough, cyan if not

            # Draw eye height lines with appropriate color
            cv2.line(frame, left_eye_top, left_eye_bottom, eye_line_color, 2)
            cv2.line(frame, right_eye_top, right_eye_bottom, eye_line_color, 2)
            cv2.circle(frame, left_eye_top, 3, (0, 0, 255), -1)
            cv2.circle(frame, left_eye_bottom, 3, (0, 0, 255), -1)
            cv2.circle(frame, right_eye_top, 3, (0, 0, 255), -1)
            cv2.circle(frame, right_eye_bottom, 3, (0, 0, 255), -1)

            # Calculate average eyebrow and eye positions
            left_eyebrow_y = sum(p[1] for p in points['left_eyebrow']) // len(points['left_eyebrow'])
            right_eyebrow_y = sum(p[1] for p in points['right_eyebrow']) // len(points['right_eyebrow'])
            left_eye_y = sum(p[1] for p in points['left_eye']) // len(points['left_eye'])
            right_eye_y = sum(p[1] for p in points['right_eye']) // len(points['right_eye'])

            # Calculate average x positions
            left_eyebrow_x = sum(p[0] for p in points['left_eyebrow']) // len(points['left_eyebrow'])
            right_eyebrow_x = sum(p[0] for p in points['right_eyebrow']) // len(points['right_eyebrow'])
            left_eye_x = sum(p[0] for p in points['left_eye']) // len(points['left_eye'])
            right_eye_x = sum(p[0] for p in points['right_eye']) // len(points['right_eye'])

            # Calculate eyebrow elevation
            left_eyebrow_elevation = left_eye_y - left_eyebrow_y
            right_eyebrow_elevation = right_eye_y - right_eyebrow_y
            avg_eyebrow_elevation = (left_eyebrow_elevation + right_eyebrow_elevation) / 2

            # Normalize eyebrow elevation using face diagonal
            normalized_eyebrow_elevation = avg_eyebrow_elevation / (face_diagonal * 0.3) if face_diagonal > 0 else 0

            # Determine if eyebrows are raised enough for surprise
            eyebrows_raised_enough = normalized_eyebrow_elevation > 0.05

            # Set color based on eyebrow elevation
            eyebrow_line_color = (0, 165, 255) if eyebrows_raised_enough else (255, 0, 0)  # Orange if raised enough, blue if not

            # Draw eyebrow elevation lines with appropriate color (hidden as per requirements)
            # cv2.line(frame, (left_eyebrow_x, left_eyebrow_y), (left_eye_x, left_eye_y), eyebrow_line_color, 2)
            # cv2.line(frame, (right_eyebrow_x, right_eyebrow_y), (right_eye_x, right_eye_y), eyebrow_line_color, 2)

            # Add eye and eyebrow measurements
            cv2.putText(frame, f"Eyes open: {eyes_open_enough}", (10, 340), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, eye_line_color, 1)
            cv2.putText(frame, f"Eye height: {normalized_eye_height:.3f}", (10, 370), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, eye_line_color, 1)
            cv2.putText(frame, f"Brows raised: {eyebrows_raised_enough}", (10, 400), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, eyebrow_line_color, 1)
            cv2.putText(frame, f"Brow elev: {normalized_eyebrow_elevation:.3f}", (10, 430), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, eyebrow_line_color, 1)

            # Check if all surprise components are present
            all_surprise_components = is_mouth_open and eyes_open_enough and eyebrows_raised_enough

            # Add surprise summary indicator
            summary_color = (0, 165, 255) if all_surprise_components else (0, 0, 255)  # Orange if all components present, red if not
            cv2.putText(frame, "SURPRISE DETECTION:", (10, 460), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            cv2.putText(frame, f"All components: {all_surprise_components}", (10, 490), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, summary_color, 1)

            # Calculate surprise score
            surprise_score = (normalized_eye_height * 0.4) + (normalized_eyebrow_elevation * 0.3) + (normalized_mouth_openness * 0.3)
            if all_surprise_components:
                surprise_score *= 1.5  # Apply the same boost as in detect_expression

            # Check if score exceeds threshold
            exceeds_threshold = surprise_score > self.expression_params['surprise_threshold']
            threshold_color = (0, 165, 255) if exceeds_threshold else (0, 0, 255)  # Orange if exceeds threshold, red if not

            cv2.putText(frame, f"Score: {surprise_score:.3f}", (10, 520), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, threshold_color, 1)
            cv2.putText(frame, f"Threshold: {self.expression_params['surprise_threshold']:.3f}", (10, 550), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            cv2.putText(frame, f"Exceeds threshold: {exceeds_threshold}", (10, 580), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, threshold_color, 1)

            # Add debug mode header
            cv2.putText(frame, "DEBUG MODE", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)

        return frame

    def detect_expression(self, face_landmarks, frame_shape):
        """
        Detect facial expression based on landmark positions.

        Args:
            face_landmarks: MediaPipe face landmarks
            frame_shape: Shape of the frame (height, width)

        Returns:
            expression: Detected facial expression (smile, surprise, neutral)
            confidence: Confidence score for the detected expression
        """
        h, w = frame_shape[:2]
        landmarks = face_landmarks.landmark

        # Extract key points for expression detection
        # Convert normalized coordinates to pixel coordinates
        points = {}
        for region, indices in self.landmarks.items():
            points[region] = [(int(landmarks[idx].x * w), int(landmarks[idx].y * h)) for idx in indices]

        # Calculate smile metrics
        # 1. Mouth width to height ratio
        mouth_left = points['mouth_outline'][0]
        mouth_right = points['mouth_outline'][10]
        mouth_top = points['mouth_outline'][3]
        mouth_bottom = points['mouth_outline'][13]

        mouth_width = abs(mouth_right[0] - mouth_left[0])
        mouth_height = abs(mouth_bottom[1] - mouth_top[1])

        if mouth_height > 0:  # Avoid division by zero
            mouth_ratio = mouth_width / mouth_height
        else:
            mouth_ratio = 0

        # 2. Mouth corner elevation (for smile detection)
        # Get mouth corners and center points
        left_corner = points['mouth_outline'][0]
        right_corner = points['mouth_outline'][10]
        top_lip_center = points['mouth_outline'][3]
        bottom_lip_center = points['mouth_outline'][13]

        # Calculate the vertical midpoint between top and bottom lip
        lip_midpoint_y = (top_lip_center[1] + bottom_lip_center[1]) / 2

        # Calculate how much the corners are elevated relative to the midpoint
        left_corner_elevation = lip_midpoint_y - left_corner[1]
        right_corner_elevation = lip_midpoint_y - right_corner[1]

        # Average corner elevation (positive means corners are above midpoint, indicating smile)
        corner_elevation = (left_corner_elevation + right_corner_elevation) / 2

        # Normalize by face size
        face_width = abs(points['left_eye'][0][0] - points['right_eye'][8][0])
        if face_width > 0:
            normalized_corner_elevation = corner_elevation / face_width
        else:
            normalized_corner_elevation = 0

        # Combined smile score (weighted combination of ratio and corner elevation)
        smile_score = (mouth_ratio * 0.7) + (normalized_corner_elevation * 5.0)

        # Calculate surprise metrics
        # 1. Eye openness
        left_eye_top = points['left_eye'][3]
        left_eye_bottom = points['left_eye'][5]
        right_eye_top = points['right_eye'][3]
        right_eye_bottom = points['right_eye'][5]

        left_eye_height = abs(left_eye_bottom[1] - left_eye_top[1])
        right_eye_height = abs(right_eye_bottom[1] - right_eye_top[1])

        # 2. Eyebrow elevation
        left_eyebrow_y = sum(p[1] for p in points['left_eyebrow']) / len(points['left_eyebrow'])
        right_eyebrow_y = sum(p[1] for p in points['right_eyebrow']) / len(points['right_eyebrow'])

        left_eye_y = sum(p[1] for p in points['left_eye']) / len(points['left_eye'])
        right_eye_y = sum(p[1] for p in points['right_eye']) / len(points['right_eye'])

        # Calculate distance between eyebrows and eyes
        left_eyebrow_elevation = left_eye_y - left_eyebrow_y
        right_eyebrow_elevation = right_eye_y - right_eyebrow_y

        # Average eyebrow elevation
        eyebrow_elevation = (left_eyebrow_elevation + right_eyebrow_elevation) / 2

        # Calculate face dimensions for more robust normalization
        # Use the distance between eyes as a horizontal reference
        inter_eye_distance = abs(points['left_eye'][0][0] - points['right_eye'][8][0])

        # Use a combination of vertical and horizontal face dimensions for normalization
        # This makes the detection more invariant to head tilt
        face_height = abs(points['left_eyebrow'][0][1] - points['mouth_outline'][13][1])
        face_diagonal = math.sqrt(face_height**2 + inter_eye_distance**2)

        if face_diagonal > 0:  # Avoid division by zero
            # Normalize using the face diagonal instead of just height
            # This helps account for head tilt
            normalized_eye_height = (left_eye_height + right_eye_height) / (2 * face_diagonal * 0.5)
            normalized_eyebrow_elevation = eyebrow_elevation / (face_diagonal * 0.3)
        else:
            normalized_eye_height = 0
            normalized_eyebrow_elevation = 0

        # Calculate mouth openness for surprise detection
        # For surprise, we want to detect when the mouth is open (height is significant compared to width)
        mouth_openness_ratio = mouth_height / mouth_width if mouth_width > 0 else 0

        # Normalize mouth openness using the face diagonal (same as eye height and eyebrow elevation)
        # This makes the detection more invariant to head tilt
        normalized_mouth_openness = mouth_height / (face_diagonal * 0.3) if face_diagonal > 0 else 0

        # Check if mouth is open enough for surprise
        is_mouth_open = normalized_mouth_openness > self.expression_params['mouth_openness_threshold']

        # Combined surprise score (weighted combination of eye height, eyebrow elevation, and mouth openness)
        # Give more weight to mouth openness for surprise detection
        surprise_score = (normalized_eye_height * 0.4) + (normalized_eyebrow_elevation * 0.3) + (normalized_mouth_openness * 0.3)

        # Boost surprise score if all three components are present
        if is_mouth_open and normalized_eye_height > self.expression_params['surprise_threshold'] * 0.8 and normalized_eyebrow_elevation > 0.05:
            surprise_score *= 1.5  # Boost the score when all surprise components are detected

        # Determine expression based on scores and thresholds
        smile_confidence = max(0, min(1.0, (smile_score - self.expression_params['smile_threshold']) * 0.5))

        # For surprise, check if all components are present
        all_surprise_components = (normalized_mouth_openness > self.expression_params['mouth_openness_threshold'] and 
                                  normalized_eye_height > self.expression_params['surprise_threshold'] * 0.8 and 
                                  normalized_eyebrow_elevation > 0.05)

        # Calculate surprise confidence with a bonus if all components are present
        base_surprise_confidence = max(0, min(1.0, (surprise_score - self.expression_params['surprise_threshold']) * 2.5))
        surprise_confidence = base_surprise_confidence

        # Apply a bonus to surprise confidence if all components are present
        if all_surprise_components:
            surprise_confidence = min(1.0, surprise_confidence * 1.2)

        # Debug information
        # print(f"Smile score: {smile_score:.2f}, threshold: {self.expression_params['smile_threshold']}, confidence: {smile_confidence:.2f}")
        # print(f"Surprise score: {surprise_score:.2f}, threshold: {self.expression_params['surprise_threshold']}, confidence: {surprise_confidence:.2f}")

        # Choose the expression with the highest confidence
        if smile_confidence > surprise_confidence and smile_confidence > self.expression_params['min_confidence']:
            expression = "smile"
            confidence = smile_confidence
        elif surprise_confidence > smile_confidence and surprise_confidence > self.expression_params['min_confidence']:
            expression = "surprise"
            confidence = surprise_confidence
        else:
            expression = "neutral"
            # For neutral, confidence is inverse of how close we are to other expressions
            confidence = 1.0 - max(smile_confidence, surprise_confidence)

        return expression, confidence

    def draw_expression(self, frame, expression, confidence, face_landmarks=None):
        """
        Draw the detected expression on the frame.

        Args:
            frame: BGR image frame
            expression: Detected facial expression
            confidence: Confidence score for the detected expression
            face_landmarks: MediaPipe face landmarks (optional)

        Returns:
            frame: Frame with expression information drawn
        """
        # Define colors for different expressions
        colors = {
            "smile": (0, 255, 0),     # Green
            "surprise": (0, 165, 255), # Orange
            "neutral": (255, 255, 0)   # Cyan
        }

        color = colors.get(expression, (255, 255, 255))  # Default to white

        # If face landmarks are provided, position the text above the head
        if face_landmarks:
            h, w = frame.shape[:2]
            landmarks = face_landmarks.landmark

            # Find the top of the head (minimum y value of all landmarks)
            min_y = min(landmark.y for landmark in landmarks)

            # Find the center x position of the face
            face_x_coords = [landmark.x for landmark in landmarks]
            center_x = int((min(face_x_coords) + max(face_x_coords)) / 2 * w)

            # Position for the text (above the head)
            text_x = max(10, center_x - 100)  # Ensure it's not too far left
            text_y = max(30, int(min_y * h) - 10)  # Ensure it's not too high

            # Draw expression text with a more subtle font
            cv2.putText(frame, f"{expression.capitalize()} ({int(confidence * 100)}%)", 
                       (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
        else:
            # Fallback to fixed position if no landmarks are provided
            cv2.putText(frame, f"Expression: {expression.capitalize()}", (10, 160), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 1)

            # Draw confidence bar
            bar_length = 180
            bar_height = 25
            filled_length = int(bar_length * confidence)

            # Draw empty bar
            cv2.rectangle(frame, (10, 190), (10 + bar_length, 190 + bar_height), (100, 100, 100), -1)
            # Draw filled portion
            cv2.rectangle(frame, (10, 190), (10 + filled_length, 190 + bar_height), color, -1)
            # Draw border
            cv2.rectangle(frame, (10, 190), (10 + bar_length, 190 + bar_height), (200, 200, 200), 2)

            # Add confidence percentage
            cv2.putText(frame, f"{int(confidence * 100)}%", (10 + bar_length + 5, 190 + 15), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)

            # Add expression guidance based on detected expression
            guidance_y = 230
            if expression == "neutral":
                cv2.putText(frame, "Try smiling or raising eyebrows!", (10, guidance_y), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            elif expression == "smile" and confidence < 0.7:
                cv2.putText(frame, "Smile more widely for better detection", (10, guidance_y), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            elif expression == "surprise" and confidence < 0.7:
                cv2.putText(frame, "Raise eyebrows more for better detection", (10, guidance_y), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

        return frame
