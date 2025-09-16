from utils.file_utils import scan_files, categorize_files, detect_file_type, extract_audio_metadata, copy_files
from utils.conflict_resolver import resolve_conflicts
from utils.html_report import generate_html_report
from utils.xls_report import generate_csv_report

class SharedStore(dict):
    pass

class FileScannerNode:
    def __init__(self, shared):
        self.shared = shared
    def run(self, source_directory):
        self.shared['source_directory'] = source_directory
        self.shared['file_metadata'] = scan_files(source_directory)

class FileCategorizerNode:
    def __init__(self, shared):
        self.shared = shared
    def run(self, destination_directory):
        source_directory = self.shared.get('source_directory')
        # Extract audio metadata for audio files
        for meta in self.shared['file_metadata']:
            if detect_file_type(meta['path']) == 'audio':
                meta['extra_metadata'] = extract_audio_metadata(meta['path'])
        self.shared['categorized_files'] = categorize_files(
            self.shared['file_metadata'], destination_directory, source_directory)

class ConflictResolverNode:
    def __init__(self, shared):
        self.shared = shared
    def run(self):
        resolved = {}
        for category, files in self.shared['categorized_files'].items():
            resolved[category] = {}
            for src, dest in files.items():
                strategy = category[:-1] if category.endswith('s') else category
                resolved[category][src] = resolve_conflicts(self.shared['file_metadata'][0], dest, strategy)
        self.shared['conflict_resolved_files'] = resolved

class FileCopierNode:
    def __init__(self, shared):
        self.shared = shared
    def run(self, destination_directory):
        copy_files(self.shared['conflict_resolved_files'], destination_directory)
        self.shared['copied_files'] = self.shared['conflict_resolved_files']

class ReportGeneratorNode:
    def __init__(self, shared):
        self.shared = shared
    def run(self, destination_directory):
        # HTML reports for images and videos
        for category in ['images', 'videos']:
            files = self.shared['copied_files'].get(category, {})
            if files:
                generate_html_report(self.shared['copied_files'], destination_directory, category)
        # CSV report for audio
        if self.shared['copied_files'].get('audio', {}):
            generate_csv_report(self.shared['copied_files'], destination_directory, 'audio')
        # Excel report for other
        if self.shared['copied_files'].get('other', {}):
            from utils.xls_report import generate_excel_report
            generate_excel_report(self.shared['copied_files'], destination_directory)
        # Master Excel report for all files
        from utils.xls_report import generate_master_report
        generate_master_report(
            self.shared['file_metadata'],
            self.shared['categorized_files'],
            self.shared['copied_files'],
            destination_directory
        )