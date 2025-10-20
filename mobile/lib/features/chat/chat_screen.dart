import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_tts/flutter_tts.dart';
import 'package:speech_to_text/speech_to_text.dart' as stt;

class ChatMessage {
  const ChatMessage({required this.text, required this.fromUser});

  final String text;
  final bool fromUser;
}

class ChatController extends StateNotifier<List<ChatMessage>> {
  ChatController() : super(const []);

  void sendUserMessage(String text) {
    state = [...state, ChatMessage(text: text, fromUser: true)];
    _reply(text);
  }

  Future<void> _reply(String text) async {
    await Future<void>.delayed(const Duration(milliseconds: 500));
    state = [...state, ChatMessage(text: 'AI: $text (resposta gerada)', fromUser: false)];
  }
}

final chatProvider = StateNotifierProvider<ChatController, List<ChatMessage>>(
  (ref) => ChatController(),
);

class ChatScreen extends ConsumerStatefulWidget {
  const ChatScreen({super.key});

  @override
  ConsumerState<ChatScreen> createState() => _ChatScreenState();
}

class _ChatScreenState extends ConsumerState<ChatScreen> {
  final TextEditingController _controller = TextEditingController();
  final FlutterTts _tts = FlutterTts();
  final stt.SpeechToText _speech = stt.SpeechToText();
  bool _listening = false;

  Future<void> _toggleListening() async {
    if (!_listening) {
      final available = await _speech.initialize();
      if (available) {
        setState(() => _listening = true);
        await _speech.listen(onResult: (result) {
          _controller.text = result.recognizedWords;
        });
      }
    } else {
      await _speech.stop();
      setState(() => _listening = false);
    }
  }

  Future<void> _speak(String text) async {
    await _tts.speak(text);
  }

  @override
  void dispose() {
    _controller.dispose();
    _tts.stop();
    _speech.stop();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final messages = ref.watch(chatProvider);
    return Scaffold(
      appBar: AppBar(title: const Text('Chat IA')),
      body: Column(
        children: [
          Expanded(
            child: ListView.builder(
              itemCount: messages.length,
              itemBuilder: (context, index) {
                final message = messages[index];
                return ListTile(
                  title: Align(
                    alignment: message.fromUser ? Alignment.centerRight : Alignment.centerLeft,
                    child: DecoratedBox(
                      decoration: BoxDecoration(
                        color: message.fromUser
                            ? Theme.of(context).colorScheme.primaryContainer
                            : Theme.of(context).colorScheme.secondaryContainer,
                        borderRadius: BorderRadius.circular(12),
                      ),
                      child: Padding(
                        padding: const EdgeInsets.all(12.0),
                        child: Text(message.text),
                      ),
                    ),
                  ),
                  onTap: () => _speak(message.text),
                );
              },
            ),
          ),
          Padding(
            padding: const EdgeInsets.all(8.0),
            child: Row(
              children: [
                IconButton(
                  icon: Icon(_listening ? Icons.stop : Icons.mic),
                  onPressed: _toggleListening,
                ),
                Expanded(
                  child: TextField(
                    controller: _controller,
                    decoration: const InputDecoration(hintText: 'Digite ou dite sua mensagem'),
                  ),
                ),
                IconButton(
                  icon: const Icon(Icons.send),
                  onPressed: () {
                    final text = _controller.text.trim();
                    if (text.isNotEmpty) {
                      ref.read(chatProvider.notifier).sendUserMessage(text);
                      _controller.clear();
                    }
                  },
                ),
              ],
            ),
          )
        ],
      ),
    );
  }
}
