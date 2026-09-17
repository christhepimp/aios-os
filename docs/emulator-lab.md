# Rooted Android emulator lab

Goal: get a root shell on an Android emulator so you can inspect the Linux environment. That is research access. It is not a way to install a new kernel by editing files in place.

## Official emulator (best first step)

1. Install Android Studio / SDK emulator.
2. Create an AVD using a **Google APIs** or AOSP system image, not a **Google Play** image.
3. Start the AVD, then:

```bash
adb devices
adb root
adb shell id
adb shell uname -a
adb shell cat /proc/version
```

On non-Play images, `adbd` can restart as root. You now have Linux root *inside the guest*. The kernel is still the emulator's Android kernel.

## Play Store images

Play-protected images often block `adb root`. Community tools:

- [AERoot](https://github.com/quarkslab/AERoot) — attach gdb via `emulator @AVD -qemu -s`, then elevate a process or `adbd`.
- Older cousin: [android_emuroot](https://github.com/airbus-seclab/android_emuroot).

These patch process credentials in guest RAM. They do not give you a writable kernel source tree or a new OS.

## What you can do with root

- Read `/proc`, mounts, cgroups, SELinux state.
- Push the AIOS userspace prototype and run it under `adb shell`.
- Experiment with a chroot or proot Linux userspace *on top of* the same kernel.

## What you cannot do from that shell

- Delete Linux and boot "AIOS kernel" in its place without building a boot image the emulator will load.
- Replace `vmlinux` while the guest is running and expect a new OS.
- Treat Magisk/AERoot as an OS installer.

## If the real goal is a custom kernel

Use QEMU or the Android emulator's `-kernel` / custom system image flow:

1. Build a kernel for the virtual board (x86_64 or arm64 goldfish/ranchu).
2. Point the emulator or QEMU at that kernel + an initramfs.
3. Put AIOS userspace in the initramfs or rootfs, ideally as PID 1.

That is standard OS-dev, not "edit Linux until it becomes AI."
