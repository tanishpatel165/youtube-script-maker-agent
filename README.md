# YouTube Script Maker Agent

A multi-agent pipeline built with Google ADK and Groq (via LiteLLM) that takes a video topic and produces a complete YouTube package.

## How it works
SequentialAgent with 4 LLM agents:
1. Research agent: facts, stats, stories
2. Structure agent: hook, sections, climax, outro
3. Script writer agent: 8-10 min script with B-roll and music cues
4. Thumbnail agent: titles, thumbnail ideas, descriptions, hashtags

## Setup
pip install -r requirements.txt
Copy .env.example to .env and add your keys.

## Run
adk web
Select youtube_search_agent and enter a topic.