"""Create local directories and ManimGL config after installing requirements."""
from pathlib import Path
import imageio_ffmpeg
import yaml

root = Path(__file__).resolve().parent
for directory in ['assets', 'assets/part2', 'qa', 'qa/part2', 'output', 'tools']:
    (root / directory).mkdir(parents=True, exist_ok=True)

config = root / 'custom_config.yml'
if config.exists():
    print('Keeping existing custom_config.yml')
else:
    config.write_text(yaml.safe_dump({
        'camera': {'background_color': '#101723', 'fps': 30,
                   'resolution': '(1920, 1080)'},
        'file_writer': {'ffmpeg_bin': imageio_ffmpeg.get_ffmpeg_exe(),
                        'pixel_format': 'yuv420p', 'video_codec': 'libx264'},
        'text': {'font': 'Segoe UI'},
    }, sort_keys=False), encoding='utf8')
    print('Created custom_config.yml with the installed FFmpeg path')
print('Project directories are ready.')
