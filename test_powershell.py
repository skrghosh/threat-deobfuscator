from deobfuscator import powershell

if __name__ == "__main__":
    with open("samples/obf_test.ps1") as f:
        code = f.read()

    cleaned = powershell.deobfuscate(code)
    print("Deobfuscated Script:\n")
    print(cleaned)
