import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

class TrainingSession {
  const TrainingSession({
    required this.day,
    required this.modality,
    required this.focus,
    required this.videoUrl,
    this.completed = false,
    this.series = const [],
  });

  final String day;
  final String modality;
  final String focus;
  final String videoUrl;
  final bool completed;
  final List<String> series;

  TrainingSession copyWith({bool? completed, List<String>? series}) => TrainingSession(
        day: day,
        modality: modality,
        focus: focus,
        videoUrl: videoUrl,
        completed: completed ?? this.completed,
        series: series ?? this.series,
      );
}

class TrainingPlannerNotifier extends StateNotifier<List<TrainingSession>> {
  TrainingPlannerNotifier()
      : super(const [
          TrainingSession(
            day: 'Segunda',
            modality: 'Funcional em casa',
            focus: 'Full body',
            videoUrl: 'https://videos.app/treino1',
          ),
          TrainingSession(
            day: 'Quarta',
            modality: 'Academia',
            focus: 'Força — superiores',
            videoUrl: 'https://videos.app/treino2',
          ),
          TrainingSession(
            day: 'Sexta',
            modality: 'Rua',
            focus: 'HIIT 30 minutos',
            videoUrl: 'https://videos.app/treino3',
          ),
        ]);

  void toggleComplete(int index, {List<String>? series}) {
    state = [
      for (int i = 0; i < state.length; i++)
        if (i == index)
          state[i].copyWith(completed: !state[i].completed, series: series ?? state[i].series)
        else
          state[i],
    ];
  }
}

final trainingPlannerProvider =
    StateNotifierProvider<TrainingPlannerNotifier, List<TrainingSession>>((ref) {
  return TrainingPlannerNotifier();
});

final streakProvider = Provider<int>((ref) {
  final sessions = ref.watch(trainingPlannerProvider);
  return sessions.where((session) => session.completed).length;
});

class TrainingPlannerScreen extends ConsumerStatefulWidget {
  const TrainingPlannerScreen({super.key});

  @override
  ConsumerState<TrainingPlannerScreen> createState() => _TrainingPlannerScreenState();
}

class _TrainingPlannerScreenState extends ConsumerState<TrainingPlannerScreen> {
  final TextEditingController _seriesController = TextEditingController();
  final TextEditingController _rpeController = TextEditingController();

  @override
  void dispose() {
    _seriesController.dispose();
    _rpeController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final sessions = ref.watch(trainingPlannerProvider);
    final streak = ref.watch(streakProvider);

    return Scaffold(
      appBar: AppBar(title: const Text('Treinos e Planner semanal')),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          Card(
            child: ListTile(
              leading: const Icon(Icons.emoji_events_outlined),
              title: Text('Streak de treinos: $streak'),
              subtitle: Text('XP total: ${streak * 50}'),
            ),
          ),
          ...sessions.asMap().entries.map((entry) {
            final index = entry.key;
            final session = entry.value;
            return Card(
              child: ExpansionTile(
                title: Text('${session.day} — ${session.modality}'),
                subtitle: Text(session.focus),
                trailing: IconButton(
                  icon: Icon(session.completed ? Icons.check_circle : Icons.radio_button_unchecked,
                      color: session.completed ? Colors.green : null),
                  onPressed: () => ref.read(trainingPlannerProvider.notifier).toggleComplete(index),
                ),
                children: [
                  ListTile(
                    leading: const Icon(Icons.play_circle_fill),
                    title: const Text('Assistir demonstração'),
                    subtitle: Text(session.videoUrl),
                    onTap: () {},
                  ),
                  Padding(
                    padding: const EdgeInsets.all(16.0),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        TextField(
                          controller: _seriesController,
                          decoration: const InputDecoration(labelText: 'Séries / repetições executadas'),
                        ),
                        const SizedBox(height: 8),
                        TextField(
                          controller: _rpeController,
                          decoration: const InputDecoration(labelText: 'RPE (esforço percebido)'),
                          keyboardType: TextInputType.number,
                        ),
                        const SizedBox(height: 8),
                        ElevatedButton(
                          onPressed: () {
                            ref.read(trainingPlannerProvider.notifier).toggleComplete(
                                  index,
                                  series: [
                                    'Séries: ${_seriesController.text}',
                                    'RPE: ${_rpeController.text}',
                                  ],
                                );
                          },
                          child: const Text('Salvar registro'),
                        ),
                        if (session.series.isNotEmpty)
                          Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: session.series.map(Text.new).toList(),
                          ),
                      ],
                    ),
                  ),
                ],
              ),
            );
          }),
        ],
      ),
    );
  }
}
