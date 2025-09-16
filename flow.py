
from nodes import SharedStore, FileScannerNode, FileCategorizerNode, ConflictResolverNode, FileCopierNode, ReportGeneratorNode

class FileOrganizerFlow:
    def __init__(self, source_directory, destination_directory):
        self.shared = SharedStore()
        self.source_directory = source_directory
        self.destination_directory = destination_directory
        self.nodes = [
            FileScannerNode(self.shared),
            FileCategorizerNode(self.shared),
            ConflictResolverNode(self.shared),
            FileCopierNode(self.shared),
            ReportGeneratorNode(self.shared)
        ]
    def run(self):
        self.nodes[0].run(self.source_directory)
        self.nodes[1].run(self.destination_directory)
        self.nodes[2].run()
        self.nodes[3].run(self.destination_directory)
        self.nodes[4].run(self.destination_directory)