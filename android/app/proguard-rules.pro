# Default ProGuard rules for the Chipsoft Tech2 emulator app.
# Keep the UDS classes since they're invoked reflectively from tests / future
# scripts, and the seed-to-key constants must not be obfuscated.
-keep class com.example.chipsoft_tech2.uds.** { *; }
-keep class com.example.chipsoft_tech2.crypto.** { *; }
