# 🌱 Touch Grass AI: An Offline Garden Planner Powered by Open-Weight Models

*This is a submission for the [Hacktoberfest Open-Source AI Challenge Week 1: Touch Grass](https://dev.to/challenges/hacktoberfest-week1-2026-10-05)*

## What I Built

**Touch Grass AI is an open-source garden planner that helps people spend less time researching gardening online and more time actually growing things.**

It uses locally running, open-weight language models to provide planting recommendations, weekly gardening calendars, frost-date information, and answers to common gardening questions.

Instead of depending on a cloud-based AI assistant, the application runs inference on your own machine. Once the model and required gardening data are downloaded, you can use the core planner without an internet connection.

Whether you're starting a vegetable garden, planning seasonal crops, or trying to figure out what to plant this week, Touch Grass AI helps turn gardening questions into practical outdoor tasks.

### 🌿 Features

- 🌱 **Local frost-date calculations:** Use locally cached frost-date data to help plan around the growing season.
- 🪴 **Plant recommendations:** Find plants suited to your growing zone, season, and garden conditions.
- 📅 **Weekly planting calendar:** Plan what to sow, transplant, harvest, and avoid.
- 🤖 **Offline AI gardening assistant:** Ask questions about planting times, pests, companion planting, and more.
- 🔒 **Privacy-first design:** Enter your location manually without requiring GPS access.
- 🧠 **Model flexibility:** Experiment with compatible GGUF models, including Llama, Mistral, Phi, and Gemma.
- 🌐 **Offline operation:** Keep gardening information available when connectivity is unavailable, after the required assets have been downloaded.

The idea is simple: open the planner, get your gardening tasks, put your phone away, and get your hands dirty.

## Code

💻 **GitHub Repository:** [parichay29/touch-grass-ai](https://github.com/parichay29/touch-grass-ai)

The project is organized into modular Python components so developers can experiment with models, planting data, frost-date logic, and prompts independently.

Contributions, feedback, and suggestions are welcome!

## How I Built It

The core design principle is that the AI should run locally rather than act as a thin wrapper around a proprietary cloud API.

### Technology Stack

- **Python:** Application logic and command-line interface.
- **llama.cpp:** Local inference for compatible GGUF model files.
- **Open-weight language models:** Phi, Llama, Mistral, and Gemma variants for gardening assistance.
- **Local plant database:** Planting schedules, companion relationships, and common pest information.
- **Cached frost-date data:** Locally available seasonal information for planning.
- **Custom prompts:** Instructions that guide the model toward practical, gardening-focused answers.

### Architecture

```text
touch-grass-ai/
├── garden_planner.py       # Main CLI application
├── download_model.py       # Model downloader
├── frost_dates.py          # Offline frost-date calculator
├── plant_database.py       # Plant data and gardening knowledge
├── llm_engine.py           # Local inference with llama.cpp
├── prompts.py              # System prompts for garden advice
├── cache/                  # Cached data and model weights
└── requirements.txt
```

Each component has a distinct responsibility:

- `garden_planner.py` coordinates the application and user interaction.
- `download_model.py` downloads the selected model during setup.
- `frost_dates.py` handles frost-date information and seasonal calculations.
- `plant_database.py` provides structured gardening knowledge.
- `llm_engine.py` runs local model inference through llama.cpp.
- `prompts.py` defines the assistant's gardening behavior.

The separation between structured data and language-model inference is deliberate. Planting dates and frost calculations should come from the application's data and logic wherever possible, while the model makes the information easier to understand and helps answer natural-language questions.

### Quick Start

**1. Install dependencies**

```bash
pip install -r requirements.txt
```

**2. Download a model**

```bash
python download_model.py --model phi-3-mini-4k-instruct-q4
```

This is a one-time setup step that downloads the model weights.

**3. Run the garden planner**

```bash
python garden_planner.py --zip 90210
```

The initial setup requires downloading the model and any external data the application needs. Once those assets are available locally, the planner can operate offline to the extent supported by its implementation.

## Example Usage

Imagine opening the planner before heading out to your garden.

```text
$ python garden_planner.py --zip 97202

🌱 Touch Grass AI - Garden Planner
Growing zone: 8b
Last frost: March 15
First frost: November 15

📅 THIS WEEK
  ✅ Plant: Garlic, suitable cover crops
  ✅ Transplant: Kale, spinach where conditions permit
  ✅ Harvest: Seasonal crops that are ready
  🛑 Review: Frost-sensitive plants and upcoming cold weather

💬 Ask me anything:
"What cover crop fixes nitrogen best?"

> Crimson clover can fix atmospheric nitrogen.
> Consider your local planting window and soil conditions
  when selecting a cover crop.

💬 Ask me:
"Companions for garlic?"

> Explore companion options such as carrots, beets,
  and spinach, and check the local plant database
  for compatibility and growing recommendations.
```

The local AI assistant helps explain gardening options, compare approaches, and suggest practical next steps using the available gardening information.

Exact recommendations depend on the local dataset, growing conditions, and selected model. Gardening advice should always be checked against local conditions.

## Models Tested

The following are candidate model configurations and indicative performance figures. Actual performance depends on hardware, inference settings, quantization, and model versions.

| Model | Approx. model size | Intended use |
|---|---:|---|
| Phi-3 Mini 4K Instruct Q4 | 2.3 GB | Compact local assistant |
| Llama 3.2 3B Instruct Q4 | 2.0 GB | General gardening questions |
| Mistral 7B Instruct v0.3 Q4 | 4.1 GB | More demanding responses |
| Gemma 2 2B Instruct Q4 | 1.6 GB | Lightweight inference |

CPU tokens-per-second figures should be included only after benchmarking each model on documented hardware. Model compatibility and licenses should also be checked before distributing model weights.

## Why Does Open Innovation Matter?

This is the most important part of the project for me.

Gardening is inherently local. Planting calendars, growing conditions, and seasonal decisions are personal to your garden. I wanted to explore what happens when an AI application can operate without requiring that information to be sent to a cloud service.

### 🔒 1. Your garden data stays on your device

A local-first architecture means the core gardening workflow doesn't need a third-party AI API. Location inputs, preferences, and gardening questions can remain on the machine.

### 📴 2. Offline access is a real feature

Gardens, allotments, and hiking areas don't always have reliable connectivity. Downloading the model and required data ahead of time makes the planner useful in those situations.

### 🧠 3. Models are replaceable

I'm not locked into one model provider. Compatible GGUF models can be evaluated and swapped based on response quality, hardware requirements, speed, and memory usage.

This also makes it possible for contributors to experiment with different model families and share improvements.

### 💸 4. No per-request API charges

Local inference avoids usage-based charges from hosted model APIs. The trade-off is that users need compatible hardware, storage, and power to run inference themselves.

### 🛠️ 5. The application is open to modification

The prompts, Python logic, plant database, and model configuration can be inspected and adapted. Contributors can add regional plant knowledge, improve planting recommendations, or change the assistant's behavior without depending entirely on a proprietary service.

**Open innovation makes this project more than a gardening chatbot. It makes it a customizable, locally controlled tool that can remain useful without a permanent connection to a cloud provider.**

## What's Next?

I'd like to explore better regional planting datasets, improved seasonal recommendations, more reliable companion-planting information, and a simpler interface for gardeners who don't want to use a command line.

The larger goal is to make local AI useful in everyday life, beyond productivity apps and chat interfaces.

Instead of using AI to spend another hour on a screen, use it to decide what to plant, step outside, and grow something.

**Less scrolling. More growing. 🌱**

#Hacktoberfest #OpenSourceAI #LocalAI #Python #TouchGrass