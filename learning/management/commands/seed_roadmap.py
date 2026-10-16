from datetime import timedelta
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone
from learning.models import Day, Project, Section, Task, Week

CURRICULUM = [
    {
        "title": "Phase 1 — Prompt Engineering",
        "order": 1,
        "description": "Learn how to design prompts, structure outputs, and evaluate LLM behavior reliably.",
        "weeks": [
            {
                "number": 1,
                "title": "LLM basics",
                "objective": "Understand the building blocks of large language models and how to call an LLM from Python.",
                "days": [
                    {"day_number": 1, "day_name": "Monday", "focus": "LLM basics", "task": "Learn what LLMs are, tokens, context windows, system/user/assistant messages, temperature, sampling, and the basics of API usage."},
                    {"day_number": 2, "day_name": "Tuesday", "focus": "Prompting", "task": "Study zero-shot, few-shot, role prompting, instruction hierarchy, and prompt decomposition; then write 10 prompts for the same problem."},
                    {"day_number": 3, "day_name": "Wednesday", "focus": "Structured outputs", "task": "Learn JSON, schemas, Pydantic, and structured output design; build a resume-to-structured-JSON flow."},
                    {"day_number": 4, "day_name": "Thursday", "focus": "Prompt evaluation", "task": "Create 20 test cases and compare Prompt A, B, and C for accuracy, hallucinations, formatting failures, and edge cases."},
                    {"day_number": 5, "day_name": "Friday", "focus": "AI Resume Analyzer", "task": "Build an AI Resume Analyzer that reads a resume and job description to output match score, skills, missing skills, and recommendations."},
                    {"day_number": 6, "day_name": "Saturday", "focus": "Project improvement", "task": "Improve the resume analyzer by adding Django API support, structured outputs, error handling, and a simple frontend if useful."},
                    {"day_number": 7, "day_name": "Sunday", "focus": "Documentation + review", "task": "Write a short reflection covering what you learned, what failed, what improved the result, and what you still do not understand."},
                ],
            }
        ],
    },
    {
        "title": "Phase 2 — Machine Learning + Mathematics",
        "order": 2,
        "description": "Build the mathematical foundation for machine learning, from feature/label thinking to classical models and evaluation.",
        "weeks": [
            {
                "number": 2,
                "title": "ML foundations",
                "objective": "Understand the differences between AI, ML, deep learning, and the core learning paradigms.",
                "days": [
                    {"day_number": 1, "day_name": "Monday", "focus": "AI vs ML vs deep learning", "task": "Study supervised, unsupervised, and reinforcement learning; note the differences and trade-offs in real-world use cases."},
                    {"day_number": 2, "day_name": "Tuesday", "focus": "Features and labels", "task": "Learn features, labels, training, validation, and testing; build a clear data pipeline mental model."},
                    {"day_number": 3, "day_name": "Wednesday", "focus": "Linear regression", "task": "Implement a linear regression example using scikit-learn and examine how features map to predictions."},
                    {"day_number": 4, "day_name": "Thursday", "focus": "Logistic regression", "task": "Implement a logistic regression classifier and understand probability outputs for binary classification."},
                    {"day_number": 5, "day_name": "Friday", "focus": "Overfitting and underfitting", "task": "Study bias, variance, overfitting, underfitting, and generalization with practical examples."},
                    {"day_number": 6, "day_name": "Saturday", "focus": "House Price Predictor", "task": "Build a House Price Predictor using a supervised learning workflow and document feature selection choices."},
                    {"day_number": 7, "day_name": "Sunday", "focus": "Documentation", "task": "Write a clear explanation of how a machine learns without using the word AI."},
                ],
            },
            {
                "number": 3,
                "title": "Linear algebra",
                "objective": "Learn vectors, matrices, and the linear algebra operations used across ML.",
                "days": [
                    {"day_number": 1, "day_name": "Monday", "focus": "Scalars and vectors", "task": "Understand scalars, vectors, dimensions, and how they represent data in ML."},
                    {"day_number": 2, "day_name": "Tuesday", "focus": "Dot products and magnitude", "task": "Study dot products, vector addition, and vector magnitude with simple Python examples."},
                    {"day_number": 3, "day_name": "Wednesday", "focus": "Vector operations", "task": "Implement vector operations in Python for add, subtract, dot product, and normalization."},
                    {"day_number": 4, "day_name": "Thursday", "focus": "Matrices", "task": "Learn matrices, shapes, and matrix multiplication with a practical example."},
                    {"day_number": 5, "day_name": "Friday", "focus": "Matrix multiplication", "task": "Implement matrix multiplication in Python and test it on small arrays."},
                    {"day_number": 6, "day_name": "Saturday", "focus": "Cosine similarity engine", "task": "Build a cosine similarity engine to compare vectors and interpret similarity scores."},
                    {"day_number": 7, "day_name": "Sunday", "focus": "Reflect and connect", "task": "Write down why vectors are important in machine learning and how matrix operations underpin model training."},
                ],
            },
            {
                "number": 4,
                "title": "Probability & statistics",
                "objective": "Build a working intuition for probability, distributions, and statistical thinking in ML.",
                "days": [
                    {"day_number": 1, "day_name": "Monday", "focus": "Summary statistics", "task": "Learn mean, median, mode, variance, and standard deviation and compute them on a small dataset."},
                    {"day_number": 2, "day_name": "Tuesday", "focus": "Probability", "task": "Study probability basics and conditional probability with intuitive examples."},
                    {"day_number": 3, "day_name": "Wednesday", "focus": "Probability distributions", "task": "Learn common distributions and explain how they model uncertainty in data."},
                    {"day_number": 4, "day_name": "Thursday", "focus": "Bayes theorem", "task": "Study Bayes theorem and solve a small classification example to understand posterior reasoning."},
                    {"day_number": 5, "day_name": "Friday", "focus": "Correlation and covariance", "task": "Explore correlation, covariance, and dependence between variables using a practical dataset."},
                    {"day_number": 6, "day_name": "Saturday", "focus": "Naive Bayes classifier", "task": "Implement a Naive Bayes classifier and compare predictions against a simple baseline."},
                    {"day_number": 7, "day_name": "Sunday", "focus": "Documentation", "task": "Document the role of probability in machine learning and summarize the main distributions and assumptions you used."},
                ],
            },
            {
                "number": 5,
                "title": "Calculus + optimization",
                "objective": "Understand derivatives, gradients, and gradient descent as the engine of training ML models.",
                "days": [
                    {"day_number": 1, "day_name": "Monday", "focus": "Functions and derivatives", "task": "Learn functions, derivatives, and how they describe change in a model."},
                    {"day_number": 2, "day_name": "Tuesday", "focus": "Partial derivatives and gradients", "task": "Study partial derivatives and gradients for multivariable functions used in ML models."},
                    {"day_number": 3, "day_name": "Wednesday", "focus": "Chain rule", "task": "Understand the chain rule and how it connects local changes across nested functions."},
                    {"day_number": 4, "day_name": "Thursday", "focus": "Gradient descent", "task": "Learn the idea of gradient descent, learning rate, local minima, and step size choices."},
                    {"day_number": 5, "day_name": "Friday", "focus": "Gradient descent implementation", "task": "Implement gradient descent on a simple dataset and observe how loss decreases over time."},
                    {"day_number": 6, "day_name": "Saturday", "focus": "Linear regression from scratch", "task": "Build linear regression without scikit-learn and explicitly update weights based on gradient descent."},
                    {"day_number": 7, "day_name": "Sunday", "focus": "Visualization", "task": "Visualize loss, gradients, and weight updates to explain the optimization loop in plain language."},
                ],
            },
            {
                "number": 6,
                "title": "ML algorithms",
                "objective": "Compare classic ML algorithms and understand when each approach is appropriate.",
                "days": [
                    {"day_number": 1, "day_name": "Monday", "focus": "Linear and logistic regression", "task": "Review linear regression and logistic regression and compare their assumptions and use cases."},
                    {"day_number": 2, "day_name": "Tuesday", "focus": "Decision trees and random forests", "task": "Study trees, splits, and ensemble learning; compare a tree versus a forest."},
                    {"day_number": 3, "day_name": "Wednesday", "focus": "KNN and K-means", "task": "Learn KNN for classification and K-means for clustering with a dataset and a visualization."},
                    {"day_number": 4, "day_name": "Thursday", "focus": "SVM and regularization", "task": "Study SVM, margin, and regularization; connect it to the bias-variance trade-off."},
                    {"day_number": 5, "day_name": "Friday", "focus": "Algorithm comparison", "task": "Compare algorithms for tabular data, talk through strengths and weaknesses, and document when one fits better than another."},
                    {"day_number": 6, "day_name": "Saturday", "focus": "Customer churn predictor", "task": "Build a churn prediction model and document preprocessing, model choice, and evaluation."},
                    {"day_number": 7, "day_name": "Sunday", "focus": "Model comparison review", "task": "Document the differences between algorithm families and write the practical lesson from each one."},
                ],
            },
            {
                "number": 7,
                "title": "ML evaluation",
                "objective": "Learn how to measure model quality and avoid common evaluation mistakes.",
                "days": [
                    {"day_number": 1, "day_name": "Monday", "focus": "Accuracy, precision, recall", "task": "Learn accuracy, precision, recall, and their effect on real-world decisions."},
                    {"day_number": 2, "day_name": "Tuesday", "focus": "F1 and confusion matrix", "task": "Compute F1 and examine confusion matrices to understand model failure modes."},
                    {"day_number": 3, "day_name": "Wednesday", "focus": "ROC-AUC", "task": "Study ROC curves and AUC as ranking metrics for binary classifiers."},
                    {"day_number": 4, "day_name": "Thursday", "focus": "Cross-validation", "task": "Learn cross-validation and why it is more reliable than a single train/test split."},
                    {"day_number": 5, "day_name": "Friday", "focus": "Bias, variance, leakage", "task": "Study bias/variance trade-offs and data leakage; document common failure modes."},
                    {"day_number": 6, "day_name": "Saturday", "focus": "ML API", "task": "Build a complete ML API with React, Django REST, and a prediction model connected end-to-end."},
                    {"day_number": 7, "day_name": "Sunday", "focus": "Section review", "task": "Review the major concepts from the ML and mathematics section and ensure you can explain overfitting, gradient descent, and vectors/matrices without notes."},
                ],
            },
        ],
    },
    {
        "title": "Phase 3 — Deep Learning",
        "order": 3,
        "description": "Move from classic ML to neural networks, representations, and deep learning training dynamics.",
        "weeks": [
            {
                "number": 8,
                "title": "Neural network basics",
                "objective": "Learn the core ingredients of neural networks: neurons, activations, loss, and backpropagation.",
                "days": [
                    {"day_number": 1, "day_name": "Monday", "focus": "Perceptron and neurons", "task": "Study the perceptron, neuron, and how a simple model forms a decision boundary."},
                    {"day_number": 2, "day_name": "Tuesday", "focus": "Activation functions", "task": "Learn ReLU, sigmoid, tanh, and why non-linearity matters in neural networks."},
                    {"day_number": 3, "day_name": "Wednesday", "focus": "Loss functions", "task": "Study mean squared error, cross-entropy, and the relationship between prediction error and optimization."},
                    {"day_number": 4, "day_name": "Thursday", "focus": "Forward propagation", "task": "Trace a forward pass through a simple network and understand intermediate activations."},
                    {"day_number": 5, "day_name": "Friday", "focus": "Backpropagation", "task": "Learn how gradients are propagated backward to update weights."},
                    {"day_number": 6, "day_name": "Saturday", "focus": "Single neuron from scratch", "task": "Implement a single neuron from scratch and train it on a tiny dataset."},
                    {"day_number": 7, "day_name": "Sunday", "focus": "Documentation", "task": "Document every component of a neural network and summarize the forward and backward flow in your own words."},
                ],
            },
            {
                "number": 9,
                "title": "Neural network from scratch",
                "objective": "Implement a multi-layer neural network with forward pass, loss, and backpropagation.",
                "days": [
                    {"day_number": 1, "day_name": "Monday", "focus": "Build layers", "task": "Implement layer abstractions to organize weights, inputs, and outputs."},
                    {"day_number": 2, "day_name": "Tuesday", "focus": "Activations", "task": "Add activation layers and compare different nonlinearities in a small network."},
                    {"day_number": 3, "day_name": "Wednesday", "focus": "Loss", "task": "Implement a loss function and inspect how prediction errors are computed."},
                    {"day_number": 4, "day_name": "Thursday", "focus": "Backpropagation", "task": "Implement gradient calculations for each layer and propagate errors correctly."},
                    {"day_number": 5, "day_name": "Friday", "focus": "Optimizers", "task": "Add an optimizer and adjust weights using gradient descent and learning-rate tuning."},
                    {"day_number": 6, "day_name": "Saturday", "focus": "Neural network from scratch", "task": "Build a complete neural network from scratch and train it on simple classification data."},
                    {"day_number": 7, "day_name": "Sunday", "focus": "Explain the system", "task": "Explain every component of the network, from input to optimizer to updated weights, using diagrams or notes."},
                ],
            },
            {
                "number": 10,
                "title": "PyTorch",
                "objective": "Use a modern deep learning framework with tensors, datasets, models, and training loops.",
                "days": [
                    {"day_number": 1, "day_name": "Monday", "focus": "PyTorch tensors", "task": "Learn tensors, operations, and shape conventions in PyTorch."},
                    {"day_number": 2, "day_name": "Tuesday", "focus": "Datasets and dataloaders", "task": "Study datasets, loaders, batching, and how to train efficiently on data."},
                    {"day_number": 3, "day_name": "Wednesday", "focus": "Neural networks in PyTorch", "task": "Build and train a simple neural network module with PyTorch."},
                    {"day_number": 4, "day_name": "Thursday", "focus": "Training loops", "task": "Implement the training loop, validation loop, and loss tracking."},
                    {"day_number": 5, "day_name": "Friday", "focus": "Optimizers", "task": "Compare Adam, SGD, and other optimizer choices on a small training task."},
                    {"day_number": 6, "day_name": "Saturday", "focus": "Image classifier", "task": "Build an image classifier in PyTorch and evaluate it on labeled samples."},
                    {"day_number": 7, "day_name": "Sunday", "focus": "Documentation", "task": "Document the training pipeline and methodically record how tensors, model, loss, and optimizer fit together."},
                ],
            },
            {
                "number": 11,
                "title": "Deep learning project",
                "objective": "Integrate deep learning concepts into a meaningful project and explain the full training loop.",
                "days": [
                    {"day_number": 1, "day_name": "Monday", "focus": "CNNs and embeddings", "task": "Learn convolutional layers, embeddings, and sequence representations used in deep learning models."},
                    {"day_number": 2, "day_name": "Tuesday", "focus": "Sequence models", "task": "Study sequence models and sequence padding, embeddings, and recurrence ideas."},
                    {"day_number": 3, "day_name": "Wednesday", "focus": "Regularization", "task": "Learn dropout, weight decay, and regularization patterns that stabilize training."},
                    {"day_number": 4, "day_name": "Thursday", "focus": "Project planning", "task": "Plan the image classification API: dataset, model, training loop, and deployment route."},
                    {"day_number": 5, "day_name": "Friday", "focus": "Build the model", "task": "Implement the image classifier and train it until you can show a working prediction flow."},
                    {"day_number": 7, "day_name": "Saturday", "focus": "API deployment", "task": "Wrap the trained model in a simple API and consider how it would be served in production."},
                    {"day_number": 6, "day_name": "Sunday", "focus": "Final explanation", "task": "Explain the full flow from input to neural network to loss to backprop to optimizer to updated weights."},
                ],
            },
        ],
    },
    {
        "title": "Phase 4 — Transformers",
        "order": 4,
        "description": "Study attention, sequence modeling, and transformer blocks as the foundation for modern LLMs.",
        "weeks": [
            {
                "number": 12,
                "title": "Attention",
                "objective": "Understand why sequence models struggle and how attention solves the problem.",
                "days": [
                    {"day_number": 1, "day_name": "Monday", "focus": "Why sequence models struggle", "task": "Study long-range dependencies and the bottlenecks of earlier sequence models."},
                    {"day_number": 2, "day_name": "Tuesday", "focus": "Attention concept", "task": "Learn the core idea of attention: weighted relationships between tokens."},
                    {"day_number": 3, "day_name": "Wednesday", "focus": "Query / Key / Value", "task": "Understand the role of queries, keys, and values and how scores are computed."},
                    {"day_number": 4, "day_name": "Thursday", "focus": "Self-attention", "task": "Trace self-attention in a small sequence and compare different token relationships."},
                    {"day_number": 5, "day_name": "Friday", "focus": "Implement self-attention", "task": "Write a small self-attention function and test it on a token sequence."},
                    {"day_number": 6, "day_name": "Saturday", "focus": "Visualize attention", "task": "Create a visualization that shows which tokens receive more weight in a sequence."},
                    {"day_number": 7, "day_name": "Sunday", "focus": "Documentation", "task": "Summarize what attention does and why it outperforms earlier sequence models."},
                ],
            },
            {
                "number": 13,
                "title": "Transformer architecture",
                "objective": "Build a complete conceptual understanding of transformer components and attention blocks.",
                "days": [
                    {"day_number": 1, "day_name": "Monday", "focus": "Multi-head attention", "task": "Study multi-head attention and why multiple heads allow diverse context patterns."},
                    {"day_number": 2, "day_name": "Tuesday", "focus": "Positional encoding", "task": "Learn why position matters in sequences and how encodings preserve order."},
                    {"day_number": 3, "day_name": "Wednesday", "focus": "Feed-forward layers", "task": "Understand feed-forward blocks and their role in transformer depth."},
                    {"day_number": 4, "day_name": "Thursday", "focus": "Residual connections", "task": "Study residual connections and how they stabilize deep architecture training."},
                    {"day_number": 5, "day_name": "Friday", "focus": "Layer normalization", "task": "Learn layer normalization and how it improves deep network learning."},
                    {"day_number": 6, "day_name": "Saturday", "focus": "Transformer block", "task": "Implement a transformer block and verify the interaction between attention, residuals, and normalization."},
                    {"day_number": 7, "day_name": "Sunday", "focus": "Reflection", "task": "Write a clean diagram of a transformer block and explain each component in your own words."},
                ],
            },
            {
                "number": 14,
                "title": "Mini GPT",
                "objective": "Connect tokenization, embeddings, position encoding, and transformer blocks into a tiny GPT-like model.",
                "days": [
                    {"day_number": 1, "day_name": "Monday", "focus": "Tokenization", "task": "Learn tokenization, vocabularies, and how text becomes discrete units for models."},
                    {"day_number": 2, "day_name": "Tuesday", "focus": "Embeddings", "task": "Study token embeddings and position embeddings and how they shape representation."},
                    {"day_number": 3, "day_name": "Wednesday", "focus": "Attention", "task": "Connect attention to the transformer block and note how context is gathered from prior tokens."},
                    {"day_number": 4, "day_name": "Thursday", "focus": "Transformer blocks", "task": "Learn how blocks stack into a deeper decoder-only architecture."},
                    {"day_number": 5, "day_name": "Friday", "focus": "Language modeling", "task": "Study next-token prediction and how logits become probabilistic output."},
                    {"day_number": 6, "day_name": "Saturday", "focus": "Tiny GPT", "task": "Build a tiny GPT or GPT-like model that predicts the next token from a small corpus."},
                    {"day_number": 7, "day_name": "Sunday", "focus": "Final test", "task": "Be able to draw the flow from tokens to embeddings to position to attention to transformer blocks to logits to next token."},
                ],
            },
        ],
    },
    {
        "title": "Phase 5 — LLMs + Training",
        "order": 5,
        "description": "Study the architecture and training pipeline behind modern LLMs, from tokenization to fine-tuning.",
        "weeks": [
            {
                "number": 15,
                "title": "Tokenization",
                "objective": "Understand tokenizer design, vocabularies, and byte-pair encoding in LLM training.",
                "days": [
                    {"day_number": 1, "day_name": "Monday", "focus": "Vocabulary and tokenization", "task": "Learn vocabulary, BPE, subword tokenization, and special tokens used by LLMs."},
                    {"day_number": 2, "day_name": "Tuesday", "focus": "BPE", "task": "Study BPE and how tokenization compresses vocabulary while preserving meaning."},
                    {"day_number": 3, "day_name": "Wednesday", "focus": "Subword design", "task": "Compare word-level, char-level, and subword approaches and how each affects model behavior."},
                    {"day_number": 4, "day_name": "Thursday", "focus": "Special tokens", "task": "Learn BOS, EOS, PAD, and other tokens used during training and inference."},
                    {"day_number": 5, "day_name": "Friday", "focus": "Tokenizer implementation", "task": "Build a basic tokenizer and inspect how texts are segmented into tokens."},
                    {"day_number": 6, "day_name": "Saturday", "focus": "Tokenizer project", "task": "Build a tokenizer project and test it on a few real text examples."},
                    {"day_number": 7, "day_name": "Sunday", "focus": "Review", "task": "Review the role of tokenization and document how choices affect context use and model behavior."},
                ],
            },
            {
                "number": 16,
                "title": "Pretraining",
                "objective": "Understand how raw text becomes a trained language model through next-token prediction.",
                "days": [
                    {"day_number": 1, "day_name": "Monday", "focus": "Dataset preparation", "task": "Learn how data pipelines clean, filter, and prepare text for language model training."},
                    {"day_number": 2, "day_name": "Tuesday", "focus": "Batching", "task": "Study batching, context windows, sequence packing, and training efficiency."},
                    {"day_number": 3, "day_name": "Wednesday", "focus": "Training objectives", "task": "Understand next-token prediction, loss, and the training objective for generative models."},
                    {"day_number": 4, "day_name": "Thursday", "focus": "Training loop", "task": "Trace a training loop from batch to logits to loss to weight updates."},
                    {"day_number": 5, "day_name": "Friday", "focus": "Tiny model training", "task": "Train a tiny language model on a small corpus and observe the loss curve."},
                    {"day_number": 6, "day_name": "Saturday", "focus": "Project", "task": "Train a tiny language model from scratch and keep a record of dataset, architecture, and performance."},
                    {"day_number": 7, "day_name": "Sunday", "focus": "Documentation", "task": "Document how raw data turns into a trained model, including batching, objective, and evaluation."},
                ],
            },
            {
                "number": 17,
                "title": "Fine-tuning",
                "objective": "Learn the difference between pretraining and fine-tuning and practice small-scale adaptation.",
                "days": [
                    {"day_number": 1, "day_name": "Monday", "focus": "Pretraining vs fine-tuning", "task": "Study when to pretrain, when to fine-tune, and how the model shifts from general language to task behavior."},
                    {"day_number": 2, "day_name": "Tuesday", "focus": "SFT and instruction datasets", "task": "Learn supervised fine-tuning and why instruction datasets matter for helpfulness."},
                    {"day_number": 3, "day_name": "Wednesday", "focus": "LoRA and PEFT", "task": "Study LoRA, PEFT, and how small adapters let you adapt an LLM efficiently."},
                    {"day_number": 4, "day_name": "Thursday", "focus": "Fine-tuning setup", "task": "Prepare a small training dataset and design a fine-tuning experiment to improve a specific behavior."},
                    {"day_number": 5, "day_name": "Friday", "focus": "Open-source model", "task": "Fine-tune a small open-source model with a manageable dataset and record the result."},
                    {"day_number": 6, "day_name": "Saturday", "focus": "Evaluation and tuning", "task": "Evaluate the model, inspect failures, and iterate on prompts or dataset quality."},
                    {"day_number": 7, "day_name": "Sunday", "focus": "Reflection", "task": "Document how fine-tuning differs from prompting and when parameter-efficient updates are worth it."},
                ],
            },
            {
                "number": 18,
                "title": "Alignment",
                "objective": "Understand preference learning and alignment techniques without building a full RLHF pipeline.",
                "days": [
                    {"day_number": 1, "day_name": "Monday", "focus": "Preference learning", "task": "Study preference learning and why it matters for aligning model behavior with human values."},
                    {"day_number": 2, "day_name": "Tuesday", "focus": "RLHF concept", "task": "Understand the role of reward models, preference data, and iterative improvement."},
                    {"day_number": 3, "day_name": "Wednesday", "focus": "DPO", "task": "Learn Direct Preference Optimization and why it is a simpler and popular alignment approach."},
                    {"day_number": 4, "day_name": "Thursday", "focus": "Safety alignment", "task": "Study safety alignment, harmful outputs, and refusal behavior in model training."},
                    {"day_number": 5, "day_name": "Friday", "focus": "Architecture understanding", "task": "Map the alignment architecture from preference data to model updates and review the purpose of each stage."},
                    {"day_number": 6, "day_name": "Saturday", "focus": "Project reflection", "task": "Consider how you would align a model in a real application and what metrics would matter for safety and usefulness."},
                    {"day_number": 7, "day_name": "Sunday", "focus": "Documentation", "task": "Write a short description of the alignment problem and the concepts of RLHF, DPO, and safety tuning."},
                ],
            },
            {
                "number": 19,
                "title": "CS336 / LLM training pipeline",
                "objective": "Go deeper into the end-to-end lifecycle of LLM training with Stanford CS336-style concepts.",
                "days": [
                    {"day_number": 1, "day_name": "Monday", "focus": "Data", "task": "Study data quality, curation, filtering, and the importance of dataset composition."},
                    {"day_number": 2, "day_name": "Tuesday", "focus": "Tokenization", "task": "Review tokenization choices and how they interact with architecture and training."},
                    {"day_number": 3, "day_name": "Wednesday", "focus": "Architecture", "task": "Understand the transformer architecture and its scaling properties."},
                    {"day_number": 4, "day_name": "Thursday", "focus": "Training", "task": "Study optimization, loss curves, and the training dynamics behind model convergence."},
                    {"day_number": 5, "day_name": "Friday", "focus": "Evaluation", "task": "Learn evaluation strategies, benchmark design, and how to identify failure cases."},
                    {"day_number": 6, "day_name": "Saturday", "focus": "LLM Training Report", "task": "Produce an LLM Training Report covering dataset, tokenizer, architecture, parameters, training, loss, evaluation, failures, and lessons."},
                    {"day_number": 7, "day_name": "Sunday", "focus": "Lifecycle explanation", "task": "Explain the entire lifecycle from raw data to trained LLM to usable model and note the most important bottlenecks and trade-offs."},
                ],
            },
        ],
    },
    {
        "title": "Phase 6 — AI Agents",
        "order": 6,
        "description": "Study tool use, memory, and the agent loop that allows LLMs to act on tasks and interact with systems.",
        "weeks": [
            {
                "number": 20,
                "title": "Tool calling",
                "objective": "Learn how function calling and tool schemas let agents act on external systems.",
                "days": [
                    {"day_number": 1, "day_name": "Monday", "focus": "Function calling", "task": "Learn function calling, tool schemas, and the idea of granting the model controlled actions."},
                    {"day_number": 2, "day_name": "Tuesday", "focus": "Structured outputs", "task": "Combine tool invocation with structured outputs and clean result handling."},
                    {"day_number": 3, "day_name": "Wednesday", "focus": "Tool design", "task": "Design a small tool interface and specify clear inputs, outputs, and failure modes."},
                    {"day_number": 4, "day_name": "Thursday", "focus": "Validation", "task": "Write validation logic to ensure tool calls are appropriately constrained and safe."},
                    {"day_number": 5, "day_name": "Friday", "focus": "Calculator Agent", "task": "Build a Calculator Agent that calls tools to solve arithmetic and math tasks."},
                    {"day_number": 6, "day_name": "Saturday", "focus": "Error handling", "task": "Add robust tool error handling, retries, and graceful failure returns."},
                    {"day_number": 7, "day_name": "Sunday", "focus": "Documentation", "task": "Document why tool calling matters and how function schemas keep model behavior precise and reliable."},
                ],
            },
            {
                "number": 21,
                "title": "Agent loops",
                "objective": "Understand the loop of think, choose tool, execute, observe, and continue safely.",
                "days": [
                    {"day_number": 1, "day_name": "Monday", "focus": "Agent loop", "task": "Study the sequence: think, choose tool, execute, observe, and continue."},
                    {"day_number": 2, "day_name": "Tuesday", "focus": "Research Agent", "task": "Design a research workflow in which the model chooses the next step based on evidence."},
                    {"day_number": 3, "day_name": "Wednesday", "focus": "Tools and state", "task": "Connect tool output back into model reasoning and note how the agent accumulates state."},
                    {"day_number": 4, "day_name": "Thursday", "focus": "Replanning", "task": "Learn how the agent should revise its plan when tool output changes the situation."},
                    {"day_number": 5, "day_name": "Friday", "focus": "Build a research agent", "task": "Implement a research agent that gathers several facts and then synthesizes a result."},
                    {"day_number": 6, "day_name": "Saturday", "focus": "Robustness", "task": "Add guardrails for repeated failures, non-actionable results, and vague reasoning loops."},
                    {"day_number": 7, "day_name": "Sunday", "focus": "Review", "task": "Explain how an agent loop differs from a normal function call and why state matters."},
                ],
            },
            {
                "number": 22,
                "title": "Memory + state",
                "objective": "Study short-term memory, long-term memory, conversation state, and persistence in agents.",
                "days": [
                    {"day_number": 1, "day_name": "Monday", "focus": "Short-term memory", "task": "Learn about memory within a single conversation and why context must be managed carefully."},
                    {"day_number": 2, "day_name": "Tuesday", "focus": "Long-term memory", "task": "Study persistent memory, user preferences, and retrieval of prior knowledge."},
                    {"day_number": 3, "day_name": "Wednesday", "focus": "State design", "task": "Model the agent state and carry it across tool calls and revisions."},
                    {"day_number": 4, "day_name": "Thursday", "focus": "Persistence", "task": "Design a storage layer for conversation state and user-specific context."},
                    {"day_number": 5, "day_name": "Friday", "focus": "ABSU Student Agent", "task": "Create a student agent that can check a result, register courses, create an invoice, print a receipt, and retrieve student information."},
                    {"day_number": 6, "day_name": "Saturday", "focus": "Evaluation", "task": "Test the student agent end-to-end and evaluate whether it interprets tasks, chooses tools, and completes them accurately."},
                    {"day_number": 7, "day_name": "Sunday", "focus": "Exit test", "task": "Verify you can explain how a task flows from receiving a goal to selecting tools to executing them and returning an answer."},
                ],
            },
        ],
    },
    {
        "title": "Phase 7 — Agentic Design Patterns",
        "order": 7,
        "description": "Explore routing, parallelization, reflection, planning, and orchestrator-worker design patterns for agent systems.",
        "weeks": [
            {
                "number": 23,
                "title": "Routing, parallelization, reflection",
                "objective": "Build small examples of the most common agentic orchestration patterns.",
                "days": [
                    {"day_number": 1, "day_name": "Monday", "focus": "Routing", "task": "Study routing and how the system chooses the correct sub-agent or tool for each task."},
                    {"day_number": 2, "day_name": "Tuesday", "focus": "Parallelization", "task": "Build a small example where multiple sub-tasks run in parallel and results are merged."},
                    {"day_number": 3, "day_name": "Wednesday", "focus": "Reflection", "task": "Design a reflexive loop where the agent examines its own output and corrects it."},
                    {"day_number": 4, "day_name": "Thursday", "focus": "Example implementation", "task": "Implement a small sample for each of the three patterns and compare their trade-offs."},
                    {"day_number": 5, "day_name": "Friday", "focus": "Failure cases", "task": "Explore failure modes such as repeated loops, stale state, and noisy parallel results."},
                    {"day_number": 6, "day_name": "Saturday", "focus": "Project build", "task": "Combine routing and reflection into a small agent workflow with clear responsibilities."},
                    {"day_number": 7, "day_name": "Sunday", "focus": "Documentation", "task": "Summarize when each pattern is useful and when a simpler function or API is better."},
                ],
            },
            {
                "number": 24,
                "title": "Planning and orchestration",
                "objective": "Learn orchestrator-worker, planner, writer, and evaluator flows for research and multi-step tasks.",
                "days": [
                    {"day_number": 1, "day_name": "Monday", "focus": "Planning", "task": "Study planning as a structured decomposition of a large task into subtasks."},
                    {"day_number": 2, "day_name": "Tuesday", "focus": "Orchestrator-worker", "task": "Learn how a coordinator distributes tasks and consolidates results from workers."},
                    {"day_number": 3, "day_name": "Wednesday", "focus": "Evaluator-optimizer", "task": "Understand how an evaluator checks output quality and tells the system to improve it."},
                    {"day_number": 4, "day_name": "Thursday", "focus": "Research agent design", "task": "Draft the architecture for an AI Research Agent with planner, researcher, evaluator, and writer roles."},
                    {"day_number": 5, "day_name": "Friday", "focus": "Build the workflow", "task": "Implement a small research workflow that plans, researches, evaluates, and writes a short report."},
                    {"day_number": 6, "day_name": "Saturday", "focus": "Analysis", "task": "Compare the planner/evaluator design against a simple one-pass model and identify where complexity pays off."},
                    {"day_number": 7, "day_name": "Sunday", "focus": "Exit test", "task": "Explain when an agentic design pattern is appropriate and when a normal function or API is preferable."},
                ],
            },
        ],
    },
    {
        "title": "Phase 8 — RAG",
        "order": 8,
        "description": "Learn retrieval, chunking, embeddings, and evaluation for grounded question-answering systems.",
        "weeks": [
            {
                "number": 25,
                "title": "Basic RAG",
                "objective": "Build a simple retrieval system that answers questions from documents with source grounding.",
                "days": [
                    {"day_number": 1, "day_name": "Monday", "focus": "Documents and chunking", "task": "Learn about documents, chunking, and why chunk boundaries matter for retrieval quality."},
                    {"day_number": 2, "day_name": "Tuesday", "focus": "Embeddings and vector DB", "task": "Study embeddings and vector databases and how retrieval uses similarity search."},
                    {"day_number": 3, "day_name": "Wednesday", "focus": "Retrieval flow", "task": "Map the full pipeline: ingest, embed, store, retrieve, and answer."},
                    {"day_number": 4, "day_name": "Thursday", "focus": "Project setup", "task": "Set up a PDF Q&A project with a small document corpus and a retrieval layer."},
                    {"day_number": 5, "day_name": "Friday", "focus": "Answer generation", "task": "Connect retrieval results to an LLM and generate a grounded answer."},
                    {"day_number": 6, "day_name": "Saturday", "focus": "PDF Q&A", "task": "Build the PDF Q&A system and test it on several questions to see retrieval quality."},
                    {"day_number": 7, "day_name": "Sunday", "focus": "Documentation", "task": "Record how retrieval differs from plain generation and why grounding matters."},
                ],
            },
            {
                "number": 26,
                "title": "Better retrieval",
                "objective": "Improve retrieval quality using metadata, filtering, hybrid search, and reranking.",
                "days": [
                    {"day_number": 1, "day_name": "Monday", "focus": "Metadata and filtering", "task": "Learn how metadata and filters focus retrieval on relevant documents and segments."},
                    {"day_number": 2, "day_name": "Tuesday", "focus": "Hybrid search", "task": "Study hybrid search and compare keyword retrieval with vector retrieval."},
                    {"day_number": 3, "day_name": "Wednesday", "focus": "Reranking", "task": "Learn how reranking can improve the highest-quality chunks before answer generation."},
                    {"day_number": 4, "day_name": "Thursday", "focus": "System tuning", "task": "Tune the PDF Q&A system by improving chunk size, metadata, and retrieval logic."},
                    {"day_number": 5, "day_name": "Friday", "focus": "Evaluation", "task": "Run evaluation cases and note where retrieval is too broad or too narrow."},
                    {"day_number": 6, "day_name": "Saturday", "focus": "Improve the project", "task": "Upgrade the PDF system using metadata, filtering, and reranking strategies."},
                    {"day_number": 7, "day_name": "Sunday", "focus": "Review", "task": "Reflect on why better retrieval changes answer quality and reliability."},
                ],
            },
            {
                "number": 27,
                "title": "Advanced retrieval",
                "objective": "Move beyond simple retrieval toward query rewriting, multi-query retrieval, and context compression.",
                "days": [
                    {"day_number": 1, "day_name": "Monday", "focus": "Query rewriting", "task": "Learn how rewriting a user question improves retrieval quality and coverage."},
                    {"day_number": 2, "day_name": "Tuesday", "focus": "Multi-query retrieval", "task": "Study generating multiple queries and merging their retrieved evidence."},
                    {"day_number": 3, "day_name": "Wednesday", "focus": "Parent-child retrieval", "task": "Learn parent-child retrieval, when it is useful, and how it balances detail and context."},
                    {"day_number": 4, "day_name": "Thursday", "focus": "Context compression", "task": "Study how to compress retrieved context before sending it to the LLM."},
                    {"day_number": 5, "day_name": "Friday", "focus": "Advanced pipeline", "task": "Build an advanced retrieval pipeline with multiple queries and reranked evidence."},
                    {"day_number": 6, "day_name": "Saturday", "focus": "Project work", "task": "Extend the retrieval system and test improvements on difficult questions."},
                    {"day_number": 7, "day_name": "Sunday", "focus": "Documentation", "task": "Document which retrieval strategies help most, and which trade-offs appear in quality or cost."},
                ],
            },
            {
                "number": 28,
                "title": "RAG evaluation",
                "objective": "Judge retrieval and answer quality with evaluation metrics such as faithfulness, relevance, and groundedness.",
                "days": [
                    {"day_number": 1, "day_name": "Monday", "focus": "Retrieval evaluation", "task": "Learn how to measure retrieval quality using recall, precision, and ranking metrics."},
                    {"day_number": 2, "day_name": "Tuesday", "focus": "Answer evaluation", "task": "Study how to evaluate answers for correctness, groundedness, and helpfulness."},
                    {"day_number": 3, "day_name": "Wednesday", "focus": "Faithfulness and relevance", "task": "Understand faithfulness, relevance, and groundedness as quality dimensions for RAG systems."},
                    {"day_number": 4, "day_name": "Thursday", "focus": "Evidence requirements", "task": "Plan how the system will fetch and cite evidence for each answer."},
                    {"day_number": 5, "day_name": "Friday", "focus": "ABSU Knowledge Assistant", "task": "Build an ABSU Knowledge Assistant that uses student handbook, regulations, and course documents and cites evidence."},
                    {"day_number": 6, "day_name": "Saturday", "focus": "Evaluation pass", "task": "Run retrieval and answer evaluations, and inspect failures by type: retrieval, context, or generation."},
                    {"day_number": 7, "day_name": "Sunday", "focus": "Exit test", "task": "Explain whether a failure is due to retrieval quality, context construction, or the generation step."},
                ],
            },
        ],
    },
    {
        "title": "Phase 9 — Inference Engineering",
        "order": 9,
        "description": "Measure latency, throughput, batching, and memory to make models practical in production.",
        "weeks": [
            {
                "number": 29,
                "title": "Inference fundamentals",
                "objective": "Learn how inference changes with latency, throughput, batching, and GPU-memory constraints.",
                "days": [
                    {"day_number": 1, "day_name": "Monday", "focus": "Inference basics", "task": "Learn inference, latency, throughput, and why serving models is a different problem from training them."},
                    {"day_number": 2, "day_name": "Tuesday", "focus": "Batching", "task": "Study batching and throughput trade-offs for multiple requests served together."},
                    {"day_number": 3, "day_name": "Wednesday", "focus": "GPU memory", "task": "Learn how memory limits affect model size, sequence length, and batch size."},
                    {"day_number": 4, "day_name": "Thursday", "focus": "KV cache", "task": "Study the KV cache and why it matters for efficient autoregressive generation."},
                    {"day_number": 5, "day_name": "Friday", "focus": "Performance measurements", "task": "Measure model performance and collect latency and throughput before optimization."},
                    {"day_number": 6, "day_name": "Saturday", "focus": "Benchmarking", "task": "Benchmark a model on a realistic small workload and compare baseline results."},
                    {"day_number": 7, "day_name": "Sunday", "focus": "Documentation", "task": "Record the factors that influence inference quality and speed in production systems."},
                ],
            },
            {
                "number": 30,
                "title": "Optimization and serving",
                "objective": "Reduce latency and cost with quantization and optimized serving patterns.",
                "days": [
                    {"day_number": 1, "day_name": "Monday", "focus": "Quantization", "task": "Learn weight quantization and the trade-off between lower precision and accuracy."},
                    {"day_number": 2, "day_name": "Tuesday", "focus": "Model serving", "task": "Study serving patterns and the role of deployment architecture in inference performance."},
                    {"day_number": 3, "day_name": "Wednesday", "focus": "vLLM and caching", "task": "Learn about vLLM, paged attention, and caching for efficient generation."},
                    {"day_number": 4, "day_name": "Thursday", "focus": "Benchmarking", "task": "Build a small comparison between a base model and an optimized model."},
                    {"day_number": 5, "day_name": "Friday", "focus": "Cost analysis", "task": "Measure latency, throughput, memory, and computation cost for the optimized version."},
                    {"day_number": 6, "day_name": "Saturday", "focus": "Comparison project", "task": "Compare a model A versus optimized Model A and record the practical gains and trade-offs."},
                    {"day_number": 7, "day_name": "Sunday", "focus": "Exit test", "task": "Explain how to make an AI model fast and economical in production without sacrificing the user experience."},
                ],
            },
        ],
    },
    {
        "title": "Phase 10 — Context Engineering + MCP",
        "order": 10,
        "description": "Master context selection, memory, compression, and tool-ecosystem integration via MCP.",
        "weeks": [
            {
                "number": 31,
                "title": "Context engineering",
                "objective": "Optimize context windows, state, and memory for agent-quality reasoning.",
                "days": [
                    {"day_number": 1, "day_name": "Monday", "focus": "Context windows", "task": "Study context limits and the trade-off between more context and more noise."},
                    {"day_number": 2, "day_name": "Tuesday", "focus": "Context selection", "task": "Learn how to choose only the most relevant context and examples for a task."},
                    {"day_number": 3, "day_name": "Wednesday", "focus": "State and memory", "task": "Understand how state, memory, and tool results shape the active reasoning window."},
                    {"day_number": 4, "day_name": "Thursday", "focus": "Compression", "task": "Learn when to compress context and which summaries preserve essential information."},
                    {"day_number": 5, "day_name": "Friday", "focus": "Agent optimization", "task": "Take your agent and optimize its context using more selective inputs and summaries."},
                    {"day_number": 6, "day_name": "Saturday", "focus": "Before vs after", "task": "Measure the change in context quality and reasoning before and after the optimization steps."},
                    {"day_number": 7, "day_name": "Sunday", "focus": "Documentation", "task": "Write down your runbook for context selection, summarization, and memory hygiene."},
                ],
            },
            {
                "number": 32,
                "title": "MCP",
                "objective": "Learn the Model Context Protocol architecture and how clients, servers, tools, resources, and prompts connect.",
                "days": [
                    {"day_number": 1, "day_name": "Monday", "focus": "MCP architecture", "task": "Learn the core MCP architecture: client, server, tools, resources, and prompts."},
                    {"day_number": 2, "day_name": "Tuesday", "focus": "Tools and resources", "task": "Design a simple tool and resource contract and understand how they differ."},
                    {"day_number": 3, "day_name": "Wednesday", "focus": "Prompt design", "task": "Study how MCP encourages structured prompt and context delivery."},
                    {"day_number": 4, "day_name": "Thursday", "focus": "Example server", "task": "Build your first MCP server with a single useful tool or capability."},
                    {"day_number": 5, "day_name": "Friday", "focus": "Client integration", "task": "Connect an AI agent or client to the MCP server and verify tool invocation works."},
                    {"day_number": 6, "day_name": "Saturday", "focus": "Testing", "task": "Test the server under realistic tool calls and inspect failure responses."},
                    {"day_number": 7, "day_name": "Sunday", "focus": "Explanation", "task": "Explain why MCP exists and what problem it solves in tool-based agent systems."},
                ],
            },
            {
                "number": 33,
                "title": "ABSU MCP",
                "objective": "Turn the ABSU workflow into an MCP-powered system with real tools and structured interactions.",
                "days": [
                    {"day_number": 1, "day_name": "Monday", "focus": "System design", "task": "Design the ABSU MCP server: check_result, register_course, get_courses, create_invoice, and get_student."},
                    {"day_number": 2, "day_name": "Tuesday", "focus": "Tool implementation", "task": "Implement the student-related tools and validate each one independently."},
                    {"day_number": 3, "day_name": "Wednesday", "focus": "Resources", "task": "Expose resource-like data such as student info and course catalog to the agent."},
                    {"day_number": 4, "day_name": "Thursday", "focus": "Client integration", "task": "Connect an AI agent to the ABSU MCP server and send a realistic student task."},
                    {"day_number": 5, "day_name": "Friday", "focus": "Evaluation", "task": "Run end-to-end tasks and inspect if the system chooses the correct tool, uses the result, and completes well."},
                    {"day_number": 6, "day_name": "Saturday", "focus": "Hardening", "task": "Improve validation, retries, and failure reporting for tool execution."},
                    {"day_number": 7, "day_name": "Sunday", "focus": "Abstract explanation", "task": "Write a clear explanation of why MCP exists and how it standardizes tool access for agents."},
                ],
            },
        ],
    },
    {
        "title": "Phase 11 — Loop / Harness Engineering",
        "order": 11,
        "description": "Build reliable agent loops, state machines, and verification flows that survive failure and recovery.",
        "weeks": [
            {
                "number": 34,
                "title": "Reliable agent loop",
                "objective": "Design loops with state machines, retries, termination, and error recovery.",
                "days": [
                    {"day_number": 1, "day_name": "Monday", "focus": "Agent loops", "task": "Learn how state machines model repeated reasoning, tool use, and termination."},
                    {"day_number": 2, "day_name": "Tuesday", "focus": "Retry and recovery", "task": "Study retries, timeouts, and failure recovery in AI workflows."},
                    {"day_number": 3, "day_name": "Wednesday", "focus": "Termination", "task": "Design conditions for stopping a loop once the task is complete or impossible."},
                    {"day_number": 4, "day_name": "Thursday", "focus": "Reliability", "task": "Implement a reliable loop that handles tool errors and unexpected outputs gracefully."},
                    {"day_number": 5, "day_name": "Friday", "focus": "Build loop", "task": "Build a Reliable Agent Loop with controlled retry logic and state transitions."},
                    {"day_number": 6, "day_name": "Saturday", "focus": "Failure analysis", "task": "Test edge cases where the loop stalls or chooses the wrong action repeatedly."},
                    {"day_number": 7, "day_name": "Sunday", "focus": "Documentation", "task": "Document how state, termination, and recovery make an agent loop robust enough for real use."},
                ],
            },
            {
                "number": 35,
                "title": "Verification and autonomy",
                "objective": "Add verification, self-checking, human approval, and evaluation to an autonomous task agent.",
                "days": [
                    {"day_number": 1, "day_name": "Monday", "focus": "Verification", "task": "Study verification and self-checking steps that confirm the task is actually complete."},
                    {"day_number": 2, "day_name": "Tuesday", "focus": "Human approval", "task": "Learn when approval gates are necessary before making risky or irreversible decisions."},
                    {"day_number": 3, "day_name": "Wednesday", "focus": "Failure recovery", "task": "Design correction loops when the agent fails, misunderstands, or gets stuck."},
                    {"day_number": 4, "day_name": "Thursday", "focus": "Evaluation", "task": "Build a rubric to measure whether actions succeed and whether the model corrected itself."},
                    {"day_number": 5, "day_name": "Friday", "focus": "Autonomous Task Agent", "task": "Build an Autonomous Task Agent that plans, executes, verifies, corrects, and finishes a multi-step task."},
                    {"day_number": 6, "day_name": "Saturday", "focus": "Failure log", "task": "Record every failure mode and explain how the system recovered or failed again."},
                    {"day_number": 7, "day_name": "Sunday", "focus": "Reflection", "task": "Document the verification loop and the difference between a functioning agent and a brittle one."},
                ],
            },
        ],
    },
    {
        "title": "Phase 12 — MLOps / LLMOps",
        "order": 12,
        "description": "Study infrastructure, deployment, evaluation, and production engineering for AI systems.",
        "weeks": [
            {
                "number": 36,
                "title": "Docker + deployment",
                "objective": "Containerize and deploy AI components in an environment that matches production realities.",
                "days": [
                    {"day_number": 1, "day_name": "Monday", "focus": "Docker and containers", "task": "Learn Docker, containers, and why they provide reproducible AI deployments."},
                    {"day_number": 2, "day_name": "Tuesday", "focus": "Environment variables", "task": "Study configuration via environment variables and how they separate code from runtime setup."},
                    {"day_number": 3, "day_name": "Wednesday", "focus": "Production config", "task": "Document the settings required for production deployments of AI apps."},
                    {"day_number": 4, "day_name": "Thursday", "focus": "Containerization", "task": "Containerize your AI application and verify that it runs without a local-only setup."},
                    {"day_number": 5, "day_name": "Friday", "focus": "Deployment basics", "task": "Review deployment architecture with a small production mindset."},
                    {"day_number": 6, "day_name": "Saturday", "focus": "Project work", "task": "Deploy the application and record the configuration needed for a clean run."},
                    {"day_number": 7, "day_name": "Sunday", "focus": "Review", "task": "Document the deployment design and the environment assumptions that matter most."},
                ],
            },
            {
                "number": 37,
                "title": "Observability",
                "objective": "Instrument AI systems with logs, metrics, tracing, and operational insight.",
                "days": [
                    {"day_number": 1, "day_name": "Monday", "focus": "Logging", "task": "Learn logging patterns and which events matter for AI applications."},
                    {"day_number": 2, "day_name": "Tuesday", "focus": "Metrics", "task": "Study latency, throughput, error rate, and usage metrics for model-backed systems."},
                    {"day_number": 3, "day_name": "Wednesday", "focus": "Tracing", "task": "Understand traces and correlation IDs across tool calls and model requests."},
                    {"day_number": 4, "day_name": "Thursday", "focus": "Token usage", "task": "Track token counts, prompt size, and model cost across realistic tasks."},
                    {"day_number": 5, "day_name": "Friday", "focus": "Observability implementation", "task": "Add logs and metrics to your agent and review the output of its operational signals."},
                    {"day_number": 6, "day_name": "Saturday", "focus": "Performance review", "task": "Analyze the operational telemetry for errors, bottlenecks, and unexpected behaviors."},
                    {"day_number": 7, "day_name": "Sunday", "focus": "Documentation", "task": "Write a monitoring plan covering logs, metrics, tracing, and cost observability."},
                ],
            },
            {
                "number": 38,
                "title": "Evaluation + CI/CD",
                "objective": "Move from ad hoc experiments to automated evaluation, regression tests, and service deployment.",
                "days": [
                    {"day_number": 1, "day_name": "Monday", "focus": "Automated evaluation", "task": "Build evaluation scripts and test cases that check prompt and model behavior automatically."},
                    {"day_number": 2, "day_name": "Tuesday", "focus": "Regression tests", "task": "Learn how to run regression checks to catch prompt or model regressions early."},
                    {"day_number": 3, "day_name": "Wednesday", "focus": "Prompt and model versioning", "task": "Study prompt and model versioning and why reproducibility matters in AI systems."},
                    {"day_number": 4, "day_name": "Thursday", "focus": "CI/CD", "task": "Design a simple CI/CD process for an AI service so deployments stay controlled and repeatable."},
                    {"day_number": 5, "day_name": "Friday", "focus": "Production service", "task": "Deploy your AI application as a production service and validate its health checks."},
                    {"day_number": 6, "day_name": "Saturday", "focus": "Operational rollout", "task": "Run the service through a production-like workflow and document what needs monitoring."},
                    {"day_number": 7, "day_name": "Sunday", "focus": "Summary", "task": "Summarize the end-to-end operational lifecycle for AI systems in production."},
                ],
            },
        ],
    },
    {
        "title": "Phase 13 — Agentic RAG",
        "order": 13,
        "description": "Combine LLMs, tools, memory, retrieval, context design, and evaluation into autonomous research systems.",
        "weeks": [
            {
                "number": 39,
                "title": "Autonomous research agent",
                "objective": "Build an agentic system that plans research, searches, retrieves, evaluates, and synthesizes evidence.",
                "days": [
                    {"day_number": 1, "day_name": "Monday", "focus": "Architecture", "task": "Combine LLM, RAG, tools, and memory into a research pipeline with explicit steps."},
                    {"day_number": 2, "day_name": "Tuesday", "focus": "Planning and search", "task": "Design planning, research, and retrieval phases with clear input and output contracts."},
                    {"day_number": 3, "day_name": "Wednesday", "focus": "Evaluation", "task": "Add evidence evaluation and logic for deciding when more research is needed."},
                    {"day_number": 4, "day_name": "Thursday", "focus": "Synthesis", "task": "Build a synthesis stage that uses retrieved evidence to answer with clear, cited reasoning."},
                    {"day_number": 5, "day_name": "Friday", "focus": "Citations", "task": "Implement citations so every answer can point to source material or evidence."},
                    {"day_number": 6, "day_name": "Saturday", "focus": "Project build", "task": "Build the Autonomous Research Agent and test it on multi-step questions requiring research."},
                    {"day_number": 7, "day_name": "Sunday", "focus": "Portfolio documentation", "task": "Document the system architecture, evidence flow, and lessons learned for portfolio use."},
                ],
            },
        ],
    },
    {
        "title": "Phase 14 — Capstone + Portfolio",
        "order": 14,
        "description": "Finalize the strongest portfolio projects across student agents, knowledge assistants, and autonomous research systems.",
        "weeks": [
            {
                "number": 40,
                "title": "Capstone + portfolio",
                "objective": "Build the final portfolio pieces and present your AI engineering journey through practical projects.",
                "days": [
                    {"day_number": 1, "day_name": "Monday", "focus": "Project 1", "task": "Finalize ABSU Student Agent with tools, APIs, and a realistic university workflow."},
                    {"day_number": 2, "day_name": "Tuesday", "focus": "Project 2", "task": "Finalize ABSU Knowledge Assistant with RAG, retrieval, reranking, evaluation, and citations."},
                    {"day_number": 3, "day_name": "Wednesday", "focus": "Project 3", "task": "Finalize the Autonomous Research Agent with planning, tools, RAG, and evaluation loops."},
                    {"day_number": 4, "day_name": "Thursday", "focus": "Integration", "task": "Connect the major portfolio projects into a coherent demonstration with architecture notes and operational details."},
                    {"day_number": 5, "day_name": "Friday", "focus": "Documentation", "task": "Prepare polished documentation, screenshots, architecture diagrams, and challenge notes for each project."},
                    {"day_number": 6, "day_name": "Saturday", "focus": "Portfolio polish", "task": "Refine the code, demos, and explanation of the full AI engineering journey as a strong portfolio story."},
                    {"day_number": 7, "day_name": "Sunday", "focus": "Presentation", "task": "Present the final portfolio, explain the stack and decisions, and summarize the biggest lessons learned from the full roadmap."},
                ],
            },
        ],
    },
]

