import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import 'app.dart';
import 'core/storage/hive_manager.dart';
import 'core/notifications/fcm_service.dart';

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await HiveManager.ensureInitialized();
  await FcmService.initialize();
  runApp(const ProviderScope(child: HLifeApp()));
}
