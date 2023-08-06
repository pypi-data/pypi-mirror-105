import unittest
from fbl.__main__ import pdf_extract_text, docx_extract_text

TEST_FILE_LOCATION_DOCX = "test/example.docx"
TEST_FILE_LOCATION_PDF = "test/example.pdf"
TEST_FILES_TEXT = """
Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.
"""

class ExtractTextTestCase(unittest.TestCase):
    maxDiff = None
    def test_pdf_extract_text(self):
        result = pdf_extract_text(TEST_FILE_LOCATION_PDF)
        self.assertEqual(result, TEST_FILES_TEXT)

    def test_docx_extract_text(self):
        result = docx_extract_text(TEST_FILE_LOCATION_DOCX)
        self.assertEqual(result, TEST_FILES_TEXT)
        pass

if __name__ == '__main__':
        unittest.main()


