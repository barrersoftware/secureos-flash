# Attributions and Third-Party Software

## Heimdall

This project integrates with Heimdall, an open-source tool for flashing Samsung devices.

- **Project:** Heimdall
- **Author:** Benjamin Dobell, Glass Echidna
- **License:** MIT License
- **Repository:** https://github.com/Benjamin-Dobell/Heimdall
- **Copyright:** Copyright (c) 2010-2017 Benjamin Dobell, Glass Echidna

Heimdall is used via subprocess calls. We do not distribute Heimdall binaries.
Users must install Heimdall separately from its official sources.

## Trademarks

This software mentions various trademarks owned by their respective companies:

- **Samsung** - Samsung Electronics Co., Ltd.
- **Google**, **Android**, **Pixel** - Google LLC
- **Qualcomm**, **Snapdragon** - Qualcomm Technologies, Inc.
- **MediaTek** - MediaTek Inc.
- **LineageOS** - The LineageOS Project
- **GrapheneOS** - GrapheneOS Project

These trademarks are mentioned only for compatibility and informational purposes.
SecureOS Flash is an independent project not affiliated with, endorsed by, or
sponsored by any of these companies.

## Open Source Components

SecureOS Flash is built using:

- **Python** - Python Software Foundation License
- **libusb** (via Heimdall) - GNU LGPL 2.1

## Protocol Information

The Samsung flash protocol (Odin 3 protocol) implementation is based on the
reverse-engineered protocol documentation from the Heimdall project. We do not
claim any ownership of the protocol itself.

## Disclaimer

SecureOS Flash is provided "as is" without warranty of any kind. Flashing
devices carries inherent risks. Users are responsible for any consequences
of using this software.

---

If you believe any attribution is missing or incorrect, please open an issue
at https://github.com/barrersoftware/secureos-flash/issues
