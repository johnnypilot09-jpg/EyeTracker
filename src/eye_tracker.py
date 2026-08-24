import cv2
import threading
import os
import sys
import ctypes
import time
import winsound
from datetime import datetime

VIDEO_PATH = "meme_video.mp4"
SOUND_PATH = "meme_sound.wav"
FRAMES_NO_FACE = 10

if not os.path.exists(VIDEO_PATH):
    ctypes.windll.user32.MessageBoxW(0, "Файл meme_video.mp4 не найден. Иди иди.", "Ошибка", 0)
    sys.exit(1)

def add_to_startup():
    try:
        exe_path = sys.argv[0] if getattr(sys, 'frozen', False) else os.path.abspath(__file__)
        startup = os.path.join(os.getenv('APPDATA'), r'Microsoft\Windows\Start Menu\Programs\Startup')
        shortcut = os.path.join(startup, "MemeTracker.lnk")
        if not os.path.exists(shortcut):
            import pythoncom
            from win32com.client import Dispatch
            shell = Dispatch('WScript.Shell')
            sc = shell.CreateShortCut(shortcut)
            sc.Targetpath = exe_path
            sc.WorkingDirectory = os.path.dirname(exe_path)
            sc.save()
    except:
        pass

add_to_startup()

def get_cascade():
    if getattr(sys, 'frozen', False):
        base = sys._MEIPASS
    else:
        base = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(base, "haarcascade_frontalface_default.xml")
    if not os.path.exists(path):
        path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
    return cv2.CascadeClassifier(path)

cascade = get_cascade()

def play_meme(stop_event):
    cap = cv2.VideoCapture(VIDEO_PATH)
    cv2.namedWindow("ну мем чё", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("ну мем чё", 640, 480)
    try:
        cv2.setWindowProperty("meme", cv2.WND_PROP_TOPMOST, 1)
    except:
        pass
    if os.path.exists(SOUND_PATH):
        winsound.PlaySound(SOUND_PATH, winsound.SND_FILENAME | winsound.SND_ASYNC | winsound.SND_LOOP)
    while not stop_event.is_set():
        ret, frame = cap.read()
        if not ret:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            continue
        cv2.imshow("Meme", frame)
        if cv2.waitKey(30) & 0xFF == ord('q'):
            break
    winsound.PlaySound(None, winsound.SND_PURGE)
    cap.release()
    cv2.destroyWindow("Meme")

def exit_hotkey():
    user32 = ctypes.windll.user32
    return (user32.GetAsyncKeyState(0x11) & 0x8000) and (user32.GetAsyncKeyState(0x10) & 0x8000) and (user32.GetAsyncKeyState(0x51) & 0x8000)

def init_video_writer(frame_width, frame_height, fps=20.0):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"reaction_{timestamp}.mp4"
    if getattr(sys, 'frozen', False):
        base_dir = os.path.dirname(sys.argv[0])
    else:
        base_dir = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(base_dir, filename)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(filepath, fourcc, fps, (frame_width, frame_height))
    return out, filepath

cap = cv2.VideoCapture(0)
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
video_writer, reaction_file = init_video_writer(frame_width, frame_height)
print(f"Запись реакции в файл: {reaction_file}")

no_face = 0
video_thread = None
stop_event = None
video_playing = False

print("Программа в фоне. Ctrl+Shift+Q - выход. Видео реакции сохранится при выходе.")

while True:
    ret, frame = cap.read()
    if not ret:
        break
    video_writer.write(frame)
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = cascade.detectMultiScale(gray, 1.3, 5)
    face_detected = len(faces) > 0

    if face_detected:
        no_face = 0
        if video_playing:
            stop_event.set()
            video_thread.join(timeout=1)
            video_playing = False
    else:
        no_face += 1
        if no_face >= FRAMES_NO_FACE and not video_playing:
            stop_event = threading.Event()
            video_thread = threading.Thread(target=play_meme, args=(stop_event,))
            video_thread.daemon = True
            video_thread.start()
            video_playing = True

    if exit_hotkey():
        break
    time.sleep(0.03)

if video_playing:
    stop_event.set()
    video_thread.join(timeout=1)
cap.release()
video_writer.release()
cv2.destroyAllWindows()
print(f"Видео реакции по пути: {reaction_file}")