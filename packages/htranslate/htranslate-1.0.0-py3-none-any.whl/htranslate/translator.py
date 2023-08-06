def translate_to_h(text: str, delimiter: str = " ") -> str:
    return delimiter.join([bin(ord(c))[2:] for c in text]).replace("0", "h").replace("1", "H")

def translate_from_h(text: str, delimiter: str = " ") -> str:
    parts = text.replace("h", "0").replace("H", "1").split(delimiter)

    return "".join([chr(int(s, 2)) for s in parts])
