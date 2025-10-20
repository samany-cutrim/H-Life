import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

class ShoppingItem {
  ShoppingItem({
    required this.name,
    required this.quantity,
    required this.unit,
    required this.substitutes,
    this.purchased = false,
  });

  final String name;
  final double quantity;
  final String unit;
  final List<String> substitutes;
  final bool purchased;

  ShoppingItem copyWith({bool? purchased}) => ShoppingItem(
        name: name,
        quantity: quantity,
        unit: unit,
        substitutes: substitutes,
        purchased: purchased ?? this.purchased,
      );
}

class ShoppingListNotifier extends StateNotifier<List<ShoppingItem>> {
  ShoppingListNotifier()
      : super([
          ShoppingItem(
            name: 'Peito de frango',
            quantity: 1.5,
            unit: 'kg',
            substitutes: const ['Sobrecoxa sem pele', 'Tofu firme'],
          ),
          ShoppingItem(
            name: 'Quinoa',
            quantity: 500,
            unit: 'g',
            substitutes: const ['Arroz integral', 'Trigo sarraceno'],
          ),
          ShoppingItem(
            name: 'Iogurte grego',
            quantity: 6,
            unit: 'unid',
            substitutes: const ['Skyr', 'Iogurte natural desnatado'],
          ),
        ]);

  void togglePurchased(int index) {
    state = [
      for (int i = 0; i < state.length; i++)
        if (i == index)
          state[i].copyWith(purchased: !state[i].purchased)
        else
          state[i],
    ];
  }
}

final shoppingListProvider = StateNotifierProvider<ShoppingListNotifier, List<ShoppingItem>>(
  (ref) => ShoppingListNotifier(),
);

class ShoppingListScreen extends ConsumerWidget {
  const ShoppingListScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final items = ref.watch(shoppingListProvider);
    return Scaffold(
      appBar: AppBar(title: const Text('Lista de compras')),
      body: ListView.builder(
        itemCount: items.length,
        itemBuilder: (context, index) {
          final item = items[index];
          return Card(
            child: ExpansionTile(
              title: Text('${item.name} — ${item.quantity} ${item.unit}'),
              leading: Checkbox(
                value: item.purchased,
                onChanged: (_) => ref.read(shoppingListProvider.notifier).togglePurchased(index),
              ),
              children: [
                const ListTile(title: Text('Substitutos')),
                ...item.substitutes.map(
                  (substitute) => ListTile(
                    leading: const Icon(Icons.sync_alt),
                    title: Text(substitute),
                    subtitle: const Text('Alternativa equivalente'),
                  ),
                ),
              ],
            ),
          );
        },
      ),
    );
  }
}
