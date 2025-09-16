import os
import shutil

def resolve_conflicts(file_info: dict, destination_path: str, strategy: str) -> str:
    """
    Resolve name conflicts based on file type and strategy.
    Strategies:
    - images/videos: if same size, keep original; if different, add index
    - audio: keep larger file
    - other: keep newer file
    """
    if not os.path.exists(destination_path):
        return destination_path
    src_size = file_info.get('size', 0)
    dest_size = os.path.getsize(destination_path)
    if strategy in ['image', 'video']:
        if src_size == dest_size:
            return destination_path  # keep original
        else:
            base, ext = os.path.splitext(destination_path)
            idx = 1
            new_path = f"{base}_{idx}{ext}"
            while os.path.exists(new_path):
                idx += 1
                new_path = f"{base}_{idx}{ext}"
            return new_path
    elif strategy == 'audio':
        return destination_path if dest_size > src_size else file_info['path']
    else:  # other
        src_mtime = file_info.get('modified')
        dest_mtime = os.path.getmtime(destination_path)
        return destination_path if dest_mtime > src_mtime.timestamp() else file_info['path']