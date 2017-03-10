# FreeOTP configuration exporter
Exports configuration from [FreeOTP Authenticator for Android](https://freeotp.github.io/) in the form of plaintext [OTP URIs](https://github.com/google/google-authenticator/wiki/Key-Uri-Format). Configurations can either be exported from an unencrypted backup (`adb backup`) or directly from the phone. In latter case the script just invokes `adb backup` itself.

**Note:** `adb` must be installed to obtain backups from an Android device. Also, [*USB Debugging* must be enabled](https://stackoverflow.com/a/16707351) on the device.


## License
The source code is distributed under the Boost Software License, Version 1.0.
