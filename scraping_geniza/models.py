from pydantic import BaseModel
from typing import List, Optional, Tuple

class Folio(BaseModel):
    folio_name: Optional[str] = None
    folio_lines_original: Optional[List[Tuple[int, str]]] = None
    folio_lines_translation: Optional[List[Tuple[int, str]]] = None
    original_language: Optional[str] = None
    translation_language: Optional[str] = None

    def __str__(self) -> str:
        original_text = "\n".join(f"{i}. {line}" for i, line in self.folio_lines_original or [])
        translation_text = "\n".join(f"{i}. {line}" for i, line in self.folio_lines_translation or [])
        return (f"Folio Name: {self.folio_name}\n"
                f"Original Language: {self.original_language}\n"
                f"Translation Language: {self.translation_language}\n"
                f"Original Text:\n{original_text}\n"
                f"Translation Text:\n{translation_text}")

class TextData(BaseModel):
    folios: List[Folio]
    transcriber: Optional[str] = None
    

    @property
    def combined_original_language(self) -> str:
        return "\n".join(f"{i}. {line}" for folio in self.folios for i, line in folio.folio_lines_original or [])
    
    @property
    def combined_translation(self) -> str:
        return "\n".join(f"{i}. {line}" for folio in self.folios for i, line in folio.folio_lines_translation or [])
    
    def __str__(self) -> str:
        folios_str = "\n\n".join(str(folio) for folio in self.folios)
        return (f"Transcriber: {self.transcriber}\n"
                f"Folios:\n{folios_str}")

class GenizaDocument(BaseModel):
    pgpid: int
    primary_languages: Optional[List[str]] = None
    secondary_languages: Optional[List[str]] = None
    editor: Optional[str] = None
    description: Optional[str] = None
    text_datas: Optional[List[TextData]] = None

    def __str__(self) -> str:
        text_datas_str = "\n\n".join(str(text_data) for text_data in self.text_datas or [])
        return (f"PGPID: {self.pgpid}\n"
                f"Primary Languages: {', '.join(self.primary_languages or [])}\n"
                f"Secondary Languages: {', '.join(self.secondary_languages or [])}\n"
                f"Editor: {self.editor}\n"
                f"Description: {self.description}\n"
                f"Text Data:\n{text_datas_str}")



# if __name__ == "__main__":
#     folio_a = Folio(folio_name="Recto", folio_lines_original = ["hello, how are you?", "I am doing well, thank you"], folio_lines_translation = ['ca va?', 'ca va bien, merci'])
#     folio_b = Folio(folio_name="Verso", folio_lines_original = ["Golly gee, how are you?", "who says 'golly gee?'"], folio_lines_translation = ['golly gee', 'ques es esto'])
#     textdata_a = TextData(folios=[folio_a,folio_b], transcriber="Joe")

#     genizaDoc = GenizaDocument(
#         pgpid = 1,
#         text_datas = [textdata_a], 
#         description = "hey, whats going on here?", 
#         primary_languages = ["english"],
#         secondary_languages = ['english', 'thai', 'greek'],
#         editor = "JS"
#         )
#     print(genizaDoc)

