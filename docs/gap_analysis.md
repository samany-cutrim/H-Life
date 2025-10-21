# Lacunas de Produto e Funcionalidades Pendentes

Este documento consolida funcionalidades estratégicas descritas na visão do aplicativo H-Life que ainda não estão implementadas ou estão presentes apenas como "stubs"/simulações no monorepo atual. Use esta lista como referência para priorização de roadmap e para alinhar expectativas com stakeholders.

## 1. Orquestração de IA Multimodal
- **Chat unificado** com histórico contextual, roteamento entre especialistas (nutrição, treino, médico) e suporte a prompts estruturados.
- **Integração com Whisper** ou serviço equivalente para transcrição de voz no backend; hoje o app móvel faz apenas processamento local básico.
- **Text-to-Speech (TTS)** server-side para respostas em áudio consistentes em todos os clientes.
- **Processamento de imagens e vídeos** com pipelines reais para detecção de alimentos e correção de postura (atualmente são respostas mockadas).

## 2. Gamificação
- **Sistema de desafios, metas e medalhas** persistente, com regras configuráveis por usuário.
- **Pontuação e ranking social**, inclusive endpoints para ranking global/grupos e telas correspondentes no front/mobile.
- **Recompensas e notificações** vinculadas ao progresso (ex.: streaks mais longos liberam medalhas especiais).

## 3. Marketplace e Profissionais Parceiros
- **Modelos e endpoints** para cadastro de nutricionistas, personal trainers e médicos, com validação de credenciais.
- **Fluxo de matching** entre usuário e profissional (solicitação, aceite, acompanhamento).
- **Gestão de comissões e assinatura** (planos pagos, repasse a profissionais) com integração a provedores de pagamento.

## 4. Ajustes Automáticos e Monitoramento Inteligente
- **Replanejamento dinâmico** de dietas/treinos quando o consumo real diverge das metas ou quando métricas fisiológicas sinalizam risco.
- **Interpretação semântica de sintomas** reportados no chat para acionar alertas e ajustes automáticos.
- **Motor de regras ou modelo preditivo** para avaliação contínua de fadiga, overtraining e adesão.

## 5. Segurança, Privacidade e LGPD Operacional
- **Gestão granular de consentimento** para compartilhamento de dados com profissionais e parceiros.
- **Logs de auditoria** e trilha de acesso a dados sensíveis.
- **Fluxo de exclusão/anonimização** sob demanda do usuário, com garantia de remoção em todos os serviços.

## 6. Relatórios Inteligentes e Consolidação de Dados
- **Geração de relatórios dinâmicos** que compilam métricas reais de dieta, treinos, hidratação e postura.
- **Visualizações gráficas** (curvas, comparativos) incluídas nos PDFs ou exportadas para web/mobile.
- **Envio automatizado** de relatórios para profissionais via e-mail seguro ou integrações específicas.

## 7. Integrações Externas e Parcerias
- **Importação automática** de bioimpedância via arquivos CSV/PDF ou APIs de fabricantes.
- **Catálogo de parceiros fitness** (suplementos, academias) com tracking de comissões.
- **Oferta white-label** com personalização de branding para clínicas e academias.

## 8. Painel Administrativo Web
- **Dashboard unificado** para gestão de usuários, profissionais, planos e relatórios.
- **Ferramentas de suporte** (reset de senha, suspensão de contas, auditoria).
- **KPIs operacionais** (retenção, adesão, NPS) para acompanhamento executivo.

## 9. Monitoramento e Observabilidade
- **Alertas proativos** (PagerDuty/Slack) para falhas em pipelines de IA ou ingestão de dados.
- **Dashboards de métricas** de uso (ex.: consultas ao LLM, uploads processados, taxa de erro). Atualmente existem apenas instruções genéricas em `docs/devops.md`.

## 10. Score de Saúde Unificado
- **Modelo de cálculo de score** que combine dieta, treino, hidratação e evolução corporal com pesos configuráveis.
- **Feedback acionável** a partir do score (ex.: avisos quando cair abaixo de limiares, recomendações de foco semanal).
- **Visualização histórica** do score e comparação com média da comunidade ou metas definidas pelo usuário/profissional.

## 11. Modo de Emergência e Alertas Preventivos
- **Detecção automática** de padrões críticos (ex.: relatos de dor aguda, marcadores clínicos fora do intervalo) para acionar modo de emergência.
- **Fluxo de escalonamento** com envio de alertas a contatos pré-definidos ou profissionais responsáveis.
- **Protocolos de resposta** documentados na aplicação (orientações passo a passo, botões de emergência) integrados ao chat multimodal.

## 12. Monetização e Planos de Assinatura
- **Gestão de tiers (Gratuito vs Premium)** com controle de acesso a funcionalidades avançadas (análise de vídeo, relatórios, ajustes automáticos).
- **Cobrança recorrente e faturamento** com suporte a gateways de pagamento, faturamento em diferentes moedas e notas fiscais.
- **Mecanismo de comissionamento** transparente para marketplace de profissionais e parcerias com marcas fitness.
0
> **Próximos passos sugeridos:** priorizar a implementação de um serviço de chat multimodal real, estabelecer o módulo de gamificação e definir MVP para onboarding de profissionais, pois esses blocos desbloqueiam diferenciais competitivos e caminhos de monetização.