PROJECTS = [
    ("ABSU Student Agent", "An AI agent that interacts with university-related tools such as checking results, registering courses, creating invoices, and printing receipts."),
    ("ABSU Knowledge / PDF RAG Assistant", "A RAG-based assistant that answers questions from university documents and provides grounded answers with evidence."),
    ("Autonomous Research Agent", "An agentic research system capable of planning research, retrieving information, evaluating evidence, and producing a cited answer."),
]


class Command(BaseCommand):
    help = "Create the comprehensive 40-week AI engineering roadmap and starter projects."

    def add_arguments(self, parser):
        parser.add_argument("--start-date", type=str, help="First roadmap day (YYYY-MM-DD); defaults to today.")

    @transaction.atomic
    def handle(self, *args, **options):
        start = timezone.localdate()
        if options["start_date"]:
            from datetime import date
            start = date.fromisoformat(options["start_date"])

        for section_data in CURRICULUM:
            section, _ = Section.objects.update_or_create(
                order=section_data["order"],
                defaults={
                    "title": section_data["title"],
                    "description": section_data["description"],
                },
            )

            for week_data in section_data["weeks"]:
                week, _ = Week.objects.update_or_create(
                    number=week_data["number"],
                    defaults={
                        "section": section,
                        "title": week_data["title"],
                        "objective": week_data["objective"],
                    },
                )

                for day_data in week_data["days"]:
                    day, _ = Day.objects.update_or_create(
                        week=week,
                        day_number=day_data["day_number"],
                        defaults={
                            "title": f"{day_data['day_name']} — {day_data['focus']}",
                            "date": start + timedelta(days=(week.number - 1) * 7 + day_data["day_number"] - 1),
                        },
                    )
                    Task.objects.update_or_create(
                        day=day,
                        order=1,
                        defaults={
                            "title": f"{week.title}: {day_data['focus']}",
                            "description": day_data["task"],
                        },
                    )

        for title, description in PROJECTS:
            Project.objects.get_or_create(title=title, defaults={"description": description})

        self.stdout.write(self.style.SUCCESS("Seeded the comprehensive 40-week AI engineering roadmap, 280 days, and starter projects."))
