# AIOS

**AIOS** is an experimental project: treat the operating system as something that *reasons* about what you want, instead of only executing commands you already know how to type.

This repository is the starting point for that idea. It is **not** a finished operating system and it does **not** replace the Linux kernel.

## What this is (and is not)

| Claim | Reality |
| --- | --- |
| "Replace Linux inside an Android emulator with an AI OS" | Not possible as a weekend drop-in. Android *is* Linux (kernel + userspace). Replacing the kernel means writing a new kernel that boots on the emulator's virtual hardware. That is a multi-year systems project. |
| "The OS itself is AI" | Useful as a *userspace* layer first: an agent that owns the shell, files, processes, and policy. Hardware, drivers, memory, and scheduling still need a real kernel. |
| Rooted Android emulator as a lab | Practical. Official Android Emulator AVDs without Google Play often already give `adb root`. Play-Store images need extra tools such as [AERoot](https://github.com/quarkslab/AERoot). |

We start where you can actually ship code: a **userspace AI OS layer** that runs on Linux (and later inside a rooted emulator / chroot / VM). Kernel work, if it ever happens, is a later phase — not a first commit.

## Lab: rooted Android emulator

Recommended path for experimentation:

1. Install [Android Studio](https://developer.android.com/studio) and create an AVD.
2. Prefer an image **without** Google Play ("Google APIs" or AOSP). Then:

   ```bash
   adb root
   adb shell
   # you should see uid=0(root)
   uname -a
   ```

3. If you need a Play Store image, look at [AERoot](https://github.com/quarkslab/AERoot) (gdb-based, emulator `-qemu -s`) or Magisk-style rooted system images. Those grant *root on Linux*, they do not replace Linux.
4. From a root shell you can inspect `/proc`, mount points, and the kernel version. You still cannot swap the running kernel for a custom "AI kernel" without building and booting a new image.

Other useful environments (often better than fighting the emulator):

- A normal Linux VM or WSL2 — best place to develop AIOS userspace.
- [Waydroid](https://waydro.id/) — Android userspace on a Linux desktop kernel.
- QEMU with a custom kernel — the real path if you ever boot your own kernel.

## Architecture (phased)

```
Phase 0  AIOS shell     ← you are here
         natural-language intent → tools (fs, process, net)
         runs as a process on Linux / adb shell

Phase 1  AIOS supervisor
         persistent session, policy, memory, sandboxed tools

Phase 2  Guest userspace
         AIOS as PID 1 *inside* a container or VM (still Linux kernel)

Phase 3  Research kernel (optional, far future)
         custom kernel or unikernel; not required to use AIOS
```

Replacing Linux is Phase 3. Shipping something you can run is Phase 0–1.

## Quick start

Requires Python 3.10+.

```bash
cd userspace
python3 -m aios
```

Type English. Examples:

- `where am i`
- `list files`
- `run echo hello from aios`
- `remember that this machine is the lab box`
- `what do you remember`

This is a local, offline prototype. No cloud model is required for the built-in intent parser. You can later plug in an LLM backend.

## Repo layout

```
userspace/     Phase 0 AIOS shell
docs/          emulator notes and design
```

## Safety

AIOS must never silently become root, rewrite `/system` or `/`, or install a kernel. The prototype runs as the current user and only executes an allowlisted set of tools. Treat any future "replace the OS" work as research, not a rootkit.

## License

MIT — see `LICENSE`.
