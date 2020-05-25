# Getting Started with mobile app development

Currently only Android is supported.

First make sure you have installed Android Studio with Android SDK. You also need to
install the Ionic Framework (using Capactior in this project instead of Cordova).

After making code changes:
```bash
ionic build
```

To open the app project in Android Studio (to run, deploy, etc.):
```bash
npx cap open android
```

After building you also need to sync the app with Capacitor:
```bash
npx cap copy
```

To run a simple dev server:
```bash
npx cap serve
```
or
```bash
ionic serve
```

To run in a watch-mode in Android:
```bash
ionic capacitor run android -l
```