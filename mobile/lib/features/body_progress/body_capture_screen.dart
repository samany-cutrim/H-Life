import 'package:camera/camera.dart';
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:local_auth/local_auth.dart';

import 'providers/body_capture_controller.dart';
import 'providers/body_progress_repository.dart';
import 'widgets/body_capture_overlay.dart';

class BodyCaptureScreen extends ConsumerStatefulWidget {
  const BodyCaptureScreen({super.key});

  @override
  ConsumerState<BodyCaptureScreen> createState() => _BodyCaptureScreenState();
}

class _BodyCaptureScreenState extends ConsumerState<BodyCaptureScreen> {
  CameraController? _controller;
  bool _loadingCamera = false;
  final LocalAuthentication _auth = LocalAuthentication();
  bool _privacyEnabled = true;

  @override
  void initState() {
    super.initState();
    _initializeCamera();
  }

  @override
  void dispose() {
    _controller?.dispose();
    super.dispose();
  }

  Future<void> _initializeCamera() async {
    setState(() => _loadingCamera = true);
    try {
      final cameras = await availableCameras();
      final backCamera = cameras.firstWhere((camera) => camera.lensDirection == CameraLensDirection.back,
          orElse: () => cameras.first);
      _controller = CameraController(backCamera, ResolutionPreset.high, enableAudio: false);
      await _controller!.initialize();
      if (mounted) setState(() {});
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('Erro na câmera: $e')));
      }
    } finally {
      if (mounted) setState(() => _loadingCamera = false);
    }
  }

  Future<void> _startCapture() async {
    final controller = _controller;
    if (controller == null || !controller.value.isInitialized) return;
    try {
      await ref.read(bodyCaptureControllerProvider.notifier).startCountdown(controller);
    } catch (e) {
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text(e.toString())));
    }
  }

  Future<void> _upload() async {
    try {
      final notifier = ref.read(bodyCaptureControllerProvider.notifier);
      final capturedFile = ref.read(bodyCaptureControllerProvider).capturedFile;
      await notifier.uploadCapture();
      if (_privacyEnabled && capturedFile != null && await capturedFile.exists()) {
        await capturedFile.delete();
      }
      if (!mounted) return;
      ScaffoldMessenger.of(context)
          .showSnackBar(const SnackBar(content: Text('Upload enviado com metadados salvos.')));
    } catch (e) {
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('Erro no upload: $e')));
    }
  }

  Future<void> _authenticateGallery() async {
    try {
      final didAuthenticate = await _auth.authenticate(
        localizedReason: 'Confirme sua identidade para abrir a galeria',
        options: const AuthenticationOptions(biometricOnly: true),
      );
      if (didAuthenticate) {
        if (!mounted) return;
        ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('Galeria liberada.')));
      }
    } catch (e) {
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('Biometria indisponível: $e')));
    }
  }

  @override
  Widget build(BuildContext context) {
    final captureState = ref.watch(bodyCaptureControllerProvider);
    return Scaffold(
      appBar: AppBar(
        title: const Text('Captura guiada'),
        actions: [
          IconButton(
            onPressed: _authenticateGallery,
            icon: const Icon(Icons.lock),
            tooltip: 'Abrir galeria protegida',
          ),
        ],
      ),
      body: _loadingCamera || _controller == null
          ? const Center(child: CircularProgressIndicator())
          : Column(
              children: [
                Expanded(
                  child: Stack(
                    fit: StackFit.expand,
                    children: [
                      CameraPreview(_controller!),
                      const BodyCaptureOverlay(),
                      if (captureState.isCountingDown)
                        Center(
                          child: Container(
                            padding: const EdgeInsets.all(32),
                            decoration: BoxDecoration(
                              color: Colors.black.withOpacity(0.6),
                              shape: BoxShape.circle,
                            ),
                            child: Text(
                              '${captureState.countdown}',
                              style: const TextStyle(fontSize: 48, color: Colors.white),
                            ),
                          ),
                        ),
                    ],
                  ),
                ),
                if (captureState.capturedFile != null)
                  Padding(
                    padding: const EdgeInsets.all(16.0),
                    child: Column(
                      children: [
                        Text(
                          _privacyEnabled
                              ? 'Arquivo pronto para upload e será apagado localmente.'
                              : 'Arquivo capturado: ${captureState.capturedFile!.path.split('/').last}',
                        ),
                        const SizedBox(height: 8),
                        ElevatedButton.icon(
                          onPressed: _upload,
                          icon: const Icon(Icons.cloud_upload),
                          label: const Text('Enviar com metadados'),
                        ),
                        SwitchListTile.adaptive(
                          value: _privacyEnabled,
                          onChanged: (value) => setState(() => _privacyEnabled = value),
                          title: const Text('Apagar arquivo local após upload'),
                        ),
                      ],
                    ),
                  ),
                _CaptureControls(
                  state: captureState,
                  onStartCountdown: _startCapture,
                ),
              ],
            ),
    );
  }
}

