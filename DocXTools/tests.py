from unittest import TestCase

# Create your tests here.
from docxtpl import DocxTemplate


class DocxGenTestCase(TestCase):
    def test_gen(self):
        doc = DocxTemplate('docx-templates/Договор лицевая сторона.docx')
        context = {'contract_id': '666-абв'}
        doc.render(context)
        doc.save('newdoc.docx')
