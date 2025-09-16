import os
import datetime
from typing import List, Dict
import mimetypes
from collections import defaultdict
from mutagen import File as MutagenFile
import shutil

def scan_files(source_directory: str) -> List[Dict]:
    """
    Recursively scan the source directory and extract metadata for each file.
    Returns a list of dicts with keys: path, type, size, created, modified, extra_metadata.
    """
    file_metadata = []
    for root, _, files in os.walk(source_directory):
        for name in files:
            path = os.path.join(root, name)
            try:
                stat = os.stat(path)
                created = datetime.datetime.fromtimestamp(stat.st_ctime)
                modified = datetime.datetime.fromtimestamp(stat.st_mtime)
                size = stat.st_size
                file_metadata.append({
                    "path": path,
                    "type": None,  # To be filled by categorize_files
                    "size": size,
                    "created": created,
                    "modified": modified,
                    "extra_metadata": {}
                })
            except Exception as e:
                print(f"Error reading file {path}: {e}")
    return file_metadata

def detect_file_type(file_path: str) -> str:
    """
    Detect file type: image, video, audio, other.
    """
    mime, _ = mimetypes.guess_type(file_path)
    if mime:
        if mime.startswith('image'):
            return 'image'
        elif mime.startswith('video'):
            return 'video'
        elif mime.startswith('audio'):
            return 'audio'
    return 'other'


def categorize_files(file_metadata: list, destination_directory: str, source_directory: str = None) -> dict:
    """
    Categorize files by type and organize them into destination subdirectories.
    For 'other' files, preserve only the subdirectory structure below the source directory.
    """
    categorized = defaultdict(dict)
    for meta in file_metadata:
        ftype = detect_file_type(meta['path'])
        meta['type'] = ftype
        if ftype == 'image' or ftype == 'video':
            year = meta['created'].strftime('%Y')
            month = meta['created'].strftime('%m-%Y')
            dest = os.path.join(destination_directory, ftype + 's', year, month)
            fname = os.path.basename(meta['path'])
            categorized[ftype + 's'][meta['path']] = os.path.join(dest, fname)
        elif ftype == 'audio':
            # Extract audio metadata
            audio_metadata = extract_audio_metadata(meta['path'])
            artist = audio_metadata.get('artist', 'UnknownArtist')
            album = audio_metadata.get('album', 'UnknownAlbum')
            title = audio_metadata.get('title', 'UnknownTitle')
            dest = os.path.join(destination_directory, 'audio', artist, album)
            fname = os.path.basename(meta['path'])
            categorized['audio'][meta['path']] = os.path.join(dest, fname)
        else:
            # Keep only subdirectories below source_directory for 'other'
            if source_directory:
                rel_path = os.path.relpath(meta['path'], source_directory)
            else:
                rel_path = os.path.relpath(meta['path'], os.path.dirname(destination_directory))
            categorized['other'][meta['path']] = os.path.join(destination_directory, 'other', rel_path)
    return categorized

def extract_audio_metadata(audio_file_path: str) -> dict:
    """
    Extract artist, album, and title from audio file using mutagen.
    """
    metadata = {'artist': 'UnknownArtist', 'album': 'UnknownAlbum', 'title': 'UnknownTitle'}
    try:
        audio = MutagenFile(audio_file_path)
        if audio:
            metadata['artist'] = (audio.tags.get('TPE1') or ['UnknownArtist'])[0] if 'TPE1' in audio.tags else metadata['artist']
            metadata['album'] = (audio.tags.get('TALB') or ['UnknownAlbum'])[0] if 'TALB' in audio.tags else metadata['album']
            metadata['title'] = (audio.tags.get('TIT2') or ['UnknownTitle'])[0] if 'TIT2' in audio.tags else metadata['title']
    except Exception as e:
        print(f"Error extracting audio metadata from {audio_file_path}: {e}")
    return metadata

def copy_files(categorized_files: dict, destination_directory: str):
    """
    Copy files to the destination directory.
    """
    for category, files in categorized_files.items():
        for src, dest in files.items():
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            if not os.path.exists(dest):
                shutil.copy2(src, dest)
            # else: conflict resolution should have already handled naming