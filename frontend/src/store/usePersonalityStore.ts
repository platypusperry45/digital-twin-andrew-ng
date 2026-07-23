import { create } from "zustand";
import { PersonalityConfig } from "@/types";
import { api } from "@/lib/api";

interface PersonalityState {
  config: PersonalityConfig;
  isLoading: boolean;

  // Actions
  loadConfig: () => Promise<void>;
  updateConfig: (partial: Partial<PersonalityConfig>) => Promise<void>;
}

export const usePersonalityStore = create<PersonalityState>((set, get) => ({
  config: {
    tone: "pedagogical",
    analogiesFrequency: 85,
    firstPrinciplesFocus: 90,
    codeExplanationDepth: "high",
    mathRigorLevel: "balanced",
  },
  isLoading: false,

  loadConfig: async () => {
    set({ isLoading: true });
    try {
      const cfg = await api.fetchPersonalityConfig();
      set({ config: cfg, isLoading: false });
    } catch (err) {
      console.error("Failed loading personality settings", err);
      set({ isLoading: false });
    }
  },

  updateConfig: async (partial) => {
    const updated = { ...get().config, ...partial };
    set({ config: updated });
    await api.savePersonalityConfig(updated);
  },
}));