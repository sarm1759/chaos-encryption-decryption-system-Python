import math

# ------------------ AGENT KEY ------------------
def generate_agent_key(u, xL, b, xG, y, xT, a, xS, length):
    temp = int(
        (u*1000 + xL*10000 + b*1000 + xG*10000 +
         y*1000 + xT*1000 + a*1000 + xS*10000) % 256
    )
    return [format(temp, "02X")] * length


# ------------------ KEY GENERATION ------------------
def generate_key(pTextLen, u, xL, b, xG, y, xT, a, xS):

    valL, valG, valT, valS = xL, xG, xT, xS
    vonOnLSB = []

    while len(vonOnLSB) < pTextLen:

        xnL, xnG, xnT, xnS = [], [], [], []
        LxorG, TxorS = [], []
        LG_LSB, TS_LSB = [], []

        for _ in range(pTextLen // 8):
            valL = u * valL * (1 - valL)
            xnL.append(int((valL * 1000) % 256))

        for _ in range(pTextLen // 8):
            valG = -b * valG * math.log(max(valG, 1e-10))
            xnG.append(int((valG * 1000) % 256))

        for i in range(len(xnL)):
            LxorG.append(xnL[i] ^ xnG[i])

        for _ in range(pTextLen // 8):
            if valT < 0.5:
                valT = y * valT
            else:
                valT = y * (1 - valT)
            xnT.append(int((valT * 1000) % 256))

        for _ in range(pTextLen // 8):
            valS = a * math.sin(math.pi * valS)
            xnS.append(int((valS * 1000) % 256))

        for i in range(len(xnT)):
            TxorS.append(xnT[i] ^ xnS[i])

        for i in range(len(LxorG)):
            LG_LSB.append(LxorG[i] & 1)
            TS_LSB.append(TxorS[i] & 1)

        for i in range(len(LG_LSB)):
            if LG_LSB[i] == 1 and TS_LSB[i] == 0:
                vonOnLSB.append(1)
            elif LG_LSB[i] == 0 and TS_LSB[i] == 1:
                vonOnLSB.append(0)

    vonOnLSB = vonOnLSB[:pTextLen]

    byte = []
    for i in range(0, len(vonOnLSB), 8):
        group = vonOnLSB[i:i+8]
        byte.append(int(''.join(map(str, group)), 2))

    hex_key = [format(b, "02X") for b in byte]

    return hex_key


# ------------------ ENCRYPT ------------------
def encrypt(pText, key, Ka_list):

    pT_hex = [format(ord(ch), "02X") for ch in pText]

    encrypt_pText = []
    for i in range(len(key)):
        val = int(key[i], 16) ^ int(pT_hex[i], 16)
        encrypt_pText.append(val)

    encrypted_text = ''.join(format(x, "02X") for x in encrypt_pText)

    enc_key = []
    for i in range(len(key)):
        enc_key.append(format(int(key[i],16) ^ int(Ka_list[i],16), "02X"))

    return ''.join(enc_key), encrypted_text


# ------------------ DECRYPT ------------------
def decrypt(eText, enc_key, Ka_list):

    key = []
    for i in range(0, len(enc_key), 2):
        val = int(enc_key[i:i+2], 16) ^ int(Ka_list[i//2], 16)
        key.append(format(val, "02X"))

    decrypted = ""
    for i in range(0, len(eText), 2):
        val = int(eText[i:i+2], 16) ^ int(key[i//2], 16)
        decrypted += chr(val)

    return decrypted


# ------------------ MAIN MENU ------------------
print("\n--> CHAOS ENCRYPTION SYSTEM <--\n")
print("Select an option:\n")
print("1. Encrypt Text")
print("2. Decrypt Text\n")

choice = input("Enter your choice (1 or 2): ")

# ------------------ ENCRYPTION ------------------
if choice == "1":

    print("\n--> ENCRYPTION PROCESS\n")

    pText = input("Enter Plain Text to encrypt:  ")
    pTextLen = len(pText) * 8

    print("\n--> Enter Chaotic Map Parameters (Use values within given ranges for best results) \n ")

    u = float(input("Logistic Map → μ (0 to 4): "))
    xL = float(input("Logistic Map → Initial X (0 to 1): "))

    b = float(input("Gompertz Map → b (0 to 2.7): "))
    xG = float(input("Gompertz Map → Initial X (0 to 1): "))

    y = float(input("Tent Map → γ (2 to 4): "))
    xT = float(input("Tent Map → Initial X (0 to 1): "))

    a = float(input("Sine Map → α (0 to 4): "))
    xS = float(input("Sine Map → Initial X (0 to 1): "))

    key = generate_key(pTextLen, u, xL, b, xG, y, xT, a, xS)

    # print("\nGenerated Secret Key:", ''.join(key)) ----  can show it too but just for clarification

    Ka_list = generate_agent_key(u, xL, b, xG, y, xT, a, xS, len(key))

    enc_key, encrypted_text = encrypt(pText, key, Ka_list)

    print("\nDecryption Key (Shared Securely):", enc_key)
    print("Final Encrypted Text:", encrypted_text)
    print()


# ------------------ DECRYPTION ------------------
elif choice == "2":

    print("\n--> DECRYPTION PROCESS\n")

    eText = input("Enter Encrypted Text:  ")
    enc_key = input("Enter Decryption Key:  ")

    print("\n--> Enter SAME parameters used during encryption\n")

    u = float(input("Logistic Map → μ: "))
    xL = float(input("Logistic Map → Initial X: "))
    b = float(input("Gompertz Map → b: "))
    xG = float(input("Gompertz Map → Initial X: "))
    y = float(input("Tent Map → γ: "))
    xT = float(input("Tent Map → Initial X: "))
    a = float(input("Sine Map → α: "))
    xS = float(input("Sine Map → Initial X: "))

    Ka_list = generate_agent_key(u, xL, b, xG, y, xT, a, xS, len(enc_key)//2)

    decrypted = decrypt(eText, enc_key, Ka_list)

    print("\nDecrypted Original Text: ", decrypted)


else:
    print("\n❌ Invalid option selected. Please run again.")