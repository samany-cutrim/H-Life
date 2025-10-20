import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

class ReportItem {
  const ReportItem(this.title, this.subtitle, this.type);

  final String title;
  final String subtitle;
  final String type;
}

final reportsProvider = Provider<List<ReportItem>>((ref) {
  return const [
    ReportItem('Laudo de bioimpedância', '10/10/2023', 'PDF'),
    ReportItem('Relatório mensal de dieta', '30/09/2023', 'PDF'),
    ReportItem('Laudo endocrinologista', '20/08/2023', 'OCR'),
  ];
});

class ReportsScreen extends ConsumerWidget {
  const ReportsScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final items = ref.watch(reportsProvider);
    return Scaffold(
      appBar: AppBar(title: const Text('Laudos e Relatórios')),
      floatingActionButton: FloatingActionButton.extended(
        onPressed: () {},
        icon: const Icon(Icons.file_upload),
        label: const Text('Upload / OCR'),
      ),
      body: ListView.builder(
        itemCount: items.length,
        itemBuilder: (context, index) {
          final item = items[index];
          return Card(
            child: ListTile(
              leading: Icon(item.type == 'OCR' ? Icons.document_scanner : Icons.picture_as_pdf),
              title: Text(item.title),
              subtitle: Text(item.subtitle),
              trailing: IconButton(
                icon: const Icon(Icons.download),
                onPressed: () {},
              ),
            ),
          );
        },
      ),
    );
  }
}
