import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import 'onboarding_state.dart';

class OnboardingScreen extends ConsumerStatefulWidget {
  const OnboardingScreen({super.key});

  @override
  ConsumerState<OnboardingScreen> createState() => _OnboardingScreenState();
}

class _OnboardingScreenState extends ConsumerState<OnboardingScreen> {
  int _stepIndex = 0;

  @override
  Widget build(BuildContext context) {
    final state = ref.watch(onboardingControllerProvider);
    final controller = ref.read(onboardingControllerProvider.notifier);

    return Scaffold(
      appBar: AppBar(
        title: const Text('Bem-vindo ao H-Life'),
      ),
      body: Stepper(
        currentStep: _stepIndex,
        onStepContinue: () {
          if (_stepIndex >= 5) {
            GoRouter.of(context).go('/home');
          } else {
            setState(() => _stepIndex += 1);
          }
        },
        onStepCancel: () {
          if (_stepIndex > 0) {
            setState(() => _stepIndex -= 1);
          }
        },
        onStepTapped: (index) => setState(() => _stepIndex = index),
        controlsBuilder: (context, details) {
          return Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              if (_stepIndex > 0)
                TextButton(onPressed: details.onStepCancel, child: const Text('Voltar')),
              ElevatedButton(
                onPressed: details.onStepContinue,
                child: Text(_stepIndex == 5 ? 'Começar' : 'Próximo'),
              ),
            ],
          );
        },
        steps: [
          Step(
            title: const Text('Objetivo'),
            content: TextFormField(
              initialValue: state.goal,
              decoration: const InputDecoration(labelText: 'Qual é o seu objetivo?'),
              onChanged: controller.updateGoal,
            ),
            isActive: _stepIndex >= 0,
            state: state.goal.isNotEmpty ? StepState.complete : StepState.indexed,
          ),
          Step(
            title: const Text('Dias por semana'),
            content: Slider(
              value: state.daysPerWeek.toDouble(),
              min: 1,
              max: 7,
              divisions: 6,
              label: '${state.daysPerWeek} dias',
              onChanged: (value) => controller.updateDays(value.toInt()),
            ),
            isActive: _stepIndex >= 1,
            state: state.daysPerWeek > 0 ? StepState.complete : StepState.indexed,
          ),
          Step(
            title: const Text('Modalidades'),
            content: Wrap(
              spacing: 8,
              children: TrainingModality.values
                  .map((modality) => FilterChip(
                        label: Text(modality.name),
                        selected: state.selectedModalities.contains(modality),
                        onSelected: (_) => controller.toggleModality(modality),
                      ))
                  .toList(),
            ),
            isActive: _stepIndex >= 2,
            state: state.selectedModalities.isNotEmpty ? StepState.complete : StepState.indexed,
          ),
          Step(
            title: const Text('Restrições'),
            content: Wrap(
              spacing: 8,
              children: Restriction.values
                  .map((restriction) => FilterChip(
                        label: Text(restriction.name),
                        selected: state.restrictions.contains(restriction),
                        onSelected: (_) => controller.toggleRestriction(restriction),
                      ))
                  .toList(),
            ),
            isActive: _stepIndex >= 3,
            state: state.restrictions.isNotEmpty ? StepState.complete : StepState.indexed,
          ),
          Step(
            title: const Text('Equipamentos'),
            content: Wrap(
              spacing: 8,
              children: Equipment.values
                  .map((equipment) => FilterChip(
                        label: Text(equipment.name),
                        selected: state.equipment.contains(equipment),
                        onSelected: (_) => controller.toggleEquipment(equipment),
                      ))
                  .toList(),
            ),
            isActive: _stepIndex >= 4,
            state: state.equipment.isNotEmpty ? StepState.complete : StepState.indexed,
          ),
          Step(
            title: const Text('Orçamento mensal'),
            content: Column(
              children: [
                Slider(
                  value: state.budget,
                  min: 0,
                  max: 1000,
                  divisions: 20,
                  label: 'R\$ ${state.budget.toStringAsFixed(0)}',
                  onChanged: (value) => controller.updateBudget(value),
                ),
                const Text('Isso ajuda a recomendar planos e equipamentos viáveis.'),
              ],
            ),
            isActive: _stepIndex >= 5,
            state: state.budget > 0 ? StepState.complete : StepState.indexed,
          ),
        ],
      ),
    );
  }
}
