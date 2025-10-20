import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

class HomeScreen extends ConsumerWidget {
  const HomeScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('H-Life'),
        actions: [
          IconButton(
            icon: const Icon(Icons.camera_alt_outlined),
            onPressed: () => GoRouter.of(context).push('/body/capture'),
          ),
          IconButton(
            icon: const Icon(Icons.compare_arrows_outlined),
            onPressed: () => GoRouter.of(context).push('/body/comparison'),
          )
        ],
      ),
      body: ListView(
        padding: const EdgeInsets.symmetric(vertical: 16),
        children: const [
          _HomeCard(
            title: 'Dieta do dia',
            subtitle: 'Refeições planejadas e macros',
            icon: Icons.restaurant_menu,
            route: '/diet',
          ),
          _HomeCard(
            title: 'Lista de compras',
            subtitle: 'Quantidades exatas e substitutos',
            icon: Icons.shopping_bag_outlined,
            route: '/shopping',
          ),
          _HomeCard(
            title: 'Treino de hoje',
            subtitle: 'Finalize e marque seu check-in',
            icon: Icons.fitness_center,
            route: '/training',
          ),
          _HomeCard(
            title: 'Água',
            subtitle: 'Acompanhe sua meta de hidratação',
            icon: Icons.water_drop,
            route: '/hydration',
          ),
          _HomeCard(
            title: 'Lembretes',
            subtitle: 'Alertas de laudos, relatórios e compras',
            icon: Icons.notifications,
            route: '/reports',
          ),
          _HomeCard(
            title: 'Bioimpedância',
            subtitle: 'Veja gráficos evolutivos e tendências',
            icon: Icons.monitor_weight_outlined,
            route: '/bioimpedance',
          ),
          _HomeCard(
            title: 'Chat IA',
            subtitle: 'Converse por voz, texto ou imagem',
            icon: Icons.smart_toy_outlined,
            route: '/chat',
          ),
        ],
      ),
    );
  }
}

class _HomeCard extends StatelessWidget {
  const _HomeCard({
    required this.title,
    required this.subtitle,
    required this.icon,
    required this.route,
  });

  final String title;
  final String subtitle;
  final IconData icon;
  final String route;

  @override
  Widget build(BuildContext context) {
    return Card(
      child: ListTile(
        leading: Icon(icon, size: 40),
        title: Text(title, style: Theme.of(context).textTheme.titleMedium),
        subtitle: Text(subtitle),
        trailing: const Icon(Icons.chevron_right),
        onTap: () => GoRouter.of(context).push(route),
      ),
    );
  }
}
