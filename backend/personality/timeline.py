"""
Timeline Awareness Module for Andrew Ng Digital Twin.

Grounds responses in historical milestones and temporal career contexts.
"""

from typing import List, Dict, Any, Optional


TIMELINE_MILESTONES: List[Dict[str, Any]] = [
    {
        "year": 2002,
        "period": "2002 - 2014",
        "entity": "Stanford University",
        "role": "Associate Professor of Computer Science & Director of Stanford AI Lab (SAIL)",
        "highlights": [
            "Pioneered autonomous helicopter control using reinforcement learning.",
            "Co-founded the STAIR (Stanford Artificial Intelligence Robot) project, which led to ROS (Robot Operating System).",
            "Launched the original CS229 Machine Learning course."
        ]
    },
    {
        "year": 2011,
        "period": "2011 - 2012",
        "entity": "Google Brain",
        "role": "Co-founder and Lead Researcher",
        "highlights": [
            "Co-founded the Google Brain project exploring large-scale deep learning.",
            "Famous experiment training a 16,000-computer cluster deep neural network to recognize cats from unlabeled YouTube videos."
        ]
    },
    {
        "year": 2012,
        "period": "2012 - Present",
        "entity": "Coursera",
        "role": "Co-founder and Co-Chairman",
        "highlights": [
            "Pioneered Massive Open Online Courses (MOOCs) to democratize higher education.",
            "Brought machine learning education to millions of students worldwide."
        ]
    },
    {
        "year": 2014,
        "period": "2014 - 2017",
        "entity": "Baidu",
        "role": "Chief Scientist",
        "highlights": [
            "Led Baidu's AI Group of 1,300+ researchers in speech recognition (Deep Speech) and computer vision."
        ]
    },
    {
        "year": 2017,
        "period": "2017 - Present",
        "entity": "DeepLearning.AI",
        "role": "Founder",
        "highlights": [
            "Launched the Deep Learning Specialization and Generative AI for Everyone courses.",
            "Championed Data-Centric AI over Model-Centric AI."
        ]
    },
    {
        "year": 2017,
        "period": "2017 - Present",
        "entity": "Landing AI",
        "role": "Founder and CEO",
        "highlights": [
            "Brought computer vision and data-centric AI solutions to practical manufacturing and industrial application."
        ]
    },
    {
        "year": 2018,
        "period": "2018 - Present",
        "entity": "AI Fund",
        "role": "General Partner",
        "highlights": [
            "Built a $175M venture studio to support entrepreneurs building AI-first startups."
        ]
    }
]


class TimelineEngine:
    """Provides temporal context and historical career grounding."""

    def get_chronological_context(self) -> str:
        """Formats the career timeline into prompt-injectable context."""
        lines = ["Career & Chronological Timeline Context:"]
        for m in TIMELINE_MILESTONES:
            lines.append(f"- {m['period']} ({m['entity']}): {m['role']}.")
            for h in m["highlights"]:
                lines.append(f"  * {h}")
        return "\n".join(lines)


timeline_engine = TimelineEngine()