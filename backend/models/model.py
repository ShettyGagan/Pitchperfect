from pydantic import BaseModel

class FacialExpressionResponse(BaseModel):
    emotion_timeline: list[dict]
    engagement_metrics: dict

class VoiceAnalysisResponse(BaseModel):
    transcription: str
    speech_rate_wpm: str
    pitch_variation: str
    volume_consistency: str

class ContentAnalysisResponse(BaseModel):
    grammar_corrections: list[str]
    filler_words: dict
    suggestions: list[str]

class FeedbackResponse(BaseModel):
    scores: dict
    total_score: int
    interpretation: str
    feedback_summary: str

class CoordinatorResponse(BaseModel):
    facial_expression_response: FacialExpressionResponse
    voice_analysis_response: VoiceAnalysisResponse
    content_analysis_response: ContentAnalysisResponse
    feedback_response: FeedbackResponse
    strengths: list[str]
    weaknesses: list[str]
    suggestions: list[str]
