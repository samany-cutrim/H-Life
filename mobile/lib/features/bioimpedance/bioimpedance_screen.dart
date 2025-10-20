import 'package:fl_chart/fl_chart.dart';
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

class BioimpedanceEntry {
  const BioimpedanceEntry(this.date, this.bodyFat, this.muscleMass);

  final DateTime date;
  final double bodyFat;
  final double muscleMass;
}

final bioimpedanceProvider = Provider<List<BioimpedanceEntry>>((ref) {
  return [
    BioimpedanceEntry(DateTime.now().subtract(const Duration(days: 90)), 24.0, 32.5),
    BioimpedanceEntry(DateTime.now().subtract(const Duration(days: 60)), 22.5, 33.1),
    BioimpedanceEntry(DateTime.now().subtract(const Duration(days: 30)), 21.9, 33.8),
    BioimpedanceEntry(DateTime.now(), 21.2, 34.2),
  ];
});

class BioimpedanceScreen extends ConsumerWidget {
  const BioimpedanceScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final entries = ref.watch(bioimpedanceProvider);
    return Scaffold(
      appBar: AppBar(title: const Text('Bioimpedância')),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          children: [
            Expanded(
              child: LineChart(
                LineChartData(
                  gridData: const FlGridData(show: true),
                  titlesData: FlTitlesData(
                    bottomTitles: AxisTitles(
                      sideTitles: SideTitles(
                        showTitles: true,
                        getTitlesWidget: (value, meta) {
                          final index = value.toInt();
                          if (index < 0 || index >= entries.length) {
                            return const SizedBox.shrink();
                          }
                          final entry = entries[index];
                          return Text('${entry.date.month}/${entry.date.year % 100}');
                        },
                      ),
                    ),
                    leftTitles: AxisTitles(
                      sideTitles: SideTitles(showTitles: true, reservedSize: 40),
                    ),
                  ),
                  lineBarsData: [
                    LineChartBarData(
                      spots: [
                        for (int i = 0; i < entries.length; i++)
                          FlSpot(i.toDouble(), entries[i].bodyFat),
                      ],
                      isCurved: true,
                      color: Colors.redAccent,
                      barWidth: 3,
                      dotData: const FlDotData(show: true),
                    ),
                    LineChartBarData(
                      spots: [
                        for (int i = 0; i < entries.length; i++)
                          FlSpot(i.toDouble(), entries[i].muscleMass),
                      ],
                      isCurved: true,
                      color: Colors.green,
                      barWidth: 3,
                      dotData: const FlDotData(show: true),
                    ),
                  ],
                  lineTouchData: LineTouchData(
                    touchTooltipData: LineTouchTooltipData(
                      tooltipBgColor: Colors.black.withOpacity(0.7),
                      getTooltipItems: (items) {
                        return items.map((item) {
                          final entry = entries[item.spotIndex];
                          return LineTooltipItem(
                            '${entry.date.day}/${entry.date.month}\n'
                            'Gordura: ${entry.bodyFat.toStringAsFixed(1)}%\n'
                            'Massa magra: ${entry.muscleMass.toStringAsFixed(1)} kg',
                            const TextStyle(color: Colors.white),
                          );
                        }).toList();
                      },
                    ),
                  ),
                ),
              ),
            ),
            const SizedBox(height: 16),
            ElevatedButton.icon(
              onPressed: () {},
              icon: const Icon(Icons.add_chart),
              label: const Text('Registrar nova avaliação'),
            ),
          ],
        ),
      ),
    );
  }
}
