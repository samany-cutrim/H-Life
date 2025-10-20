import 'package:hive_flutter/hive_flutter.dart';

class HiveManager {
  static const hydrationBox = 'hydration';
  static const onboardingBox = 'onboarding';

  static Future<void> ensureInitialized() async {
    await Hive.initFlutter();
    await Hive.openBox(hydrationBox);
    await Hive.openBox(onboardingBox);
  }
}
