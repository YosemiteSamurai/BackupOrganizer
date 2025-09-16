import os
from PIL import Image

def generate_thumbnails(image_path: str, thumbnail_size=(128, 128)) -> str:
    """
    Generate a thumbnail for the given image and return the thumbnail path.
    """
    thumb_dir = os.path.join(os.path.dirname(image_path), 'thumbnails')
    os.makedirs(thumb_dir, exist_ok=True)
    thumb_path = os.path.join(thumb_dir, os.path.basename(image_path))
    try:
        with Image.open(image_path) as img:
            img.thumbnail(thumbnail_size)
            img.save(thumb_path)
    except Exception as e:
        print(f"Error generating thumbnail for {image_path}: {e}")
    return thumb_path


def generate_html_report(organized_files: dict, destination_directory: str, category: str):
    """
    Generate an HTML gallery report for images or videos, organized by year and month.
    Displays each image as no larger than 100x100 pixels, sorted newest to oldest, with years in reverse chronological order.
    """
    report_path = os.path.join(destination_directory, category, 'index.html')
    years = {}
    file_dates = {}
    # Build mapping and collect modified dates
    for src, dest in organized_files.get(category, {}).items():
        parts = dest.split(os.sep)
        if len(parts) >= 4:
            year = parts[-3]
            month = parts[-2]
            years.setdefault(year, {}).setdefault(month, []).append(dest)
            try:
                file_dates[dest] = os.path.getmtime(dest)
            except Exception:
                file_dates[dest] = 0
    html = ['<html><body>']
    for year in sorted(years.keys(), reverse=True):
        html.append(f'<h2>{year}</h2>')
        months = years[year]
        for month, files in sorted(months.items()):
            # Sort files by modified date, newest first
            files_sorted = sorted(files, key=lambda f: file_dates.get(f, 0), reverse=True)
            html.append(f'<h3>{month}</h3><div style="display:flex;flex-wrap:wrap;">')
            for file in files_sorted:
                rel_file = os.path.relpath(file, os.path.dirname(report_path))
                html.append(f'<a href="{rel_file}" target="_blank"><img src="{rel_file}" style="max-width:100px;max-height:100px;margin:4px;object-fit:contain;"/></a>')
            html.append('</div>')
    html.append('</body></html>')
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(html))
    return report_path