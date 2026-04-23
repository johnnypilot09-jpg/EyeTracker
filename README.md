
<h1>👁️ Eye Tracker - Отвлекся и отвернулся? Теперь будешь смотреть на экран падла!</h1>
    <p><strong>Отвернись от камеры — и на весь экран вылетает мем со звуком!</strong></p>
    <p>Этот проект отслеживает ваше лицо через веб-камеру и автоматически запускает видео с мемом (и звуком), как только вы отводите взгляд или уходите из зоны видимости. Как только лицо снова появляется — мем мгновенно исчезает. Идеально для розыгрышей друзей или просто для весёлого времяпрепровождения.</p>
    <blockquote>
        <p>🎯 <strong>Фишки</strong><br>
        - Работает в фоне (окно камеры не показывается)<br>
        - Автоматическая загрузка при старте Windows (опционально)<br>
        - Выход по хоткею <code>Ctrl+Shift+Q</code> (даже во время проигрывания мема)<br>
        - Всё упаковано в один <code>.exe</code> — никаких установок Python или дополнительных библиотек на компьютере жертвы не требуется
        - Записывает видео жертвы и когда программа отключается ложит файл <code>mp4</code>в папку с приложением 😘</p>
    </blockquote>
    <hr>
    <h2>📦 Что входит в репозиторий</h2>
    <ul>
        <li><code>eye_tracker.py</code> — исходный код на Python</li>
        <li><code>requirements.txt</code> — зависимости для запуска из исходников</li>
        <li><code>haarcascade_frontalface_default.xml</code> — каскад Хаара для детекции лица (OpenCV)</li>
        <li><code>meme_video.mp4</code> — видео с мемом (без звука)</li>
        <li><code>meme_sound.wav</code> — звуковая дорожка мема (WAV)</li>
        <li><code>README.md</code> — этот файл</li>
        <li>(опционально) <code>eye_tracker.exe</code> — готовое приложение, собранное PyInstaller</li>
    </ul>
    <hr>
    <h2>🚀 Как запустить</h2>
    <h3>Вариант 1. Использовать готовый EXE (для друзей)</h3>
    <ol>
        <li>Скачайте папку с проектом или только файл <code>eye_tracker.exe</code></li>
        <li>Положите <strong>рядом с EXE</strong> файлы:
            <ul>
                <li><code>haarcascade_frontalface_default.xml</code></li>
                <li><code>meme_video.mp4</code></li>
                <li><code>meme_sound.wav</code></li>
            </ul>
        </li>
        <li>Запустите <code>eye_tracker.exe</code></li>
        <li>Программа добавит себя в автозагрузку (при первом запуске)</li>
        <li>Отвернитесь от веб-камеры — увидите мем!</li>
        <li>Чтобы выйти — нажмите <code>Ctrl+Shift+Q</code></li>
    </ol>
    <div class="note">
        <strong>Примечание:</strong> Никакой консоли нет, программа работает в фоне. Желательно положить EXE в отдельную папку и при желании создать ярлык на рабочем столе.
    </div>
    <h3>Вариант 2. Запуск из исходного кода Python</h3>
    <p>Если вы хотите модифицировать проект или просто запустить скрипт:</p>
    <ol>
        <li>Убедитесь, что установлен <strong>Python 3.10–3.14</strong> (на 3.14 протестировано)</li>
        <li>Установите зависимости:
            <pre><code>pip install -r requirements.txt</code></pre>
        </li>
        <li>Поместите в ту же папку файлы:
            <ul>
                <li><code>haarcascade_frontalface_default.xml</code></li>
                <li><code>meme_video.mp4</code></li>
                <li><code>meme_sound.wav</code></li>
            </ul>
        </li>
        <li>Запустите скрипт:
            <pre><code>python eye_tracker.py</code></pre>
        </li>
    </ol>
    <hr>
    <h2>🛠️ Как собрать свой EXE (для разработчиков)</h2>
    <p>Если вы хотите изменить код или встроить свой мем внутрь одного файла:</p>
    <ol>
        <li>Установите PyInstaller:
            <pre><code>pip install pyinstaller</code></pre>
        </li>
        <li>Соберите EXE с встраиванием каскада (видео и звук можно оставить снаружи или тоже встроить):
            <pre><code>pyinstaller --onefile --noconsole --add-data "haarcascade_frontalface_default.xml;." eye_tracker.py</code></pre>
        </li>
        <li>Готовый файл появится в папке <code>dist/</code></li>
    </ol>
    <p>Чтобы встроить видео и звук, добавьте флаги:</p>
    <pre><code>--add-data "meme_video.mp4;." --add-data "meme_sound.wav;."</code></pre>
    <hr>
    <h2>📝 Как это работает</h2>
    <ol>
        <li><strong>Детекция лица</strong> — используется классификатор Хаара из OpenCV (<code>haarcascade_frontalface_default.xml</code>). Он быстрый и не требует дополнительных моделей.</li>
        <li><strong>Фоновый режим</strong> — веб-камера читается в цикле, но окно с её изображением <strong>не показывается</strong>.</li>
        <li><strong>Запуск мема</strong> — если лицо не обнаружено в течение <code>FRAMES_NO_FACE = 10</code> кадров (~0.3 секунды), запускается отдельный поток:
            <ul>
                <li>Воспроизводится видео (<code>meme_video.mp4</code>) через OpenCV в отдельном окне (поверх всех окон)</li>
                <li>Одновременно зацикленно проигрывается звук (<code>meme_sound.wav</code>) через <code>winsound</code></li>
            </ul>
        </li>
        <li><strong>Остановка</strong> — как только лицо появляется, поток останавливается, окно и звук закрываются.</li>
        <li><strong>Автозагрузка</strong> — при первом запуске создаётся ярлык в <code>shell:startup</code>. Вы можете отключить это, закомментировав вызов <code>add_to_startup()</code> в коде.</li>
        <li><strong>Аварийный выход</strong> — глобальный хоткей <code>Ctrl+Shift+Q</code> (отслеживается через WinAPI) закрывает программу в любой момент.</li>
    </ol>
    <hr>
    <h2>📁 Структура файлов</h2>
    <pre><code>EyeTracker/
