# MIT 6.1600: Foundations of Computer Security — Lab Solutions

This repository contains my personal solutions for the labs in **MIT 6.1600 (Foundations of Computer Security)**.
6.1600 is an undergraduate course at MIT focused on the design of secure systems.

While some labs include built-in verification, others do not. For labs lacking official test suites, this repository provides custom validation scripts. Look for files named grader.py to verify the solutions.

## 📚 Resources
* **Official Course Site:** [6.1600 MIT](https://61600.csail.mit.edu/2024/)
* **Lab Instructions:** [Documentation](./docs)

## 🚀 Lab Overview

### [Lab 0: Hashing](./hash)
This lab explores the properties of cryptographic hash functions and various attack vectors.
* Dictionary attacks
* Multi-Target Preimage Attacks: Leveraging the Birthday Paradox to find a preimage among $2^{24}$ unsalted hashes using a toy 48-bit SHA-256 variant.
* Collision Finding Implementing: **Floyd’s Cycle-Finding Algorithm** (Tortoise and Hare) to find hash collisions in $O(\sqrt{N})$ time with $O(1)$ memory, specifically targeting a 56-bit hash space.

### [Lab 1: Merkle trees](./merkle)
This lab explores the implementation of authenticated key-value stores and vulnerabilities arising from improper structural validation.

* **Path & Depth Manipulation:** Exploiting clients that fail to enforce fixed-depth traversal, allowing short-circuit proofs to misrepresent the tree's state by stopping the hash calculation before reaching the leaf level.
* **Type Confusion Attacks:** Leveraging identical hash constructions for leaf nodes $`H_{kv}(k, v)`$ and internal nodes $$H_{kv}(k, v) = H_{int}(L, R)$$ to trick the client into "promoting" a branch hash into a data leaf. This highlights the necessity of cryptographic domain separation.

### [Lab 2: Bad Randomness](./bad-random)
This lab explores the failures resulting from reused randomness yand the lack of cryptographic integrity in early wireless protocols.
* **ECDSA Nonce Reuse**: Recovering a private key by exploiting the reuse of the secret nonce across two distinct signatures. By canceling out the nonce in the modular system, the private key $d$ is isolated, demonstrating that "random" values must never be predictable or repeated.
* **WEP Keystream Recovery**: Forging packets by recovering the RC4 keystream $K$ when both a message $M$ and its ciphertext $C$ are intercepted. Because $C = (M \parallel \text{CRC}(M)) \oplus K$, an attacker can extract $K$ to encrypt any arbitrary payload.
* **CRC32 Bit-Flipping**: Leveraging the mathematical linearity of RC4 and CRC32. An attacker applies a bit-mask $L = \Delta M \parallel \text{CRC}(\Delta M)$ to modify encrypted traffic without knowing the key or plaintext, as the modified checksum remains valid.

### [Lab 3: Timing](./timing)
This lab explores how minute differences in execution time can leak secret information, even when the data itself remains encrypted or inaccessible.
* **Remote Timing Side-Channel**: Exploding an "early-exit" password comparison vulnerability. By measuring the server's response time, the attacker identifies which character causes the longest delay, allowing for recovery of the password.

### [Lab 3: SSH](./ssh)
This lab explores the failures resulting from reused randomness yand the lack of cryptographic integrity in early wireless protocols.
* **Confidentiality Analysis**: Exploiting the deterministic nature of encryption when combined with compression. By observing the changes in packet lengths during the SSH handshake and data transfer, an attacker can infer the length of a secret without needing to decrypt the payload. This demonstrates that encryption alone does not hide metadata.
* **Bit-Flipping & Integrity**: Executing attack against a "None-MAC" SSH configuration. An attacker can XOR the ciphertext with a calculated bit-mask: $`C_{new} = C_{old} \oplus P_{old} \oplus P_{new}`$ This allows for the surgical replacement of the command `ls ./files/*\n` with `rm -r /      \n`.

### [Lab 4: Python Introspection](./escape)
Exploiting function closures, the call stack, global module mutability, and the garbage collector to recover "isolated" secrets through language-level reflection.

### [Lab 4: Sandbox Escapes](./wasm)
Bypassing WASI directory restrictions via symlinks and stale file descriptor invariants, and manually bridging memory boundaries to execute isolated C code.

### [Lab 5: Fuzzing & Codec Security](./fuzz)
This lab explores fuzzing and the design of serialization formats that remain secure against truncated or malicious data streams.

* **Buggy MsgPacker and Repair**: Inherited a flawed implementation of the MessagePack specification. It contained several "silent" bugs—errors that didn't always crash the program but caused data corruption or failed to decode valid MessagePack buffers. Developed a fuzzer that compared the inherited flawed implementation against the official, reference msgpack Python library Utilizing **Atheris** to perform stress testing on custom codecs.  The fuzzer identified numerous boundary condition errors (missing or extra = in comparison operators).
* **Robust Byte Codec**: Developed a "Punctuation-Hex" encoder mapping 4-bit nibbles to a unique 16-character punctuation alphabet ($L_{enc} \le 3 \cdot L_{raw}$). This design prevents "type confusion" and satisfies the Recoverability Rule through pessimistic parsing, ensuring truncated buffers decode only to valid prefixes without generating garbage data.
---
