# IA & Modelos

## Abstração `AIProvider`

```python
provider = AIProvider.from_settings(settings)
response = provider.generate_plan(prompt, timeout=15)
```

- Suporte a OpenAI (API oficial) e provedores locais (text-generation-inference).
- Timeout configurável (`AI_TIMEOUT_SECONDS`).
- Retentativas exponenciais com jitter.

## Pipelines

- **Pose**: MoveNet (lite) via TF Lite ou MediaPipe, encapsulado em `PosePipeline`. Retorna keypoints normalizados + confiança.
- **Segmentação**: DeepLabV3 (ONNX) com fallback para `rembg`. Utilizado para remover fundo de fotos corporais.
- **OCR**: Tesseract (docker) + heurísticas para laudos médicos.
- **Visão Nutricional**: Modelo leve (Food-ViT) para estimar calorias por imagem.

## Dados de Exemplo

- `app/data/vision_samples/plate.jpg`
- `app/data/vision_samples/squat.mp4`

## Rate Limiting

- Endpoints `photo-analysis`, `video-analysis`, `ocr` usam quota compartilhada por usuário (5 requisições/5min).
- Implementado em `app/core/rate_limit.py` com backend Redis (`rate_limit:{user_id}`) ou memória.

## Testes

- `tests/test_ai_pipelines.py` valida fallback e parsing de respostas.
- `tests/test_rate_limit.py` garante bloqueio após exceder quota.