│
├── eye_tracker.py               # основной скрипт
├── requirements.txt             # зависимости
├── haarcascade_frontalface_default.xml   # каскад OpenCV
├── meme_video.mp4               # видео мема (без звука)
├── meme_sound.wav               # звук мема (WAV, зацикленный)
├── README.md                    # этот файл
└── (опционально) eye_tracker.exe  # собранное приложение</code></pre>
    <hr>
    <h2>❓ Часто задаваемые вопросы</h2>
    <p><strong>Почему нет звука в видео?</strong><br>
    OpenCV не воспроизводит звук из MP4. Поэтому мы используем отдельный WAV-файл, который запускается параллельно. Вы можете заменить его на любой другой WAV.</p>
    <p><strong>Как сделать свой мем?</strong><br>
    - Видео: любой MP4 (лучше не очень большой, чтобы EXE не раздувался)<br>
    - Звук: сконвертируйте MP3 в WAV (PCM, 16 бит) через онлайн-конвертер<br>
    - Положите файлы рядом с EXE (или пересоберите со встраиванием)</p>
    <p><strong>Программа не видит моё лицо?</strong><br>
    Проверьте освещение и расположение камеры. Хаар-каскад чувствителен к поворотам головы — смотрите прямо в объектив.</p>
    <p><strong>Как отключить автозагрузку?</strong><br>
    Нажмите <code>Win+R</code>, введите <code>shell:startup</code>, удалите ярлык <code>MemeTracker.lnk</code>.</p>
    <hr>
    <h2>🧪 Требования для запуска из Python</h2>
    <p>- Python 3.10 – 3.14<br>
    - Библиотеки из <code>requirements.txt</code>:</p>
    <pre><code>opencv-python
numpy
pywin32</code></pre>
    <p>Установка одной командой:</p>
    <pre><code>pip install -r requirements.txt</code></pre>
    <hr>
    <h2>⚠️ Примечания</h2>
    <ul>
        <li>Для работы звука требуется <strong>WAV-файл</strong>. MP3 не поддерживается <code>winsound</code>.</li>
        <li>Программа использует веб-камеру по индексу <code>0</code>. Если у вас несколько камер, может потребоваться изменить индекс в коде.</li>
        <li>На слабых компьютерах может наблюдаться небольшая задержка перед запуском мема (из-за детекции лица).</li>
    </ul>
    <hr>
    <div class="footer">
       <h2><p><code><strong>Created by YN</strong></code><br> </h1>
        Свободное использование, модификация и распространение приветствуются. Код написан в образовательных и развлекательных целях.</p>
        <p>🤝 По вопросам улучшения или багам — создавайте Issue в репозитории. Удачных пранков! 😈</p>
    </div>
</div>
</body>
</html>


### Telegram [`Y A N`](https://t.me/Anonimbotqq_Bot?start=anon_1085124509)
