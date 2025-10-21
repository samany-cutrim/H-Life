import 'package:camera/camera.dart';
import 'package:dio/dio.dart';
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../core/network/dio_provider.dart';

final dietPlanProvider = Provider<List<String>>((ref) {
  return const [
    'Café da manhã: Omelete de claras, aveia, frutas vermelhas',
    'Almoço: Frango grelhado, quinoa, salada verde',
    'Lanche: Iogurte grego com castanhas',
    'Jantar: Salmão, legumes assados, batata doce',
  ];
});

final dietMacrosProvider = Provider<Map<String, int>>((ref) {
  return const {'calorias': 2200, 'carboidratos': 200, 'proteinas': 160, 'gorduras': 70};
});

class DietScreen extends ConsumerStatefulWidget {
  const DietScreen({super.key});

  @override
  ConsumerState<DietScreen> createState() => _DietScreenState();
}

class _DietScreenState extends ConsumerState<DietScreen> {
  CameraController? _cameraController;
  bool _isUploading = false;
  String? _analysis;

  @override
  void dispose() {
    _cameraController?.dispose();
    super.dispose();
  }

  Future<void> _openCamera() async {
    try {
      final cameras = await availableCameras();
      final camera = cameras.first;
      _cameraController = CameraController(camera, ResolutionPreset.medium);
      await _cameraController!.initialize();
      if (mounted) setState(() {});
    } catch (e) {
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('Erro ao abrir câmera: $e')));
    }
  }

  Future<void> _captureAndAnalyze() async {
    if (_cameraController == null || !_cameraController!.value.isInitialized) {
      await _openCamera();
    }
    if (!mounted || _cameraController == null) return;
    try {
      final picture = await _cameraController!.takePicture();
      final dio = ref.read(dioProvider);
      if (!mounted) return;
      setState(() => _isUploading = true);
      final response = await dio.post('/diet/analyze',
          data: FormData.fromMap({'photo': await MultipartFile.fromFile(picture.path)}));
      if (!mounted) return;
      setState(() => _analysis = response.data['analysis'] as String? ?? 'Sem retorno.');
    } catch (e) {
      if (!mounted) return;
      setState(() => _analysis = 'Erro ao analisar: $e');
    } finally {
      if (!mounted) return;
      setState(() => _isUploading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    final plan = ref.watch(dietPlanProvider);
    final macros = ref.watch(dietMacrosProvider);

    return Scaffold(
      appBar: AppBar(title: const Text('Plano alimentar')),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Card(
              child: Padding(
                padding: const EdgeInsets.all(16),
                child: Wrap(
                  alignment: WrapAlignment.spaceBetween,
                  runSpacing: 8,
                  children: macros.entries
                      .map((entry) => Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              Text(entry.key.toUpperCase()),
                              Text('${entry.value}', style: Theme.of(context).textTheme.titleLarge),
                            ],
                          ))
                      .toList(),
                ),
              ),
            ),
            ...plan.map((item) => Card(
                  child: ListTile(
                    title: Text(item),
                    trailing: IconButton(
                      icon: const Icon(Icons.camera_alt_outlined),
                      onPressed: _isUploading ? null : _captureAndAnalyze,
                    ),
                  ),
                )),
            if (_isUploading) const LinearProgressIndicator(),
            if (_analysis != null)
              Card(
                child: Padding(
                  padding: const EdgeInsets.all(16),
                  child: Text(_analysis!),
                ),
              ),
            if (_cameraController != null && _cameraController!.value.isInitialized)
              Padding(
                padding: const EdgeInsets.only(top: 16),
                child: AspectRatio(
                  aspectRatio: _cameraController!.value.aspectRatio,
                  child: CameraPreview(_cameraController!),
                ),
              ),
          ],
        ),
      ),
    );
  }
}
