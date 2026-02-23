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

## 📚 Resources
* **Official Course Site:** [6.1600 MIT](https://61600.csail.mit.edu/2024/)
* **Lab Instructions:** [Documentation](./docs)
---

