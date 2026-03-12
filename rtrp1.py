import cv2
import mediapipe as mp
import time
import math

# Initialize MediaPipe Face Mesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(max_num_faces=1, refine_landmarks=True, min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Eye Landmark Indices (MediaPipe)
LEFT_EYE = [362, 385, 387, 263, 373, 380]
RIGHT_EYE = [33, 160, 158, 133, 153, 144]

# EAR Threshold to consider an eye closed
EAR_THRESH = 0.22

def calculate_distance(p1, p2):
    return math.hypot(p1[0] - p2[0], p1[1] - p2[1])

def calculate_ear(landmarks, indices, frame_w, frame_h):
    points = [(int(landmarks.landmark[i].x * frame_w), int(landmarks.landmark[i].y * frame_h)) for i in indices]
    
    # Vertical distances
    v1 = calculate_distance(points[1], points[5])
    v2 = calculate_distance(points[2], points[4])
    # Horizontal distance
    h = calculate_distance(points[0], points[3])
    
    # Eye Aspect Ratio
    ear = (v1 + v2) / (2.0 * h)
    return ear

# Start Video Capture
cap = cv2.VideoCapture(0)

# Variables for tracking time
eyes_closed_start_time = None
timeline_action = "Monitoring..."

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
        
    frame = cv2.flip(frame, 1) # Mirror the frame
    frame_h, frame_w, _ = frame.shape
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    results = face_mesh.process(rgb_frame)
    
    left_eye_status = "Open"
    right_eye_status = "Open"
    eyes_open_count = 2
    
    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            
            # Draw Eyelid Tracking Nodes
            for idx in LEFT_EYE + RIGHT_EYE:
                x = int(face_landmarks.landmark[idx].x * frame_w)
                y = int(face_landmarks.landmark[idx].y * frame_h)
                cv2.circle(frame, (x, y), 2, (0, 255, 255), -1) 
            
            # Calculate EAR for both eyes
            left_ear = calculate_ear(face_landmarks, LEFT_EYE, frame_w, frame_h)
            right_ear = calculate_ear(face_landmarks, RIGHT_EYE, frame_w, frame_h)
            
            # Check individual eyes
            if left_ear < EAR_THRESH:
                left_eye_status = "Closed"
                eyes_open_count -= 1
            if right_ear < EAR_THRESH:
                right_eye_status = "Closed"
                eyes_open_count -= 1

            # Determine Actions based on user logic
            if eyes_open_count == 1:
                timeline_action = "ACTION: LOUD HORN (One Eye Closed)"
                eyes_closed_start_time = None 
                
            elif eyes_open_count == 0:
                if eyes_closed_start_time is None:
                    eyes_closed_start_time = time.time()
                
                closed_duration = time.time() - eyes_closed_start_time
                
                # Escalation Timeline
                if closed_duration > 12:
                    timeline_action = "STAGE 5: Police & Ambulance"
                elif closed_duration > 10:
                    timeline_action = "STAGE 4: Spraying Water"
                elif closed_duration > 7:
                    timeline_action = "STAGE 3: Stop + Horn + Indicators"
                elif closed_duration > 5:
                    timeline_action = "STAGE 2: Slowing + Indicators"
                elif closed_duration > 3:
                    timeline_action = "STAGE 1: LOUD HORN"
                else:
                    timeline_action = f"Eyes Closed... ({int(closed_duration)}s)"
            else:
                eyes_closed_start_time = None
                timeline_action = "Status Normal: Driver Awake"
                
    # --- UI DISPLAY ---
    # Scaled down the font to prevent overlapping
    font_scale = 0.6 
    thickness = 2
    
    # Left Side: Timeline Actions
    cv2.putText(frame, "SYSTEM ACTION:", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, font_scale, (0, 255, 255), thickness)
    cv2.putText(frame, timeline_action, (10, 60), cv2.FONT_HERSHEY_SIMPLEX, font_scale, (0, 0, 255), thickness)
    
    # Right Side: Eye Status (Moved closer to the edge since text is smaller)
    cv2.putText(frame, f"Left Eye: {left_eye_status}", (frame_w - 220, 30), cv2.FONT_HERSHEY_SIMPLEX, font_scale, (0, 255, 0) if left_eye_status == "Open" else (0, 0, 255), thickness)
    cv2.putText(frame, f"Right Eye: {right_eye_status}", (frame_w - 220, 60), cv2.FONT_HERSHEY_SIMPLEX, font_scale, (0, 255, 0) if right_eye_status == "Open" else (0, 0, 255), thickness)
    cv2.putText(frame, f"Eyes Open: {eyes_open_count}", (frame_w - 220, 90), cv2.FONT_HERSHEY_SIMPLEX, font_scale, (255, 255, 0), thickness)

    # Updated Window Title
    cv2.imshow("Road Safety", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()