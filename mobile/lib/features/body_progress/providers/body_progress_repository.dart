import 'dart:io';

import 'package:dio/dio.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../core/network/dio_provider.dart';

enum BodyView { front, side, back }

class BodyCaptureMetadata {
  const BodyCaptureMetadata({
    required this.distanceCm,
    required this.cameraHeightCm,
    required this.lighting,
    required this.clothing,
    required this.location,
    required this.view,
  });

  final double distanceCm;
  final double cameraHeightCm;
  final String lighting;
  final String clothing;
  final String location;
  final BodyView view;

  Map<String, dynamic> toJson() => {
        'distance_cm': distanceCm,
        'camera_height_cm': cameraHeightCm,
        'lighting': lighting,
        'clothing': clothing,
        'location': location,
        'view': view.name,
      };
}

class BodyAnalysisResult {
  const BodyAnalysisResult({
    required this.verdict,
    required this.confidence,
    required this.metrics,
    required this.beforeImageUrl,
    required this.afterImageUrl,
  });

  final String verdict;
  final double confidence;
  final Map<String, double> metrics;
  final String beforeImageUrl;
  final String afterImageUrl;
}

class BodyProgressRepository {
  BodyProgressRepository(this._dio);

  final Dio _dio;

  Future<String> requestUploadUrl(BodyCaptureMetadata metadata) async {
    final response = await _dio.post('/body-progress/upload-url', data: metadata.toJson());
    return response.data['upload_url'] as String;
  }

  Future<void> uploadCapture({required String uploadUrl, required File file}) async {
    await _dio.put(uploadUrl, data: file.openRead(), options: Options(headers: {'Content-Type': 'image/jpeg'}));
  }

  Future<BodyAnalysisResult> analyzeComparison({
    required String beforeId,
    required String afterId,
    required BodyView view,
  }) async {
    final response = await _dio.post('/body-progress/analyze', data: {
      'before_id': beforeId,
      'after_id': afterId,
      'view': view.name,
    });
    final data = response.data as Map<String, dynamic>;
    return BodyAnalysisResult(
      verdict: data['verdict'] as String? ?? 'Sem análise',
      confidence: (data['confidence'] as num?)?.toDouble() ?? 0,
      metrics: (data['deltas'] as Map<String, dynamic>? ?? {})
          .map((key, value) => MapEntry(key, (value as num).toDouble())),
      beforeImageUrl: data['before_image'] as String? ?? '',
      afterImageUrl: data['after_image'] as String? ?? '',
    );
  }

  Future<List<Map<String, dynamic>>> listCaptures() async {
    final response = await _dio.get('/body-progress');
    return (response.data as List<dynamic>)
        .map((entry) => Map<String, dynamic>.from(entry as Map))
        .toList();
  }
}

final bodyProgressRepositoryProvider = Provider<BodyProgressRepository>((ref) {
  final dio = ref.watch(dioProvider);
  return BodyProgressRepository(dio);
});
