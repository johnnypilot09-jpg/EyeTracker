import cv2
import threading
import os
import sys
import ctypes
import time
import winsound

VIDEO_PATH = "meme_video.mp4"
SOUND_PATH = "meme_sound.wav"
FRAMES_NO_FACE = 10

if not os.path.exists(VIDEO_PATH):
    ctypes.windll.user32.MessageBoxW(0, "Файл meme_video.mp4 не найден!", "Ошибка", 0)
    sys.exit(1)

# Автозагрузка
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

# Загрузка каскада
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

# Воспроизведение мема (видео + звук)
def play_meme(stop_event):
    # Видео
    cap = cv2.VideoCapture(VIDEO_PATH)
    cv2.namedWindow("😂 МЕМ", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("😂 МЕМ", 640, 480)
    try:
        cv2.setWindowProperty("😂 МЕМ", cv2.WND_PROP_TOPMOST, 1)
    except:
        pass
    # Звук (если есть WAV)
    if os.path.exists(SOUND_PATH):
        winsound.PlaySound(SOUND_PATH, winsound.SND_FILENAME | winsound.SND_ASYNC | winsound.SND_LOOP)
    while not stop_event.is_set():
        ret, frame = cap.read()
        if not ret:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            continue
        cv2.imshow("😂 МЕМ", frame)
        if cv2.waitKey(30) & 0xFF == ord('q'):
            break
    # Остановить звук
    winsound.PlaySound(None, winsound.SND_PURGE)
    cap.release()
    cv2.destroyWindow("😂 МЕМ")

# Горячая клавиша Ctrl+Shift+Q
def exit_hotkey():
    user32 = ctypes.windll.user32
    return (user32.GetAsyncKeyState(0x11) & 0x8000) and (user32.GetAsyncKeyState(0x10) & 0x8000) and (user32.GetAsyncKeyState(0x51) & 0x8000)

# Основной цикл
cap = cv2.VideoCapture(0)
no_face = 0
video_thread = None
stop_event = None
video_playing = False

print("Программа в фоне. Отвернись -> мем. Ctrl+Shift+Q - выход.")

while True:
    ret, frame = cap.read()
    if not ret:
        break
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = cascade.detectMultiScale(gray, 1.3, 5)
    face = len(faces) > 0

    if face:
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
cv2.destroyAllWindows()