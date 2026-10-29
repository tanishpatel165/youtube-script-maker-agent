import os
from dotenv import load_dotenv
from google.adk.agents import LlmAgent, SequentialAgent
from google.adk.models.lite_llm import LiteLlm

load_dotenv()
MODEL = LiteLlm(model="groq/openai/gpt-oss-20b")

# RESEARCH AGENT 
research_agent = LlmAgent(
    name='research_agent',
    model=MODEL,
    instruction="""You are a YouTube research specialist. When given a video topic, provide:
        Your job:
        - Research the topic deeply
        - Find 10 interesting and surprising facts
        - Find real world examples and stories
        - Find statistics and data
        - Think about what viewers would find most interesting
        Output everything as detailed research notes.
        Be thorough — the script writer depends on your research.""",
        output_key="raw_research",
        )

# Structure agent 
structure_agent = LlmAgent(
    name="structure_agent",
    model=MODEL,
    instruction="""You are a YouTube video structure expert.
        Use this research to create a video structure:
        {raw_research}

        Create this exact structure:

        HOOK (0-30 sec):
        - One shocking fact or question to grab attention

        INTRO (30 sec - 1 min):
        - What this video is about
        - Why viewer should watch till end

        SECTION 1 - [Title]:
        - Key points to cover

        SECTION 2 - [Title]:
        - Key points to cover

        SECTION 3 - [Title]:
        - Key points to cover

        CLIMAX:
        - Most exciting/surprising part

        OUTRO (last 1 min):
        - Summary
        - Call to action (like, subscribe, comment)

        Keep it engaging for a general audience.""",
        output_key="script_structure",
    )


# Script writing agent
script_writer_agent = LlmAgent(
    name="script_writer_agent",
    model=MODEL,
    instruction="""You are a professional YouTube script writer.
                Use this structure to write a full script:
                {script_structure}

                Also use this research for facts and details:
                {raw_research}

                Rules:
                - Write in a conversational, friendly tone
                - Use "you" and "we" to connect with viewer
                - Add [PAUSE] where presenter should pause
                - Add [B-ROLL: description] where visuals should change
                - Add [MUSIC: mood] where background music changes
                - Make it 8-10 minutes long (around 1200-1500 words)
                - Start every section with an engaging transition

                Format:
                [SECTION NAME]
                Script text here...
                [B-ROLL: what to show]
                More script...

                Write the complete ready-to-record script.""",
                    output_key="full_script",
                )


# Thumbnail and title agent

thumbnail_agent = LlmAgent(
    name="thumbnail_agent",
    model=MODEL,
    instruction="""You are a YouTube thumbnail and title expert.
        Read this script and create:
        {full_script}

        Give me:

        5 CATCHY TITLES:
        (Use numbers, questions, or shocking statements)
        1. ...
        2. ...
        3. ...
        4. ...
        5. ...

        5 THUMBNAIL IDEAS:
        (Describe exactly what should be in the image)
        1. ...
        2. ...
        3. ...
        4. ...
        5. ...

        3 DESCRIPTION IDEAS:
        (First 2 lines are most important for SEO)
        1. ...
        2. ...
        3. ...

        10 HASHTAGS:
        #... #... #...

        Pick the BEST title and thumbnail and explain why.""",
            output_key="thumbnail_ideas",
        )


root_agent = SequentialAgent(
    name="youtube_script_maker",
    sub_agents=[
        research_agent,       # Step 1 - Research
        structure_agent,      # Step 2 - Structure banao
        script_writer_agent,  # Step 3 - Script likho
        thumbnail_agent,      # Step 4 - Titles + Thumbnails
    ]
)