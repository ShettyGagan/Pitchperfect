# from fastapi import FastAPI
# from agno.team import Team
# from agno.models.groq import Groq
# from backend.agents.facial_expression import facial_expression_agent
# from backend.agents.voice_analyser_agent import voice_analyser_agent
# from backend.agents.content_analysis import content_analysis_agent
# from backend.agents.feedback_agent import feedback_agent

# from backend.models.model import CoordinatorResponse


# #team of agents
# final_agent=Team(
#     name="coordinator_agent",
#     model=Groq(id="llama-3.3-70b-versatile"),
#     mode="coordinate",
#     members=[facial_expression_agent,voice_analyser_agent,content_analysis_agent,feedback_agent],
#     description="You are a public speaking coach who helps individuals improve their presentation skills through feedback and analysis.",
#     instructions=[
#         # ── Orchestration ────────────────────────────────────────────────────
#         "You will be given a video file path of a person speaking.",
 
#         "Step 1 — Ask the facial_expression_agent to analyse the video for "
#         "emotions and engagement.  Its response will be in TOON format.",
 
#         "Step 2 — Ask the voice_analysis_agent to analyse the same video for "
#         "speech rate, pitch variation, volume consistency, and to produce a "
#         "full transcription.  Its response will be in TOON format.",
 
#         "Step 3 — Pass the TOON transcription from the voice_analysis_agent "
#         "verbatim to the content_analysis_agent for grammar, filler-word, and "
#         "content analysis.  Its response will be in TOON format.",
 
#         "Step 4 — Pass all three TOON responses to the feedback_agent so it "
#         "can score the speaker and produce a feedback summary.  Its response "
#         "will be in TOON format.",
 
#         # ── Synthesis ────────────────────────────────────────────────────────
#         "After collecting all four TOON responses, decode each one and "
#         "synthesise the results.",
 
#         "Produce the following lists, addressing the speaker directly:",
#         "  • strengths   — what the speaker is already doing well.",
#         "  • weaknesses  — specific areas that need improvement.",
#         "  • suggestions — concrete, actionable steps to improve.",
 
#         # ── Output contract ──────────────────────────────────────────────────
#         "Your final output MUST be valid JSON conforming to the CoordinatorResponse schema.",
#         "Populate every field; no field may be null or an empty list.",
#         "Do NOT include any text outside the JSON object.",
 
#         # ── Data fidelity ────────────────────────────────────────────────────
#         "The nested *_response fields must faithfully reflect the decoded "
#         "data from each sub-agent — do not invent or omit values.",
#     ],
#     add_datetime_to_instructions=True,
#     add_member_tools_to_system_message=False,  # This can be tried to make the agent more consistently get the transfer tool call correct
#     enable_agentic_context=True,  # Allow the agent to maintain a shared context and send that to members.
#     share_member_interactions=True,  # Share all member responses with subsequent member requests.
#     show_members_responses=True,
#     response_model=CoordinatorResponse,
#     use_json_mode=True,
#     markdown=False,
#     show_tool_calls=True,
#     debug_mode=True

# )



from agno.team import Team
from agno.agent import Agent
from agno.models.groq import Groq

from backend.agents.facial_expression import facial_expression_agent
from backend.agents.voice_analyser_agent import voice_analyser_agent
from backend.agents.content_analysis import content_analysis_agent
from backend.agents.feedback_agent import feedback_agent
from backend.models.model import CoordinatorResponse
from backend.toon_util import structure_template_pydantic

_output_template = structure_template_pydantic(CoordinatorResponse)

# ── Step 1: Coordinator — tools ON, json mode OFF ────────────────────────────
final_agent = Team(
    name="coordinator_agent",
    model=Groq(id="llama-3.3-70b-versatile"),
    mode="coordinate",
    members=[facial_expression_agent, voice_analyser_agent, content_analysis_agent, feedback_agent],
    description="You are a public speaking coach who helps individuals improve their presentation skills through feedback and analysis.",
    instructions=[
        "You will be given a video file path of a person speaking.",

        "Step 1 — Ask the facial_expression_agent to analyse the video for "
        "emotions and engagement.  Its response will be in TOON format.",

        "Step 2 — Ask the voice_analysis_agent to analyse the same video for "
        "speech rate, pitch variation, volume consistency, and to produce a "
        "full transcription.  Its response will be in TOON format.",

        "Step 3 — Pass the TOON transcription from the voice_analysis_agent "
        "verbatim to the content_analysis_agent for grammar, filler-word, and "
        "content analysis.  Its response will be in TOON format.",

        "Step 4 — Pass all three TOON responses to the feedback_agent so it "
        "can score the speaker and produce a feedback summary.  Its response "
        "will be in TOON format.",

        "After collecting all four TOON responses, synthesise the results.",

        "Produce the following lists, addressing the speaker directly:",
        "  • strengths   — what the speaker is already doing well.",
        "  • weaknesses  — specific areas that need improvement.",
        "  • suggestions — concrete, actionable steps to improve.",

        "Output ALL four agent TOON responses plus your strengths, weaknesses, "
        "and suggestions in TOON format.",
        "Do NOT output JSON. Output TOON only. No markdown, no code fences.",
    ],
    add_datetime_to_instructions=True,
    add_member_tools_to_system_message=False,
    enable_agentic_context=True,
    share_member_interactions=True,
    show_members_responses=True,
    markdown=False,
    show_tool_calls=True,
    debug_mode=True,
)

# ── Step 2: Parser — tools OFF, json mode ON ─────────────────────────────────
parser_agent = Agent(
    name="parser_agent",
    model=Groq(id="llama-3.1-8b-instant"),
    description="You convert a TOON-formatted analysis summary into strict JSON.",
    instructions=[
        "You will receive a TOON-formatted public speaking analysis.",
        "Your only job is to parse it and return a valid JSON object.",
        "The JSON MUST conform exactly to this structure:",
        _output_template,
        "Rules:",
        "  • Output ONLY the JSON object, nothing else.",
        "  • No markdown, no code fences, no explanation.",
        "  • All fields must be populated — no nulls, no empty lists.",
    ],
    response_model=CoordinatorResponse,
    use_json_mode=True,
    markdown=False,
    show_tool_calls=False,
    debug_mode=True,
)