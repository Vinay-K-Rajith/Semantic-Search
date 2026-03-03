"""
Sample document corpus for the semantic search demo.
Each document has a title and body text.
"""

DOCUMENTS = [
    {
        "id": 0,
        "title": "Introduction to Neural Networks",
        "text": "Neural networks are computational models inspired by the human brain. They consist of interconnected layers of nodes (neurons) that learn patterns from data through a process called backpropagation and gradient descent.",
    },
    {
        "id": 1,
        "title": "Transformer Architecture",
        "text": "The Transformer is a deep learning model introduced in 2017 that relies on self-attention mechanisms, allowing it to process sequences in parallel. It underpins models like BERT, GPT, and T5.",
    },
    {
        "id": 2,
        "title": "FAISS: Efficient Similarity Search",
        "text": "FAISS (Facebook AI Similarity Search) is a library developed by Meta AI for efficient similarity search and clustering of dense vectors. It supports billion-scale datasets and is widely used in production retrieval systems.",
    },
    {
        "id": 3,
        "title": "Sentence Embeddings",
        "text": "Sentence embeddings map variable-length sentences into fixed-size dense vectors in a high-dimensional semantic space. Models like SentenceBERT and all-MiniLM achieve state-of-the-art performance on semantic similarity benchmarks.",
    },
    {
        "id": 4,
        "title": "Convolutional Neural Networks in Vision",
        "text": "CNNs apply learnable filters across spatial dimensions of images to extract hierarchical feature representations. They are the backbone of image classification, object detection, and segmentation tasks.",
    },
    {
        "id": 5,
        "title": "Reinforcement Learning Fundamentals",
        "text": "Reinforcement learning trains agents to maximise cumulative reward through trial-and-error interactions with an environment. Key algorithms include Q-learning, PPO, and DDPG.",
    },
    {
        "id": 6,
        "title": "Natural Language Processing Overview",
        "text": "NLP enables computers to understand, interpret, and generate human language. Core tasks include tokenisation, named entity recognition, sentiment analysis, machine translation, and question answering.",
    },
    {
        "id": 7,
        "title": "Graph Neural Networks",
        "text": "GNNs operate directly on graph-structured data such as social networks, molecular graphs, and knowledge bases. They aggregate neighbour information to produce node, edge, or graph-level representations.",
    },
    {
        "id": 8,
        "title": "Generative Adversarial Networks",
        "text": "GANs consist of a generator and a discriminator trained in an adversarial fashion. GANs can synthesise photorealistic images, perform style transfer, and generate audio and video content.",
    },
    {
        "id": 9,
        "title": "Large Language Models",
        "text": "LLMs are transformer-based models with billions of parameters pretrained on vast text corpora. GPT-4, Claude, and Gemini demonstrate emergent reasoning, code generation, and in-context learning abilities.",
    },
    {
        "id": 10,
        "title": "DNA and Genetic Code",
        "text": "DNA is a double-helix polymer encoding genetic instructions for the development and function of all known organisms. The four nucleotide bases — adenine, thymine, cytosine, and guanine — form complementary base pairs.",
    },
    {
        "id": 11,
        "title": "Quantum Computing Basics",
        "text": "Quantum computers use qubits that can exist in superposition, allowing massive parallelism. Algorithms like Shor's factoring algorithm and Grover's search algorithm offer exponential speedups over classical counterparts.",
    },
    {
        "id": 12,
        "title": "Climate Change and Global Warming",
        "text": "Anthropogenic greenhouse gas emissions, particularly CO₂ and methane, trap solar radiation and raise global temperatures. Consequences include sea-level rise, extreme weather events, and ecosystem disruption.",
    },
    {
        "id": 13,
        "title": "Black Holes and Spacetime",
        "text": "Black holes are regions of spacetime where gravity is so strong that nothing, not even light, can escape beyond the event horizon. They form when massive stars collapse under their own gravity.",
    },
    {
        "id": 14,
        "title": "The Human Immune System",
        "text": "The immune system defends the body against pathogens via innate and adaptive immunity. B cells produce antibodies, while T cells coordinate cellular responses and destroy infected or cancerous cells.",
    },
    {
        "id": 15,
        "title": "CRISPR Gene Editing",
        "text": "CRISPR-Cas9 is a molecular tool that edits DNA at specific locations using guide RNA and an endonuclease. It holds promise for treating genetic diseases, developing new crops, and studying gene function.",
    },
    {
        "id": 16,
        "title": "The Industrial Revolution",
        "text": "The Industrial Revolution (1760–1840) transformed manufacturing from hand production to machine-based processes, driven by steam power, mechanised textile production, and iron and steel industries in Britain.",
    },
    {
        "id": 17,
        "title": "Python Programming Language",
        "text": "Python is a high-level, dynamically-typed general-purpose programming language known for its readability. It dominates data science, machine learning, and web development ecosystems.",
    },
    {
        "id": 18,
        "title": "REST API Design Principles",
        "text": "REST (Representational State Transfer) is an architectural style for distributed hypermedia systems. Key constraints include statelessness, uniform interface, client-server separation, and layered system design.",
    },
    {
        "id": 19,
        "title": "Docker and Containerisation",
        "text": "Docker packages applications and their dependencies into lightweight containers, ensuring consistent runtime environments across development, staging, and production. Kubernetes orchestrates container fleets at scale.",
    },
    {
        "id": 20,
        "title": "Photosynthesis in Plants",
        "text": "Photosynthesis converts sunlight, water, and carbon dioxide into glucose and oxygen. It occurs in two stages: the light-dependent reactions in the thylakoid membrane and the Calvin cycle in the stroma.",
    },
    {
        "id": 21,
        "title": "The Theory of Relativity",
        "text": "Einstein's special relativity postulates that the speed of light is constant and that time dilates and length contracts at relativistic speeds. General relativity describes gravity as the curvature of spacetime.",
    },
    {
        "id": 22,
        "title": "Stock Markets and Financial Instruments",
        "text": "Stock exchanges facilitate the buying and selling of equity securities. Instruments include common shares, bonds, ETFs, options, and futures. Market capitalisation reflects investor expectations of future earnings.",
    },
    {
        "id": 23,
        "title": "Machine Learning Model Evaluation",
        "text": "Model evaluation metrics include accuracy, precision, recall, F1-score, ROC-AUC for classification, and MAE, RMSE for regression. Cross-validation and held-out test sets prevent overfitting evaluation.",
    },
    {
        "id": 24,
        "title": "Blockchain Technology",
        "text": "A blockchain is a distributed, immutable ledger of transactions secured by cryptographic hashing and consensus mechanisms such as Proof of Work or Proof of Stake. It underpins cryptocurrencies and smart contracts.",
    },
    {
        "id": 25,
        "title": "Human Brain Anatomy",
        "text": "The brain is divided into the cerebrum, cerebellum, and brainstem. The cerebral cortex handles higher cognition. The limbic system regulates emotion and memory, while the brainstem controls vital autonomic functions.",
    },
    {
        "id": 26,
        "title": "Autonomous Vehicles",
        "text": "Self-driving cars use sensor fusion (cameras, LIDAR, radar), deep learning for perception, and planning algorithms for navigation. SAE levels define automation from driver assistance (L1) to full automation (L5).",
    },
    {
        "id": 27,
        "title": "Antibiotic Resistance",
        "text": "Antibiotic resistance arises when bacteria evolve mechanisms to survive drug treatment through mutations or horizontal gene transfer. Overuse of antibiotics in medicine and agriculture accelerates this global health threat.",
    },
    {
        "id": 28,
        "title": "Microservices Architecture",
        "text": "Microservices decompose applications into small, independently deployable services that communicate via APIs. This improves scalability and fault isolation but introduces complexity in service discovery and data consistency.",
    },
    {
        "id": 29,
        "title": "The Standard Model of Particle Physics",
        "text": "The Standard Model classifies elementary particles into quarks, leptons, and bosons. It explains three of the four fundamental forces — electromagnetic, weak, and strong — and is validated by the discovery of the Higgs boson.",
    },
]
