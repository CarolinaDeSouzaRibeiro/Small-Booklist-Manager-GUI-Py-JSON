from re import sub as re_sub

text_cleaner = lambda text: re_sub(r"\W", "", text).lower().strip()

def id_encode(id_keyword:str):
    """Gera um ID via codificação simples
    """
    id_keyword = text_cleaner(id_keyword)

    codificado = int.from_bytes(id_keyword.encode("utf-8"), "big")
    return codificado

def id_decode(id:int):
    '''Decodifica um ID gerado via id_encode'''
    return id.to_bytes((id.bit_length() + 7) // 8, "big").decode("utf-8")