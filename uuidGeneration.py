import hashlib
import platform
import psutil
import uuid
import socket
import uuid
from datetime import datetime, time, timezone
from screeninfo import get_monitors
from PIL import Image

def get_time_zone_offset():
    utc_offset_sec = datetime.now(timezone.utc).astimezone().utcoffset().total_seconds()
    utc_offset_hours = int(utc_offset_sec / 3600)
    return str(utc_offset_hours)

def get_screen_resolution():
    monitors = get_monitors()
    if monitors:
        monitor = monitors[0]
        return f"{monitor.width}x{monitor.height}"
    return "Unknown"

def get_color_depth():
    img = Image.new('RGB', (1, 1))
    return img.mode

def format_uuid(uuid_str):
    return f"{uuid_str[:8]}-{uuid_str[8:12]}-{uuid_str[12:16]}-{uuid_str[16:20]}-{uuid_str[20:]}"

def get_device_uuid():
    user_agent = f"Python/{platform.python_version()}"
    os_info = platform.platform()
    cpu_info = str(psutil.cpu_count())
    mac_address = uuid.UUID(int=uuid.getnode()).hex[-12:]
    screen_resolution = get_screen_resolution()
    color_depth = get_color_depth()
    time_zone = get_time_zone_offset()
    hostname = socket.gethostname()

    combined_info = ":".join([
        user_agent,
        os_info,
        cpu_info,
        mac_address,
        screen_resolution,
        color_depth,
        time_zone,
        hostname
    ])

    hashed_uuid = hashlib.md5(combined_info.encode()).hexdigest()

    formatted_uuid = format_uuid(hashed_uuid)

    return formatted_uuid

device_uuid = get_device_uuid()
print(device_uuid)