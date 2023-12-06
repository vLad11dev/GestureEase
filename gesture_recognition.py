import cv2
import pyautogui
import mediapipe as mp
import psutil
from threading import Thread

class GestureRecognition:
    def __init__(self):
        self.WIDTH, self.HEIGHT = pyautogui.size()
        self.cap = None
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(static_image_mode=False, max_num_hands=1,
                                         min_detection_confidence=0.5, min_tracking_confidence=0.5)
        self.mp_drawing = mp.solutions.drawing_utils
        self.WMPLAYER_OPENED = False
        self.time = 0

        for proc in psutil.process_iter():
            if proc.name() == 'wmplayer.exe':
                self.WMPLAYER_OPENED = True

    def start_camera(self):
        self.cap = cv2.VideoCapture(0)

    def stop_camera(self):
        if self.cap:
            self.cap.release()

    def display_frame(self, frame, window_name='Hand Gestures'):
        cv2.imshow(window_name, frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            self.stop_camera()
            cv2.destroyAllWindows()

    def gesture_recognition(self, frame):
        frame_height, frame_width, _ = frame.shape

        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        results = self.hands.process(image_rgb)

        hand_gesture = 'unknown'

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                self.mp_drawing.draw_landmarks(frame, hand_landmarks)

                keypoint = []
                for i in hand_landmarks.landmark:
                    keypoint.append({
                        'x': i.x,
                        'y': i.y,
                    })

                if (keypoint[8]['y'] < keypoint[5]['y']
                        and keypoint[8]['x'] > keypoint[4]['x']
                        and keypoint[16]['y'] > keypoint[13]['y']
                        and keypoint[20]['y'] > keypoint[17]['y']
                ):
                    self.time = 0
                    hand_gesture = "other"

                    thumb_x_on_frame = int(keypoint[4]['x'] * frame_width)
                    thumb_y_on_frame = int(keypoint[4]['y'] * frame_height)

                    thumb_x = self.WIDTH / frame_width * thumb_x_on_frame * 1.5
                    thumb_y = self.HEIGHT / frame_height * thumb_y_on_frame * 1.5

                    pyautogui.moveTo(thumb_x - 200, thumb_y - 300)

                    if keypoint[8]['y'] > keypoint[6]['y']:
                        pyautogui.click()
                        pyautogui.sleep(0.5)

                elif (
                        keypoint[8]['y'] < keypoint[5]['y']
                        and keypoint[12]['y'] > keypoint[9]['y']
                        and keypoint[16]['y'] > keypoint[14]['y']
                        and keypoint[20]['y'] > keypoint[18]['y']
                        and keypoint[4]['x'] > keypoint[8]['x']
                ):
                    self.time += 1
                    print(self.time)
                    hand_gesture = 'pointing up'

                elif (
                        keypoint[8]['y'] > keypoint[5]['y']
                        and keypoint[8]['y'] > keypoint[7]['y']
                        and keypoint[12]['y'] < keypoint[10]['y']
                        and keypoint[16]['y'] < keypoint[14]['y']
                        and keypoint[20]['y'] < keypoint[18]['y']
                        and keypoint[4]['x'] > keypoint[8]['x']
                ):
                    self.time -= 1
                    print(self.time)
                    hand_gesture = 'pointing down'

                elif (
                        keypoint[8]['y'] < keypoint[5]['y']
                        and keypoint[8]['y'] < keypoint[7]['y']
                        and keypoint[12]['y'] > keypoint[10]['y']
                        and keypoint[16]['y'] > keypoint[14]['y']
                        and keypoint[20]['y'] < keypoint[17]['y']
                        and keypoint[20]['y'] < keypoint[19]['y']
                        and keypoint[4]['x'] < keypoint[8]['x']
                ):
                    hand_gesture = 'wmp'

                elif (
                        keypoint[8]['y'] < keypoint[5]['y']
                        and keypoint[8]['y'] < keypoint[7]['y']
                        and keypoint[12]['y'] < keypoint[10]['y']
                        and keypoint[16]['y'] < keypoint[14]['y']
                        and keypoint[20]['y'] < keypoint[17]['y']
                        and keypoint[20]['y'] < keypoint[19]['y']
                        and keypoint[4]['x'] < keypoint[8]['x']
                ):
                    self.time += 1
                    print(self.time)
                    hand_gesture = 'stop music'

                else:
                    self.time = 0
                    print("other")
                    hand_gesture = 'other'

                if hand_gesture == 'pointing up' and self.time > 20:
                    pyautogui.press('volumeup')
                elif hand_gesture == 'pointing down' and self.time < -20:
                    pyautogui.press('volumedown')
                elif hand_gesture == 'wmp':
                    self.WMPLAYER_OPENED = False
                    for proc in psutil.process_iter():
                        if proc.name() == 'wmplayer.exe':
                            self.WMPLAYER_OPENED = True
                    if not self.WMPLAYER_OPENED:
                        pyautogui.hotkey('win', 'r')
                        pyautogui.write('wmplayer')
                        pyautogui.press('enter')
                        pyautogui.sleep(1)
                        self.WMPLAYER_OPENED = True
                elif hand_gesture == 'stop music' and self.time > 30:
                    pyautogui.press('playpause')
                    self.time = 0

                self.display_frame(frame)

    def gesture_recognition_thread(self):
        self.start_camera()

        while True:
            ret, frame = self.cap.read()

            if frame is None:
                break

            frame = cv2.flip(frame, 1)
            self.gesture_recognition(frame)

        self.stop_camera()
        cv2.destroyAllWindows()

    def start_gesture_recognition_thread(self):
        gesture_thread = Thread(target=self.gesture_recognition_thread)
        gesture_thread.start()

# For testing the module
if __name__ == "__main__":
    gesture_recognition_instance = GestureRecognition()
    gesture_recognition_instance.start_gesture_recognition_thread()

    while True:
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    gesture_recognition_instance.stop_camera()
    cv2.destroyAllWindows()
