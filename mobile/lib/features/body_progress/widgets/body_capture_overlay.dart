import 'package:flutter/material.dart';

class BodyCaptureOverlay extends StatelessWidget {
  const BodyCaptureOverlay({super.key});

  @override
  Widget build(BuildContext context) {
    return IgnorePointer(
      child: CustomPaint(
        painter: _BodyOverlayPainter(),
        child: Container(),
      ),
    );
  }
}

class _BodyOverlayPainter extends CustomPainter {
  @override
  void paint(Canvas canvas, Size size) {
    final gridPaint = Paint()
      ..color = Colors.white.withOpacity(0.3)
      ..strokeWidth = 1;

    for (int i = 1; i < 3; i++) {
      final dy = size.height * i / 3;
      canvas.drawLine(Offset(0, dy), Offset(size.width, dy), gridPaint);
    }
    for (int i = 1; i < 3; i++) {
      final dx = size.width * i / 3;
      canvas.drawLine(Offset(dx, 0), Offset(dx, size.height), gridPaint);
    }

    final posePaint = Paint()
      ..color = Colors.white.withOpacity(0.4)
      ..style = PaintingStyle.stroke
      ..strokeWidth = 2;

    final bodyPath = Path()
      ..moveTo(size.width * 0.5, size.height * 0.1)
      ..quadraticBezierTo(size.width * 0.65, size.height * 0.25, size.width * 0.5, size.height * 0.4)
      ..quadraticBezierTo(size.width * 0.35, size.height * 0.25, size.width * 0.5, size.height * 0.1)
      ..moveTo(size.width * 0.5, size.height * 0.4)
      ..lineTo(size.width * 0.5, size.height * 0.75)
      ..moveTo(size.width * 0.3, size.height * 0.5)
      ..lineTo(size.width * 0.7, size.height * 0.5)
      ..moveTo(size.width * 0.5, size.height * 0.75)
      ..lineTo(size.width * 0.35, size.height * 0.95)
      ..moveTo(size.width * 0.5, size.height * 0.75)
      ..lineTo(size.width * 0.65, size.height * 0.95);

    canvas.drawPath(bodyPath, posePaint);
  }

  @override
  bool shouldRepaint(covariant CustomPainter oldDelegate) => false;
}
