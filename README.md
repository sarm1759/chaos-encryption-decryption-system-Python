# chaos-encryption-decryption-system-Python
Chaos-based encryption system using multiple chaotic maps (Logistic, Gompertz, Tent, Sine) using Python

# 🔐 Chaos-Based Encryption System

## 📌 Overview
This project implements a **chaos-based encryption system** using multiple chaotic maps:

- Logistic Map
- Gompertz Map
- Tent Map
- Sine Map

These maps are combined to generate a pseudo-random key used for encryption and decryption.

---

## ⚙️ Features

- Multi-chaotic key generation
- XOR-based encryption
- Agent key masking for secure key sharing
- CLI-based interface (easy to use)
- Full encryption & decryption pipeline

---

## 🧠 How It Works

1. User enters plain text
2. Chaotic parameters generate a random key
3. Key is masked using an agent key
4. Plain text is encrypted using XOR
5. Decryption reverses the same process

---

## ▶️ How to Run

```bash
python main.py
