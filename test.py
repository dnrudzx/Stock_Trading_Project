def solution(encrypted_text, key, rotation):
    rotation = rotation % len(encrypted_text)
    text = encrypted_text[rotation:] + encrypted_text[:rotation]

    return text

print(solution(	"qyyigoptvfb", "abcdefghijk", 3))
