import cv2
import numpy as np
import mediapipe as mp
from deepface import DeepFace
from agno.tools import tool 
import json

def log_before_call(fn):
     print(f"About to call function with arguments: {fn.arguments}")

def log_after_call(fn):
    """Post-hook function that runs after the tool execution"""
    print(f"Function call completed with result: {fn.result}")

@tool(
    name="facial_expression_analyzer",
    description="Analyzes facial expressions to detect emotions and engagement",
    show_result=True,
    stop_after_tool_call=True,
    pre_hook=log_before_call,                       # Hook to run before execution
    post_hook=log_after_call,                       # Hook to run after execution
    cache_results=False,                            # Enable caching of results
    cache_dir="/tmp/agno_cache",                    # Custom cache directory
    cache_ttl=3600  
)

def analyze_facial_expression(video_path:str)->dict:
     
    mp_face_mesh= mp.solutions.face_mesh
    face_mesh=mp_face_mesh.FaceMesh(static_image_mode=False,max_num_faces=1)
    cap=cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(" Cannot open video.")
    else:
        print(" Video opened.")

    emotion_timeline = []
    eye_contact_count = 0
    smile_count = 0
    frame_count = 0
    fps=cap.get(cv2.CAP_PROP_FPS)

    frame_interval=5

    while cap.isOpened():
        ret,frame=cap.read()
        if not ret:
            break

        frame_count+=1
        if frame_count % frame_interval != 0:
            continue

        #resize frame for faster processimg
        frame = cv2.resize(frame,(640,480))
        rgb_frame=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        results=face_mesh.process(rgb_frame)

        if results.multi_face_landmarks:
            print(f" Face detected at frame {frame_count}")
            for face_landmarks in results.multi_face_landmarks:
                landmarks=face_landmarks.landmark

                #convert landmark to pixel coordinates
                h,w,_ = frame.shape
                landmark_cordinates=[(int(lm.x * w), int(lm.y * h)) for lm in landmarks]

                #emotion detection
                try:
                    analysis= DeepFace.analyze(frame,actions=['emotion'],enforce_detection=False)
                    print(f" DeepFace emotion: {analysis[0]['dominant_emotion']} at frame {frame_count}")
                    emotion = analysis[0]['dominant_emotion']
                    if emotion == "happy":
                        smile_count+=1

                    timestamp = frame_count/fps
                    #timestamp to seconds
                    timestamp=round(timestamp,2)
                    emotion_timeline.append({"timestamp": timestamp, "emotion": emotion})
                except Exception as e:
                    print(f"Error analyzing frame: {e}")
                    continue

                #eye contact estimation
                left_eye_upper_lid = landmark_cordinates[159]
                left_eye_lower_lid = landmark_cordinates[145]
                right_eye_upper_lid = landmark_cordinates[386]
                right_eye_lower_lid = landmark_cordinates[374]

                left_eye_opening = np.linalg.norm(np.array(left_eye_upper_lid) - np.array(left_eye_lower_lid))
                right_eye_opening = np.linalg.norm(np.array(right_eye_upper_lid) - np.array(right_eye_lower_lid))

                eye_opening_avg = (left_eye_opening + right_eye_opening) / 2

                if eye_opening_avg > 5:  # Threshold adjustment through experimentation
                    eye_contact_count += 1
        else:
            print(f" No face detected at frame {frame_count}")

    cap.release()
    face_mesh.close()

    total_processed_frames = frame_count // frame_interval
    if total_processed_frames == 0:
        total_processed_frames = 1  # Avoid division by zero

    return json.dumps({
        "emotion_timeline": emotion_timeline,
        "engagement_metrics": {
            "eye_contact_frequency": eye_contact_count / total_processed_frames,
            "smile_frequency": smile_count / total_processed_frames
        }
    })
# result = analyze_facial_expression("C:/Users/Gagan Shetty/Documents/Speech_Trainer/backend/WIN_20250709_11_04_53_Pro.mp4")
# print(result)




