# FreeOTP configuration exporter
Exports configuration from [FreeOTP Authenticator for Android](https://freeotp.github.io/) in the form of plaintext [OTP URIs](https://github.com/google/google-authenticator/wiki/Key-Uri-Format). Configurations can either be exported from an unencrypted backup (`adb backup`) or directly from the phone. In latter case the script just invokes `adb backup` itself.


## Usage
**Note:** `adb` must be installed to obtain backups from an Android device. Also, [*USB Debugging* must be enabled](https://stackoverflow.com/a/16707351) on the device.

- Connect your device via USB and unlock it.
- Run `./freeotp-export.py`.
- Confirm the backup dialog on your device. Do not enter a passphrase.
- The OTP URIs are printed to stdout.


## License
The source code is distributed under the Boost Software License, Version 1.0.
