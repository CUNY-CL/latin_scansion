"""Code for reading and writing scansion text-format protocol buffers."""

from google.protobuf import text_format  # type: ignore

from . import scansion_pb2  # type: ignore


# TODO(kbg): Add read and write functions for Verse messages, if needed.


def read_document(path: str) -> scansion_pb2.Document:
    """Reads document message from file.

    Args:
     path: file path to read from.

    Returns:
       A parsed document message.
    """
    document = scansion_pb2.Document()
    with open(path, "r") as source:
        text_format.ParseLines(source, document)
    return document


def write_document(document: scansion_pb2.Document, path: str) -> None:
    """Writes document message to file.

    Args:
      document: the document message to write
      path: file path to write to.
    """
    with open(path, "w") as sink:
        text_format.PrintMessage(document, sink, as_utf8=True)
