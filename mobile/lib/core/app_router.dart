import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import '../features/onboarding/onboarding_screen.dart';
import '../features/home/home_screen.dart';
import '../features/diet/diet_screen.dart';
import '../features/shopping/shopping_list_screen.dart';
import '../features/training/training_planner_screen.dart';
import '../features/hydration/hydration_screen.dart';
import '../features/bioimpedance/bioimpedance_screen.dart';
import '../features/reports/reports_screen.dart';
import '../features/chat/chat_screen.dart';
import '../features/body_progress/body_capture_screen.dart';
import '../features/body_progress/body_comparison_screen.dart';

final _rootNavigatorKey = GlobalKey<NavigatorState>();

final appRouterProvider = Provider<GoRouter>((ref) {
  return GoRouter(
    navigatorKey: _rootNavigatorKey,
    initialLocation: '/onboarding',
    routes: [
      GoRoute(
        path: '/onboarding',
        builder: (context, state) => const OnboardingScreen(),
      ),
      ShellRoute(
        builder: (context, state, child) => HomeScaffold(child: child),
        routes: [
          GoRoute(
            path: '/home',
            builder: (context, state) => const HomeScreen(),
          ),
          GoRoute(
            path: '/diet',
            builder: (context, state) => const DietScreen(),
          ),
          GoRoute(
            path: '/shopping',
            builder: (context, state) => const ShoppingListScreen(),
          ),
          GoRoute(
            path: '/training',
            builder: (context, state) => const TrainingPlannerScreen(),
          ),
          GoRoute(
            path: '/hydration',
            builder: (context, state) => const HydrationScreen(),
          ),
          GoRoute(
            path: '/bioimpedance',
            builder: (context, state) => const BioimpedanceScreen(),
          ),
          GoRoute(
            path: '/reports',
            builder: (context, state) => const ReportsScreen(),
          ),
          GoRoute(
            path: '/chat',
            builder: (context, state) => const ChatScreen(),
          ),
          GoRoute(
            path: '/body/capture',
            builder: (context, state) => const BodyCaptureScreen(),
          ),
          GoRoute(
            path: '/body/comparison',
            builder: (context, state) => const BodyComparisonScreen(),
          ),
        ],
      ),
    ],
    redirect: (context, state) {
      if (state.matchedLocation == '/onboarding') {
        return null;
      }
      return null;
    },
  );
});

class HomeScaffold extends StatelessWidget {
  const HomeScaffold({required this.child, super.key});

  final Widget child;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: child,
      bottomNavigationBar: NavigationBar(
        selectedIndex: _indexFromLocation(GoRouter.of(context).location),
        onDestinationSelected: (index) {
          final router = GoRouter.of(context);
          switch (index) {
            case 0:
              router.go('/home');
              break;
            case 1:
              router.go('/diet');
              break;
            case 2:
              router.go('/training');
              break;
            case 3:
              router.go('/hydration');
              break;
            default:
              router.go('/home');
          }
        },
        destinations: const [
          NavigationDestination(icon: Icon(Icons.dashboard_outlined), label: 'Início'),
          NavigationDestination(icon: Icon(Icons.restaurant_menu), label: 'Dieta'),
          NavigationDestination(icon: Icon(Icons.fitness_center), label: 'Treino'),
          NavigationDestination(icon: Icon(Icons.water_drop), label: 'Hidratação'),
        ],
      ),
    );
  }

  int _indexFromLocation(String location) {
    if (location.startsWith('/diet')) return 1;
    if (location.startsWith('/training')) return 2;
    if (location.startsWith('/hydration')) return 3;
    return 0;
  }
}
