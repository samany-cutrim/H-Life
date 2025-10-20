import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:hive_flutter/hive_flutter.dart';

import '../../core/storage/hive_manager.dart';

class HydrationState {
  const HydrationState({required this.goalMl, required this.currentMl, required this.history});

  final int goalMl;
  final int currentMl;
  final List<int> history;

  HydrationState copyWith({int? goalMl, int? currentMl, List<int>? history}) {
    return HydrationState(
      goalMl: goalMl ?? this.goalMl,
      currentMl: currentMl ?? this.currentMl,
      history: history ?? this.history,
    );
  }
}

class HydrationNotifier extends StateNotifier<HydrationState> {
  HydrationNotifier()
      : super(const HydrationState(goalMl: 2500, currentMl: 0, history: [])) {
    _hydrate();
  }

  Future<void> _hydrate() async {
    final box = Hive.box(HiveManager.hydrationBox);
    final stored = box.get('data') as Map<dynamic, dynamic>?;
    if (stored != null) {
      state = HydrationState(
        goalMl: stored['goal'] as int? ?? 2500,
        currentMl: stored['current'] as int? ?? 0,
        history: (stored['history'] as List<dynamic>? ?? []).cast<int>(),
      );
    }
  }

  void addWater(int ml) {
    final updated = (state.currentMl + ml).clamp(0, 5000);
    final history = [...state.history, updated];
    state = state.copyWith(currentMl: updated, history: history);
    _persist();
  }

  void updateGoal(int ml) {
    state = state.copyWith(goalMl: ml);
    _persist();
  }

  void _persist() {
    final box = Hive.box(HiveManager.hydrationBox);
    box.put('data', {
      'goal': state.goalMl,
      'current': state.currentMl,
      'history': state.history,
    });
  }
}

final hydrationProvider = StateNotifierProvider<HydrationNotifier, HydrationState>((ref) {
  return HydrationNotifier();
});

class HydrationScreen extends ConsumerWidget {
  const HydrationScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final hydration = ref.watch(hydrationProvider);
    final notifier = ref.read(hydrationProvider.notifier);
    final progress = hydration.currentMl / hydration.goalMl;

    return Scaffold(
      appBar: AppBar(title: const Text('Hidratação')), 
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Card(
              child: Padding(
                padding: const EdgeInsets.all(16),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text('Meta diária: ${hydration.goalMl} mL'),
                    const SizedBox(height: 8),
                    LinearProgressIndicator(value: progress.clamp(0.0, 1.0)),
                    const SizedBox(height: 8),
                    Text('Consumido: ${hydration.currentMl} mL'),
                    Slider(
                      value: hydration.goalMl.toDouble(),
                      min: 1500,
                      max: 4000,
                      divisions: 10,
                      label: '${hydration.goalMl} mL',
                      onChanged: (value) => notifier.updateGoal(value.toInt()),
                    ),
                  ],
                ),
              ),
            ),
            Wrap(
              spacing: 16,
              children: [
                ElevatedButton.icon(
                  onPressed: () => notifier.addWater(200),
                  icon: const Icon(Icons.local_drink),
                  label: const Text('+200 mL'),
                ),
                ElevatedButton.icon(
                  onPressed: () => notifier.addWater(500),
                  icon: const Icon(Icons.bolt),
                  label: const Text('+500 mL'),
                ),
              ],
            ),
            const SizedBox(height: 16),
            const Text('Histórico'),
            Expanded(
              child: ListView.builder(
                itemCount: hydration.history.length,
                itemBuilder: (context, index) {
                  final value = hydration.history[index];
                  return ListTile(
                    leading: const Icon(Icons.water_drop),
                    title: Text('$value mL'),
                    subtitle: Text('Registro ${index + 1}'),
                  );
                },
              ),
            ),
          ],
        ),
      ),
    );
  }
}
