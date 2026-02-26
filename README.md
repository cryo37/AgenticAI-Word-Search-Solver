# AgenticAI-Word-Search-Solver
An agentic AI pipeline that extracts, parses, and deterministically solves word search puzzles using Groq Vision and Langflow.

# Word Search Puzzle Solver  
### Agentic AI Project — DataStax Langflow + Groq Vision

A multi-agent AI system that:

- Reads a word search puzzle from an image
- Extracts the letter grid using Groq Vision
- Parses the grid into structured data
- Solves the puzzle algorithmically (8 directions)
- Returns a color-highlighted HTML visualization

---

# Problem Statement

Given a word search puzzle image, build an agentic system that:

1. Extracts the letter grid using Vision AI
2. Structures it into a 2D matrix
3. Searches for target words in all 8 directions
4. Returns solved results with highlighted letters

---

# Architecture
```
Chat Input (Image URL)
↓
Image URL → Base64 Converter
↓
Groq Vision (Llama 4 Maverick)
↓
Groq Text Model (Cleanup / Structuring)
↓
Word Grid Finder (Custom Python Component)
↓
Chat Output (HTML Visualization)
```

---

# How It Works

### Step 1 — Vision OCR  
Groq Vision extracts the raw letter grid from the image.

### Step 2 — Grid Structuring  
Text is cleaned and converted into a structured 2D array.

### Step 3 — Deterministic Word Search  
The solver scans every cell in all 8 directions:

- Horizontal → ←
- Vertical ↑ ↓
- Diagonal ↘ ↙ ↗ ↖

### Step 4 — Visualization  
The grid is rendered as an HTML table with:
- Unique color per word
- Direction indicators
- Not-found word list

---

# Default Word List (Marvel Theme)

IRONMAN, THOR, HULK, SPIDERMAN, THANOS,  
VISION, WANDA, LOKI, GROOT, ROCKET,  
GAMORA, DRAX, ANTMAN, WASP, FALCON,  
PANTHER, NEBULA, HAWKEYE, BLACKWIDOW,  
STARLORD, MANTIS, SHURI, PEPPER,  
FURY, STARK, ROGERS, MARVEL, AVENGERS  

---

# Setup

## Prerequisites

- DataStax Langflow account
- Groq API key

## Flow Components Order

1. Chat Input
2. Image URL to Base64
3. Groq Vision
4. Groq Text Model
5. Word Grid Finder (Custom Component)
6. Chat Output

---

# Repository Structure
```
word-search-agentic-ai/
│
├── README.md
├── AgentSpec.md
├── Interaction.md
│
├── components/
│ ├── word_grid_finder.py
│
├── prompts/
│ ├── vision_prompt.txt
│
└── examples/
├── sample_input.jpg
├── sample_output.html
```


---

# Why Deterministic Algorithm?

LLMs hallucinate grid coordinates.  
This project uses a custom Python solver to guarantee:

- Accurate indexing
- No hallucinated positions
- Repeatable results
- Production-safe logic

---

# Notes

- One image processed per request
- No data storage
- OCR accuracy depends on image clarity
- Works best when image is cropped to grid only

