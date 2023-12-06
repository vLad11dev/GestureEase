import cv2
import pyautogui
import mediapipe as mp
import psutil

WIDTH, HEIGHT = pyautogui.size()
pyautogui.FAILSAFE = False # Для возможности перемещения курсора на край экрана

cap = cv2.VideoCapture(0)

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1,
                       min_detection_confidence=0.5, min_tracking_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

WMPLAYER_OPENED = False
for proc in psutil.process_iter():
    if proc.name() == 'wmplayer.exe':
        WMPLAYER_OPENED = True

time = 0
hand_gesture = "other"

while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    frame_height, frame_width, _ = frame.shape
    if not ret:
        break

    image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = hands.process(image_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks)

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
                time = 0
                hand_gesture = "other"

                # index_x_on_frame = int(keypoint[8]['x'] * frame_width)
                # index_y_on_frame = int(keypoint[8]['y'] * frame_height)

                thumb_x_on_frame = int(keypoint[4]['x'] * frame_width)
                thumb_y_on_frame = int(keypoint[4]['y'] * frame_height)

                # index_x = WIDTH / frame_width * index_x_on_frame
                # index_y = HEIGHT / frame_height * index_y_on_frame

                thumb_x = WIDTH / frame_width * thumb_x_on_frame * 1.5
                thumb_y = HEIGHT / frame_height * thumb_y_on_frame * 1.5

                # cv2.circle(img=frame, center=(index_x_on_frame, index_y_on_frame), radius=10, color=(0, 255, 255))
                # cv2.circle(img=frame, center=(thumb_x_on_frame, thumb_y_on_frame), radius=10, color=(0, 255, 255))
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
                time += 1
                print(time)
                hand_gesture = 'pointing up'

            elif (
                    keypoint[8]['y'] > keypoint[5]['y']
                    and keypoint[8]['y'] > keypoint[7]['y']
                    and keypoint[12]['y'] < keypoint[10]['y']
                    and keypoint[16]['y'] < keypoint[14]['y']
                    and keypoint[20]['y'] < keypoint[18]['y']
                    and keypoint[4]['x'] > keypoint[8]['x']
            ):
                time -= 1
                print(time)
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
                time += 1
                print(time)
                hand_gesture = 'stop music'

            # elif (keypoint[4]['y'] < keypoint[3]['y']
            #       and keypoint[5]['y'] < keypoint[9]['y']
            #       and keypoint[8]['x'] > keypoint[7]['x']
            #       and keypoint[12]['x'] > keypoint[11]['x']
            #       and keypoint[16]['x'] > keypoint[15]['x']
            #       and keypoint[20]['x'] > keypoint[19]['x']
            #       and keypoint[8]['x'] < keypoint[0]['x']
            #       and keypoint[12]['x'] < keypoint[0]['x']
            #       and keypoint[16]['x'] < keypoint[0]['x']
            #       and keypoint[20]['x'] < keypoint[0]['x']
            # ):
            #     hand_gesture = "vspich"

            else:
                time = 0
                print("other")
                hand_gesture = 'other'

            if hand_gesture == 'pointing up' and time > 20:
                pyautogui.press('volumeup')
            elif hand_gesture == 'pointing down' and time < -20:
                pyautogui.press('volumedown')
            elif hand_gesture == 'wmp':
                WMPLAYER_OPENED = False
                for proc in psutil.process_iter():
                    if proc.name() == 'wmplayer.exe':
                        WMPLAYER_OPENED = True
                if not WMPLAYER_OPENED:
                    pyautogui.hotkey('win', 'r')
                    pyautogui.write('wmplayer')
                    pyautogui.press('enter')
                    pyautogui.sleep(1)
                    WMPLAYER_OPENED = True
            elif hand_gesture == 'stop music' and time > 30:
                pyautogui.press('playpause')
                time = 0

            # elif hand_gesture == 'vspich':
            #     pyautogui.hotkey('win', 'h')

    cv2.imshow('hand gesture', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
