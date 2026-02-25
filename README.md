# MIT 6.1600: Foundations of Computer Security — Lab Solutions

This repository contains my personal solutions for the labs in **MIT 6.1600 (Foundations of Computer Security)**.
6.1600 is an undergraduate course at MIT focused on the design of secure systems.

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

## 📚 Resources
* **Official Course Site:** [6.1600 MIT](https://61600.csail.mit.edu/2024/)
* **Lab Instructions:** [Documentation](./docs)
---
