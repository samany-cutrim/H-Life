import 'package:firebase_core/firebase_core.dart';
import 'package:firebase_messaging/firebase_messaging.dart';
import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';

class FcmService {
  static Future<void> initialize() async {
    try {
      await Firebase.initializeApp();
      FirebaseMessaging messaging = FirebaseMessaging.instance;
      await messaging.requestPermission();
      FirebaseMessaging.onMessage.listen((RemoteMessage message) {
        debugPrint('FCM message received: ${message.messageId}');
      });
      if (kDebugMode) {
        final token = await messaging.getToken();
        debugPrint('FCM token: $token');
      }
    } catch (e) {
      debugPrint('Failed to init FCM: $e');
    }
  }
}
