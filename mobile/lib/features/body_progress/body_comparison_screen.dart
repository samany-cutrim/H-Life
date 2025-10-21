import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import 'providers/body_progress_repository.dart';

class BodyComparisonScreen extends ConsumerStatefulWidget {
  const BodyComparisonScreen({super.key});

  @override
  ConsumerState<BodyComparisonScreen> createState() => _BodyComparisonScreenState();
}

class _BodyComparisonScreenState extends ConsumerState<BodyComparisonScreen> {
  String? _beforeId;
  String? _afterId;
  BodyView _view = BodyView.front;
  bool _loading = false;
  BodyAnalysisResult? _result;

  Future<void> _analyze() async {
    if (_beforeId == null || _afterId == null) return;
    setState(() => _loading = true);
    try {
      final repository = ref.read(bodyProgressRepositoryProvider);
      final analysis = await repository.analyzeComparison(
        beforeId: _beforeId!,
        afterId: _afterId!,
        view: _view,
      );
      if (!mounted) return;
      setState(() => _result = analysis);
    } catch (e) {
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('Erro na análise: $e')));
    } finally {
      if (mounted) setState(() => _loading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    final repository = ref.watch(bodyProgressRepositoryProvider);
    return Scaffold(
      appBar: AppBar(title: const Text('Comparação corporal')),
      body: FutureBuilder<List<Map<String, dynamic>>>(
        future: repository.listCaptures(),
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return const Center(child: CircularProgressIndicator());
          }
          final captures = snapshot.data ?? [];
          final views = captures.where((capture) => capture['view'] == _view.name).toList();
          if (captures.isEmpty) {
            return const Center(
              child: Padding(
                padding: EdgeInsets.all(32),
                child: Text('Nenhuma captura encontrada. Fotografe seu progresso primeiro.'),
              ),
            );
          }
          if (views.isEmpty) {
            return Center(
              child: Padding(
                padding: const EdgeInsets.all(32),
                child: Text('Sem capturas na vista ${_view.name}. Garanta a ordem Frente → Lado → Costas.'),
              ),
            );
          }
          return ListView(
            padding: const EdgeInsets.all(16),
            children: [
              DropdownButton<BodyView>(
                value: _view,
                items: BodyView.values
                    .map((view) => DropdownMenuItem(value: view, child: Text(view.name.toUpperCase())))
                    .toList(),
                onChanged: (value) => setState(() {
                  _view = value ?? BodyView.front;
                  _beforeId = null;
                  _afterId = null;
                }),
              ),
              Row(
                children: [
                  Expanded(
                    child: DropdownButton<String>(
                      value: _beforeId,
                      hint: const Text('Antes'),
                      items: views
                          .map((capture) => DropdownMenuItem(
                                value: capture['id'] as String?,
                                child: Text('${capture['captured_at']}'),
                              ))
                          .toList(),
                      onChanged: (value) => setState(() => _beforeId = value),
                    ),
                  ),
                  const SizedBox(width: 12),
                  Expanded(
                    child: DropdownButton<String>(
                      value: _afterId,
                      hint: const Text('Depois'),
                      items: views
                          .map((capture) => DropdownMenuItem(
                                value: capture['id'] as String?,
                                child: Text('${capture['captured_at']}'),
                              ))
                          .toList(),
                      onChanged: (value) => setState(() => _afterId = value),
                    ),
                  ),
                ],
              ),
              const SizedBox(height: 16),
              ElevatedButton.icon(
                onPressed: _loading ? null : _analyze,
                icon: const Icon(Icons.analytics),
                label: const Text('Analisar mudanças'),
              ),
              if (_loading) const LinearProgressIndicator(),
              if (_result != null) _BodyAnalysisResultCard(result: _result!),
            ],
          );
        },
      ),
    );
  }
}

class _BodyAnalysisResultCard extends StatefulWidget {
  const _BodyAnalysisResultCard({required this.result});

  final BodyAnalysisResult result;

  @override
  State<_BodyAnalysisResultCard> createState() => _BodyAnalysisResultCardState();
}

class _BodyAnalysisResultCardState extends State<_BodyAnalysisResultCard> {
  double _slider = 0.5;

  @override
  Widget build(BuildContext context) {
    return Card(
      margin: const EdgeInsets.only(top: 16),
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text('Veredito: ${widget.result.verdict}', style: Theme.of(context).textTheme.titleMedium),
            Text('Confiança: ${(widget.result.confidence * 100).toStringAsFixed(1)}%'),
            const SizedBox(height: 8),
            const Text('Variações percentuais:'),
            ...widget.result.metrics.entries.map(
              (entry) => Text('${entry.key}: ${entry.value.toStringAsFixed(2)}%'),
            ),
            const SizedBox(height: 16),
            SizedBox(
              height: 300,
              child: LayoutBuilder(
                builder: (context, constraints) {
                  return ClipRRect(
                    borderRadius: BorderRadius.circular(16),
                    child: Stack(
                      fit: StackFit.expand,
                      children: [
                        Positioned.fill(
                          child: Image.network(widget.result.beforeImageUrl, fit: BoxFit.cover),
                        ),
                        Positioned.fill(
                          child: FractionallySizedBox(
                            widthFactor: _slider,
                            alignment: Alignment.centerLeft,
                            child: Image.network(widget.result.afterImageUrl, fit: BoxFit.cover),
                          ),
                        ),
                        Positioned(
                          left: constraints.maxWidth * _slider,
                          top: 0,
                          bottom: 0,
                          child: Container(width: 2, color: Colors.white),
                        ),
                      ],
                    ),
                  );
                },
              ),
            ),
            Slider(
              value: _slider,
              onChanged: (value) => setState(() => _slider = value),
            ),
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: const [
                Text('Antes'),
                Text('Depois'),
              ],
            ),
          ],
        ),
      ),
    );
  }
}