class _CaptureControls extends ConsumerWidget {
  const _CaptureControls({required this.state, required this.onStartCountdown});

  final BodyCaptureState state;
  final VoidCallback onStartCountdown;

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final controller = ref.read(bodyCaptureControllerProvider.notifier);
    return Padding(
      padding: const EdgeInsets.all(16.0),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          DropdownButton<BodyView>(
            value: state.view,
            items: BodyView.values
                .map((view) => DropdownMenuItem(value: view, child: Text(view.name.toUpperCase())))
                .toList(),
            onChanged: (value) => controller.updateView(value ?? BodyView.front),
          ),
          Row(
            children: [
              Expanded(
                child: Slider(
                  min: 100,
                  max: 300,
                  label: '${state.distanceCm.round()} cm',
                  value: state.distanceCm,
                  onChanged: controller.updateDistance,
                ),
              ),
              Text('${state.distanceCm.round()} cm distância'),
            ],
          ),
          Row(
            children: [
              Expanded(
                child: Slider(
                  min: 80,
                  max: 180,
                  label: '${state.cameraHeightCm.round()} cm',
                  value: state.cameraHeightCm,
                  onChanged: controller.updateCameraHeight,
                ),
              ),
              Text('${state.cameraHeightCm.round()} cm altura'),
            ],
          ),
          Wrap(
            spacing: 12,
            runSpacing: 8,
            children: [
              ChoiceChip(
                label: const Text('Iluminação difusa'),
                selected: state.lighting == 'Iluminação difusa',
                onSelected: (_) => controller.updateLighting('Iluminação difusa'),
              ),
              ChoiceChip(
                label: const Text('Luz natural'),
                selected: state.lighting == 'Luz natural',
                onSelected: (_) => controller.updateLighting('Luz natural'),
              ),
              ChoiceChip(
                label: const Text('Roupa justa'),
                selected: state.clothing == 'Roupa esportiva justa',
                onSelected: (_) => controller.updateClothing('Roupa esportiva justa'),
              ),
              ChoiceChip(
                label: const Text('Roupa neutra'),
                selected: state.clothing == 'Roupa neutra clara',
                onSelected: (_) => controller.updateClothing('Roupa neutra clara'),
              ),
            ],
          ),
          const SizedBox(height: 12),
          TextFormField(
            initialValue: state.location,
            decoration: const InputDecoration(labelText: 'Local / observações'),
            onChanged: controller.updateLocation,
          ),
          const SizedBox(height: 12),
          const Text('Checklist obrigatório:'),
          ...state.checklist.asMap().entries.map((entry) {
            final index = entry.key;
            final item = entry.value;
            return CheckboxListTile(
              value: item.checked,
              onChanged: (_) => controller.toggleChecklist(index),
              title: Text(item.label),
            );
          }),
          const SizedBox(height: 8),
          ElevatedButton.icon(
            onPressed: state.isCountingDown ? null : onStartCountdown,
            icon: const Icon(Icons.timer),
            label: const Text('Iniciar captura com contagem regressiva'),
          ),
        ],
      ),
    );
  }
}
