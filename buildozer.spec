[app]

# ── App Identity ──────────────────────────────────────────────────────────────
title = HealthAI
package.name = healthai
package.domain = org.healthai

# ── Source ────────────────────────────────────────────────────────────────────
source.dir = .
source.include_exts = py,png,jpg,jpeg,kv,atlas,pkl,ttf,otf,json
source.include_patterns = assets/*,models/*.pkl,data/*,screens/*,utils/*

# ── Version ───────────────────────────────────────────────────────────────────
version = 1.0.0

# ── Python / Kivy Requirements ────────────────────────────────────────────────
# NOTE: on Android, use the p4a-friendly names.
# scikit-learn is available via the kivy-garden or as a p4a recipe.
requirements = python3,kivy==2.2.1,numpy,scikit-learn,joblib

# ── Orientation & UI ─────────────────────────────────────────────────────────
orientation = portrait
fullscreen = 0

# ── Android Settings ─────────────────────────────────────────────────────────
android.permissions = INTERNET,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE
android.api = 33
android.minapi = 24
android.ndk = 25b
android.sdk = 33
android.ndk_api = 24
android.accept_sdk_license = True

# Use the latest stable p4a
android.branch = master

# Gradle / build
android.gradle_dependencies =
android.add_aars =
android.add_jars =

# Architecture (include both for wider device coverage)
android.archs = arm64-v8a, armeabi-v7a

# Allow backup
android.allow_backup = True

# ── Icons & Splash ────────────────────────────────────────────────────────────
# Uncomment when you have these assets:
# icon.filename = %(source.dir)s/assets/icon.png
# presplash.filename = %(source.dir)s/assets/presplash.png

# ── Log / Debug ───────────────────────────────────────────────────────────────
android.logcat_filters = *:S python:D

# ── Build Dir ────────────────────────────────────────────────────────────────
# buildozer uses .buildozer/ inside source.dir by default

[buildozer]

# Log level: 0 = error only, 1 = info, 2 = debug (default: 1)
log_level = 2

# Warn when the buildozer home directory is in the source directory
warn_on_root_element = 1
