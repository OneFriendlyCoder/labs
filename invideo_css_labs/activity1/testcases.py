from cryptography.fernet import Fernet
import json

tests = [
    (1, ".hero-inner - max-width", ".hero-inner", "max-width", ["var(--site-width)", "1200px"]),
    (2, ".hero-inner - margin", ".hero-inner", "margin", ["0 auto", "0px auto", "auto"]),
    (3, ".hero-inner - padding", ".hero-inner", "padding", ["0 20px", "0px 20px"]),
    (4, ".hero-inner - display", ".hero-inner", "display", ["flex"]),
    (5, ".hero-inner - align-items", ".hero-inner", "align-items", ["center", "flex-start"]),
    (6, ".hero-inner - justify-content", ".hero-inner", "justify-content", ["space-between"]),
    (7, ".hero-inner - gap", ".hero-inner", "gap", ["12px"]),
    (8, ".site-header - display", ".site-header", "display", ["flex"]),
    (9, ".site-header - align-items", ".site-header", "align-items", ["center"]),
    (10, ".site-header - justify-content", ".site-header", "justify-content", ["space-between"]),
    (11, ".site-header - gap", ".site-header", "gap", ["12px"]),
    (12, ".filters - display", ".filters", "display", ["flex"]),
    (13, ".filters - gap", ".filters", "gap", ["12px"]),
    (14, ".filters - align-items", ".filters", "align-items", ["center", "stretch"]),
    (15, ".filters - margin", ".filters", "margin", ["18px 0", "18px 0px"]),
    (16, ".filters - flex-wrap", ".filters", "flex-wrap", ["wrap"]),
]

key = Fernet.generate_key()
print("Your AUTOGRADER_KEY:", key.decode())

f = Fernet(key)
encrypted = f.encrypt(json.dumps(tests).encode())
print("Encrypted blob:\n", encrypted.decode())
