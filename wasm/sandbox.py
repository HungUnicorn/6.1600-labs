import pywasm
import wasi

def sha256(v):
    wasimod = wasi.Wasi(['sha-export.wasm'])
    runtime = pywasm.load('sha-export.wasm', { 'wasi_snapshot_preview1': wasimod.imports() })

    in_ptr = runtime.exec('malloc', [len(v)])
    out_ptr = runtime.exec('malloc', [32])

    runtime.store.memory_list[0].data[in_ptr: in_ptr + len(v)] = v
    runtime.exec('SHA256', [in_ptr, len(v), out_ptr])

    hash_result = runtime.store.memory_list[0].data[out_ptr: out_ptr + 32]

    return bytes(hash_result)
