import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import 'core/app_router.dart';
import 'core/theme/app_theme.dart';

class HLifeApp extends ConsumerWidget {
  const HLifeApp({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final router = ref.watch(appRouterProvider);
    return MaterialApp.router(
      title: 'H-Life',
      theme: buildAppTheme(),
      routerConfig: router,
    );
  }
}
