"use client";

import React from "react";
import {
  Radar,
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  ResponsiveContainer,
} from "recharts";
import { PersonalityConfig } from "@/types";

interface PersonalityRadarProps {
  config: PersonalityConfig;
}

export default function PersonalityRadar({ config }: PersonalityRadarProps) {
  const data = [
    { subject: "Analogies", value: config.analogiesFrequency, fullMark: 100 },
    { subject: "First Principles", value: config.firstPrinciplesFocus, fullMark: 100 },
    {
      subject: "Math Rigor",
      value: config.mathRigorLevel === "formal" ? 95 : config.mathRigorLevel === "balanced" ? 65 : 30,
      fullMark: 100,
    },
    {
      subject: "Code Depth",
      value: config.codeExplanationDepth === "high" ? 90 : config.codeExplanationDepth === "medium" ? 60 : 30,
      fullMark: 100,
    },
    {
      subject: "Pedagogy Tone",
      value: config.tone === "rigorous" ? 95 : config.tone === "pedagogical" ? 85 : 60,
      fullMark: 100,
    },
  ];

  return (
    <div className="w-full h-64 flex flex-col items-center justify-center">
      <ResponsiveContainer width="100%" height="100%">
        <RadarChart cx="50%" cy="50%" outerRadius="75%" data={data}>
          <PolarGrid stroke="#334155" />
          <PolarAngleAxis dataKey="subject" stroke="#94a3b8" tick={{ fill: "#94a3b8", fontSize: 11 }} />
          <PolarRadiusAxis angle={30} domain={[0, 100]} stroke="#475569" />
          <Radar
            name="Andrew Persona Profile"
            dataKey="value"
            stroke="#6366f1"
            fill="#6366f1"
            fillOpacity={0.4}
          />
        </RadarChart>
      </ResponsiveContainer>
    </div>
  );
}