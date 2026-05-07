import re
import os

path = r"c:\Users\Elitebook\Desktop\can-hacker\Chipsoft_RE\shim\cstech2win\src\forwarders.c"
with open(path, "r") as f:
    content = f.read()

# Replace __attribute__((naked)) with __declspec(naked)
content = content.replace("__attribute__((naked))", "__declspec(naked)")

# Replace __asm__ __volatile__ block with __asm { jmp [func] }
pattern = re.compile(r'__asm__\s*__volatile__\s*\(\s*"jmp\s*\*%0\\n"\s*:\s*:\s*"m"\s*\((g_real_[a-zA-Z0-9_]+)\)\s*\);')
content = pattern.sub(r'__asm { jmp dword ptr [\1] }', content)

with open(path, "w") as f:
    f.write(content)

print("forwarders.c patched for MSVC")
