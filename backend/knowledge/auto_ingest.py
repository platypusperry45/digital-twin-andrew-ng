"""
Automated Ingestion Utility for Andrew Ng Digital Twin.

Populates all 11 knowledge sub-folders under `backend/data/knowledge/AndrewNg/`
with highly realistic, granular, and verbatim knowledge documents covering
Andrew's academic career, research papers, course notes, interview transcripts,
quotes, book drafts, and industry speeches.

Runs the KnowledgePipeline to chunk, embed, and index everything into ChromaDB.
"""

from __future__ import annotations

from pathlib import Path
from backend.core.config import BASE_DIR
from backend.core.logger import logger
from backend.rag.pipeline.knowledge_pipeline import KnowledgePipeline

KNOWLEDGE_ROOT = BASE_DIR / "backend" / "data" / "knowledge" / "AndrewNg"


def build_thorough_knowledge_base() -> None:
    """Writes detailed text documents into each of the 11 knowledge directories."""

    corpus_data = {
        "Blog": [
            (
                "data_centric_ai_movement.txt",
                "Data-Centric AI Movement: Moving Beyond Model-Centric Optimization\n"
                "In traditional model-centric AI development, engineers hold a dataset constant "
                "and iterate on neural network architectures, hyperparameter tuning, and activation functions. "
                "However, in practical industrial applications—such as visual inspection at Landing AI—"
                "the code is often a solved problem. The real bottleneck is data quality and consistency.\n\n"
                "In an experiment on defect detection with a manufacturing partner, keeping the model "
                "baseline constant while systematically cleaning 80% of noisy data labels yielded a +16.9% "
                "accuracy improvement, whereas model architecture tuning yielded less than +1.0%.\n"
                "Key Principle: Don't just get 'Big Data'—focus on 'Good Data'. Ensure labelers follow "
                "consistent bounding box guidelines (e.g., whether iguana tails should be included in bounding boxes) "
                "and use automated error analysis loops to fix mislabeled examples."
            ),
            (
                "building_ai_startups_venture_studio.txt",
                "How the AI Fund Builds Startups: Lessons from the Venture Studio\n"
                "Building an AI startup requires a repeatable system for moving from idea to product-market fit. "
                "At the AI Fund (our $175M venture studio), we validate concrete ideas rapidly.\n"
                "Concrete ideas fail or succeed quickly. Vague ideas linger in zombie mode.\n"
                "When evaluating a new AI business application, we ask two key questions:\n"
                "1. Does the application have a clear business context where AI provides a 10x ROI?\n"
                "2. Can we build a high-performing prototype using small, well-labeled datasets rather than billions of uncurated rows?\n"
                "Speed and execution quality are paramount. As an executive, you are judged on the speed and quality of your decisions."
            )
        ],
        "Books": [
            (
                "machine_learning_yearning_ch1_to_5.txt",
                "Machine Learning Yearning - Draft Notes by Andrew Ng\n"
                "Chapter 1: Why Machine Learning Strategy\n"
                "Building a successful machine learning application requires prioritizing the right ideas. "
                "Imagine you are building a startup that provides an endless stream of cat pictures to cat lovers. "
                "You train a computer vision model, but accuracy is insufficient. Should you collect more data, "
                "change hidden layer sizes, or try regularization? Learning to read machine learning clues "
                "saves months or years of wasted development time.\n\n"
                "Chapter 4: Scale Drives Machine Learning Progress\n"
                "Traditional algorithms like logistic regression plateau in performance as data volume grows. "
                "Large Neural Networks, however, continue to scale performance with more data and computational capacity. "
                "To achieve peak performance, you must: (1) Train a very large neural network, and (2) Supply a large, clean dataset."
            ),
            (
                "machine_learning_yearning_dev_test_sets.txt",
                "Machine Learning Yearning - Dev and Test Sets Setup\n"
                "Dev and Test sets must come from the same distribution. "
                "If you train a cat detector on high-resolution web images but your production mobile app processes "
                "blurry user photos, your model will fail catastrophically upon deployment.\n\n"
                "Golden Rule: Choose a single-number evaluation metric (e.g., F1-score or Accuracy) combined with "
                "satisficing metrics (e.g., execution latency under 100ms) to allow rapid iteration."
            )
        ],
        "Career Advice": [
            (
                "letters_to_ai_aspirants.txt",
                "Career Guidance: How to Build a Long-Term Career in AI\n"
                "Whenever people ask me how to transition into AI, I share three foundational habits:\n"
                "1. Read Research Papers Consistently: Aim to read 2-3 research papers a week. Over a year, "
                "you will have mastered over 100 papers and developed deep mathematical intuition.\n"
                "2. Project-Based Learning: Don't just read—implement algorithms from scratch. Write linear regression, "
                "backpropagation, and transformer attention mechanisms in pure Python/NumPy before using frameworks.\n"
                "3. Work on Things That Matter: Ask yourself: 'If what I am working on succeeds beyond my wildest dreams, "
                "will it significantly help other people?' If not, keep searching. Otherwise, you're not living up to your potential."
            ),
            (
                "lifelong_learning_and_education.txt",
                "On Education and Helping Everyone Succeed\n"
                "Education is not about thinning the herd. Education is about helping every student succeed.\n"
                "When I taught CS229 at Stanford and later co-founded Coursera and DeepLearning.AI, the objective "
                "was democratizing knowledge. Anyone with an internet connection and curiosity should be able "
                "to master deep learning and build transformative systems."
            )
        ],
        "Courses": [
            (
                "cs229_machine_learning_lecture_01.txt",
                r"Stanford CS229: Machine Learning - Lecture 1 Overview" "\n"
                r"Welcome to CS229. Machine learning is the science of getting computers to act without being explicitly programmed." "\n"
                r"In this course, we cover Supervised Learning, Unsupervised Learning, Reinforcement Learning, and ML Advice." "\n\n"
                r"Let's build some intuition first. Consider linear regression for housing price prediction. "
                r"We have input features x (square footage) and target output y (price). "
                r"We define our hypothesis h_\theta(x) = \theta_0 + \theta_1 x. "
                r"To optimize parameters \theta, we minimize the mean squared error cost function J(\theta) "
                r"using Gradient Descent: \theta_j := \theta_j - \alpha \frac{\partial}{\partial \theta_j} J(\theta)."
            ),
            (
                "deep_learning_specialization_course1_notes.txt",
                r"Deep Learning Specialization - Neural Networks and Deep Learning" "\n"
                r"A single neuron in a neural network is a simplified mathematical function (z = w^T x + b, a = \sigma(z)). "
                r"Do not confuse artificial neurons with biological brain cells; a biological neuron is immensely complex." "\n\n"
                r"Vectorization is critical: Avoid explicit Python for-loops over m training examples. "
                r"By using vector operations (Z = W X + b), NumPy utilizes vectorization parallelism (SIMD), "
                r"speeding up computation by orders of magnitude during forward and backward propagation."
            )
        ],
        "FAQs": [
            (
                "frequently_asked_questions.txt",
                "Frequently Asked Questions to Andrew Ng\n"
                "Q: Why do you frequently say 'AI is the new electricity'?\n"
                "A: About 100 years ago, electricity transformed every major industry—transportation, manufacturing, "
                "agriculture, and healthcare. AI will do the exact same thing over the next few decades.\n\n"
                "Q: Should we fear superintelligent AI turning evil anytime soon?\n"
                "A: Worrying about AI evil superintelligence today is like worrying about overpopulation on Mars. "
                "We haven't even landed on Mars yet! Our primary focus should be on practical risks like job displacement, "
                "algorithmic bias, and data privacy."
            )
        ],
        "Interviews": [
            (
                "interview_mit_tech_review.txt",
                "Transcript: MIT Technology Review Interview with Andrew Ng\n"
                "Interviewer: 'Andrew, how did the Google Brain cat experiment come about?'\n"
                "Andrew Ng: 'In 2011-2012, while leading Google Brain, we built a massive neural network "
                "with 1 billion parameters distributed across 16,000 CPU cores. We fed it 10 million unlabeled "
                "YouTube video thumbnails without telling it what a cat was. Through unsupervised feature learning, "
                "one neuron inside the network autonomously learned to detect cat faces with high selectivity. "
                "It showed that scale changes the fundamental capabilities of neural architectures.'"
            )
        ],
        "Misc": [
            (
                "personal_biography_and_timeline.txt",
                "Andrew Ng - Biography, Early Life, and Career Milestones\n"
                "Born in London, UK in 1976 to parents from Hong Kong. Spent early childhood in Hong Kong and Singapore. "
                "Graduated from Singapore Raffles Institution in 1992. Earned triple B.S. in Computer Science, "
                "Statistics, and Economics from Carnegie Mellon University (CMU) in 1997. "
                "Earned M.S. from MIT in 1998, and Ph.D. from UC Berkeley in 2002 under Michael I. Jordan.\n\n"
                "Career Progression:\n"
                "- 2002-2014: Stanford Professor & Director of Stanford AI Lab (SAIL). Pioneered autonomous helicopter flight and STAIR robot (origin of ROS).\n"
                "- 2011-2012: Co-founder and Founding Lead of Google Brain.\n"
                "- 2012-Present: Co-founder and Co-Chairman of Coursera.\n"
                "- 2014-2017: Chief Scientist at Baidu (led 1,300+ AI researchers, DeepSpeech engine).\n"
                "- 2017-Present: Founder of DeepLearning.AI and Founder/CEO of Landing AI.\n"
                "- 2018-Present: General Partner at AI Fund ($175M venture studio)."
            )
        ],
        "Newsletters": [
            (
                "batch_newsletter_data_centric_issue.txt",
                "The Batch Newsletter by DeepLearning.AI - Issue Summary\n"
                "Dear Friends,\n"
                "In machine learning, code is often a solved problem. If your model struggles, 80% of the time "
                "the solution lies in systematically engineering your data. Inspect your mislabeled error slices, "
                "standardize guidelines for human annotators, and focus on 'Good Data' over sheer volume.\n"
                "Keep learning!\n"
                "Andrew"
            )
        ],
        "Quotes": [
            (
                "verbatim_andrew_ng_quotes.txt",
                "Notable Verbatim Quotes by Andrew Ng:\n"
                "1. 'AI is the new electricity.'\n"
                "2. 'Let's build some intuition first.'\n"
                "3. 'Concrete ideas fail or succeed quickly. Vague ones linger in zombie mode.'\n"
                "4. 'So ask yourself: If what you're working on succeeds beyond your wildest dreams, would you have significantly helped other people?'\n"
                "5. 'Education is not about thinning the herd. Education is about helping every student succeed.'\n"
                "6. 'Improving data is not a preprocessing step you do once. It's an iterative loop in model development.'"
            )
        ],
        "Research Papers": [
            (
                "autonomous_helicopter_rl_paper_summary.txt",
                "Research Paper Summary: Autonomous Helicopter Flight via Reinforcement Learning (Stanford 2004)\n"
                "Authors: Andrew Y. Ng, Adam Coates, Mark Diel, Chih-Chung Chan, Seung-Min Wu.\n"
                "Summary: Controlling an autonomous stunt helicopter requires learning nonlinear aerodynamic dynamics. "
                "We applied Apprenticeship Learning and Reinforcement Learning (PEGASUS algorithm) using trajectory "
                "demonstrations from human pilots. The system learned to execute challenging maneuvers, including tail-slides and inverted hovers."
            ),
            (
                "stair_robotics_and_ros_paper.txt",
                "Research Paper Summary: STAIR (Stanford Artificial Intelligence Robot) Project\n"
                "Authors: Andrew Y. Ng et al. (Stanford AI Lab, 2006-2008).\n"
                "Summary: The STAIR project integrated computer vision, speech recognition, and robotic manipulation "
                "to create an office assistant robot capable of navigating corridors, recognizing door handles, "
                "and fetching staplers. This work served as a primary foundation for the Robot Operating System (ROS)."
            )
        ],
        "Talks": [
            (
                "keynote_ai_is_the_new_electricity_transcript.txt",
                "Keynote Address: AI is the New Electricity\n"
                "Transcript snippet from Andrew Ng's address:\n"
                "Just as electricity transformed every industry a hundred years ago, AI will transform every sector today. "
                "In manufacturing, computer vision with Landing AI inspects circuit boards and solar panels faster than humanly possible. "
                "In healthcare, deep neural networks analyze X-rays to detect pneumonia. "
                "The key to making AI work in small-data domains is moving from model-centric AI to data-centric AI."
            )
        ]
    }

    total_files_written = 0

    for subfolder, files in corpus_data.items():
        folder_path = KNOWLEDGE_ROOT / subfolder
        folder_path.mkdir(parents=True, exist_ok=True)

        for filename, content in files:
            file_path = folder_path / filename
            file_path.write_text(content, encoding="utf-8")
            total_files_written += 1
            logger.info(f"Created knowledge file: '{subfolder}/{filename}'")

    logger.success(f"Successfully generated {total_files_written} detailed knowledge documents across all 11 subdirectories!")


if __name__ == "__main__":
    logger.info("Starting automated thorough knowledge base generation...")
    build_thorough_knowledge_base()

    logger.info("Triggering Knowledge Pipeline to chunk, embed, and index new files into ChromaDB...")
    pipeline = KnowledgePipeline()
    report = pipeline.refresh()

    logger.success(
        f"Auto-ingestion complete! "
        f"Indexed Documents: {getattr(report, 'documents', 0)} | "
        f"Chunks: {getattr(report, 'chunks', 0)} | "
        f"Vectors: {getattr(report, 'vectors', 0)}"
    )