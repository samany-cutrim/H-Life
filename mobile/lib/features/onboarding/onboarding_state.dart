import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:hive_flutter/hive_flutter.dart';

import '../../core/storage/hive_manager.dart';

enum TrainingModality { gym, home, outdoor, crossfit, pilates, yoga }

enum Restriction { gastritis, hypertension, insulinResistance, injury }

enum Equipment { dumbbells, bands, barbell, none }

class OnboardingState {
  const OnboardingState({
    this.goal = '',
    this.daysPerWeek = 3,
    this.selectedModalities = const {},
    this.restrictions = const {},
    this.equipment = const {},
    this.budget = 0,
  });

  final String goal;
  final int daysPerWeek;
  final Set<TrainingModality> selectedModalities;
  final Set<Restriction> restrictions;
  final Set<Equipment> equipment;
  final double budget;

  OnboardingState copyWith({
    String? goal,
    int? daysPerWeek,
    Set<TrainingModality>? selectedModalities,
    Set<Restriction>? restrictions,
    Set<Equipment>? equipment,
    double? budget,
  }) {
    return OnboardingState(
      goal: goal ?? this.goal,
      daysPerWeek: daysPerWeek ?? this.daysPerWeek,
      selectedModalities: selectedModalities ?? this.selectedModalities,
      restrictions: restrictions ?? this.restrictions,
      equipment: equipment ?? this.equipment,
      budget: budget ?? this.budget,
    );
  }
}

class OnboardingController extends StateNotifier<OnboardingState> {
  OnboardingController() : super(const OnboardingState()) {
    _hydrate();
  }

  Future<void> _hydrate() async {
    final box = Hive.box(HiveManager.onboardingBox);
    final stored = box.get('state') as Map<dynamic, dynamic>?;
    if (stored != null) {
      state = OnboardingState(
        goal: stored['goal'] as String? ?? '',
        daysPerWeek: stored['daysPerWeek'] as int? ?? 3,
        selectedModalities: {
          for (final value in (stored['modalities'] as List<dynamic>? ?? []))
            TrainingModality.values.firstWhere((e) => e.name == value)
        },
        restrictions: {
          for (final value in (stored['restrictions'] as List<dynamic>? ?? []))
            Restriction.values.firstWhere((e) => e.name == value)
        },
        equipment: {
          for (final value in (stored['equipment'] as List<dynamic>? ?? []))
            Equipment.values.firstWhere((e) => e.name == value)
        },
        budget: (stored['budget'] as num?)?.toDouble() ?? 0,
      );
    }
  }

  void updateGoal(String goal) => _update(state.copyWith(goal: goal));

  void updateDays(int days) => _update(state.copyWith(daysPerWeek: days));

  void toggleModality(TrainingModality modality) {
    final updated = {...state.selectedModalities};
    if (!updated.add(modality)) {
      updated.remove(modality);
    }
    _update(state.copyWith(selectedModalities: updated));
  }

  void toggleRestriction(Restriction restriction) {
    final updated = {...state.restrictions};
    if (!updated.add(restriction)) {
      updated.remove(restriction);
    }
    _update(state.copyWith(restrictions: updated));
  }

  void toggleEquipment(Equipment equipment) {
    final updated = {...state.equipment};
    if (!updated.add(equipment)) {
      updated.remove(equipment);
    }
    _update(state.copyWith(equipment: updated));
  }

  void updateBudget(double budget) => _update(state.copyWith(budget: budget));

  void _update(OnboardingState value) {
    state = value;
    final box = Hive.box(HiveManager.onboardingBox);
    box.put('state', {
      'goal': state.goal,
      'daysPerWeek': state.daysPerWeek,
      'modalities': state.selectedModalities.map((e) => e.name).toList(),
      'restrictions': state.restrictions.map((e) => e.name).toList(),
      'equipment': state.equipment.map((e) => e.name).toList(),
      'budget': state.budget,
    });
  }
}

final onboardingControllerProvider =
    StateNotifierProvider<OnboardingController, OnboardingState>((ref) {
  return OnboardingController();
});
