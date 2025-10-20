import 'dart:async';
import 'dart:io';

import 'package:camera/camera.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import 'body_progress_repository.dart';

class ChecklistItem {
  ChecklistItem({required this.label, this.checked = false});

  final String label;
  final bool checked;

  ChecklistItem copyWith({bool? checked}) => ChecklistItem(label: label, checked: checked ?? this.checked);
}

class BodyCaptureState {
  const BodyCaptureState({
    this.view = BodyView.front,
    this.distanceCm = 200,
    this.cameraHeightCm = 120,
    this.lighting = 'Iluminação difusa',
    this.clothing = 'Roupa esportiva justa',
    this.location = 'Mesmo local',
    this.checklist = const [],
    this.isCountingDown = false,
    this.countdown = 3,
    this.capturedFile,
  });

  final BodyView view;
  final double distanceCm;
  final double cameraHeightCm;
  final String lighting;
  final String clothing;
  final String location;
  final List<ChecklistItem> checklist;
  final bool isCountingDown;
  final int countdown;
  final File? capturedFile;

  BodyCaptureState copyWith({
    BodyView? view,
    double? distanceCm,
    double? cameraHeightCm,
    String? lighting,
    String? clothing,
    String? location,
    List<ChecklistItem>? checklist,
    bool? isCountingDown,
    int? countdown,
    File? capturedFile,
    bool overrideCapture = false,
  }) {
    return BodyCaptureState(
      view: view ?? this.view,
      distanceCm: distanceCm ?? this.distanceCm,
      cameraHeightCm: cameraHeightCm ?? this.cameraHeightCm,
      lighting: lighting ?? this.lighting,
      clothing: clothing ?? this.clothing,
      location: location ?? this.location,
      checklist: checklist ?? this.checklist,
      isCountingDown: isCountingDown ?? this.isCountingDown,
      countdown: countdown ?? this.countdown,
      capturedFile: overrideCapture ? capturedFile : (capturedFile ?? this.capturedFile),
    );
  }
}

class BodyCaptureController extends StateNotifier<BodyCaptureState> {
  BodyCaptureController(this._repository)
      : super(BodyCaptureState(
          checklist: [
            ChecklistItem(label: 'Mesmo local e fundo neutro'),
            ChecklistItem(label: 'Iluminação difusa e frontal'),
            ChecklistItem(label: 'Distância e altura fixas'),
            ChecklistItem(label: 'Roupa igual e postura neutra'),
            ChecklistItem(label: 'Manhã em jejum leve'),
            ChecklistItem(label: 'Capturar ordem Frente → Lado → Costas'),
          ],
        ));

  final BodyProgressRepository _repository;
  Timer? _timer;

  void updateView(BodyView view) {
    state = state.copyWith(view: view);
  }

  void updateDistance(double value) => state = state.copyWith(distanceCm: value);

  void updateCameraHeight(double value) => state = state.copyWith(cameraHeightCm: value);

  void updateLighting(String value) => state = state.copyWith(lighting: value);

  void updateClothing(String value) => state = state.copyWith(clothing: value);

  void updateLocation(String value) => state = state.copyWith(location: value);

  void toggleChecklist(int index) {
    final updated = [...state.checklist];
    updated[index] = updated[index].copyWith(checked: !updated[index].checked);
    state = state.copyWith(checklist: updated);
  }

  bool get checklistComplete => state.checklist.every((item) => item.checked);

  Future<void> startCountdown(CameraController controller) async {
    if (!checklistComplete) {
      throw StateError('Checklist incompleto');
    }
    if (state.isCountingDown) {
      return;
    }
    state = state.copyWith(isCountingDown: true, countdown: 3);
    _timer?.cancel();
    _timer = Timer.periodic(const Duration(seconds: 1), (timer) async {
      final next = state.countdown - 1;
      if (next <= 0) {
        timer.cancel();
        state = state.copyWith(isCountingDown: false, countdown: 0);
        final file = await controller.takePicture();
        state = state.copyWith(capturedFile: File(file.path), overrideCapture: true);
      } else {
        state = state.copyWith(countdown: next);
      }
    });
  }

  Future<void> uploadCapture() async {
    final file = state.capturedFile;
    if (file == null) {
      throw StateError('Nenhuma captura disponível');
    }
    final metadata = BodyCaptureMetadata(
      distanceCm: state.distanceCm,
      cameraHeightCm: state.cameraHeightCm,
      lighting: state.lighting,
      clothing: state.clothing,
      location: state.location,
      view: state.view,
    );
    final uploadUrl = await _repository.requestUploadUrl(metadata);
    await _repository.uploadCapture(uploadUrl: uploadUrl, file: file);
    state = state.copyWith(capturedFile: null, overrideCapture: true);
  }

  @override
  void dispose() {
    _timer?.cancel();
    super.dispose();
  }
}

final bodyCaptureControllerProvider =
    StateNotifierProvider<BodyCaptureController, BodyCaptureState>((ref) {
  final repository = ref.watch(bodyProgressRepositoryProvider);
  return BodyCaptureController(repository);
});
