# Mobile (Flutter)

## Flavors e Configs

- `env.dev.example`
- `env.staging.example`
- `env.prod.example`

Cada arquivo define chaves de API, base URL e configurações de push. Os segredos sensíveis são carregados via `flutter_secure_storage` após o onboarding.

## Principais Funcionalidades

- Onboarding com captura de consentimentos LGPD.
- Dashboard com hidratação, treinos e nutrição sincronizados.
- Câmera com overlay, temporizador, grade e checklist para fotos corporais.
- Upload com metadados completos (distância, altura câmera, iluminação, roupa).
- Comparação side-by-side/slider para evolução corporal.
- Integração com FCM (config pronta em `firebase_options.dart`).

## Scripts

| Comando | Descrição |
|---------|-----------|
| `flutter pub get` | Instala dependências |
| `flutter test` | Testes unitários |
| `flutter run --flavor dev -t lib/main_dev.dart` | Execução Dev |
| `flutter build apk --flavor prod` | Build Android |
| `flutter build ios --flavor prod` | Build iOS |

## Requisitos Extras

- Android: `usesCleartextTraffic="true"` em dev ou usar túnel HTTPS.
- iOS: exceções ATS configuradas em `Info.plist` para dev.
- Configurar `google-services.json`/`GoogleService-Info.plist` antes do build.

## Estrutura

```
lib/
  main_dev.dart
  main_staging.dart
  main_prod.dart
  core/
  features/
    nutrition/
    training/
    hydration/
    body_progress/
    reports/
  shared/
```
