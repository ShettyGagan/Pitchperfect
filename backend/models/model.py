# from pydantic import BaseModel

# class FacialExpressionResponse(BaseModel):
#     emotion_timeline: list[dict]
#     engagement_metrics: dict

# class VoiceAnalysisResponse(BaseModel):
#     transcription: str
#     speech_rate_wpm: str
#     pitch_variation: str
#     volume_consistency: str

# class ContentAnalysisResponse(BaseModel):
#     grammar_corrections: list[str]
#     filler_words: dict
#     suggestions: list[str]

# class FeedbackResponse(BaseModel):
#     scores: dict
#     total_score: int
#     interpretation: str
#     feedback_summary: str

# class CoordinatorResponse(BaseModel):
#     facial_expression_response: FacialExpressionResponse
#     voice_analysis_response: VoiceAnalysisResponse
#     content_analysis_response: ContentAnalysisResponse
#     feedback_response: FeedbackResponse
#     strengths: list[str]
#     weaknesses: list[str]
#     suggestions: list[str]


from pydantic import BaseModel, Field


class FacialExpressionResponse(BaseModel):
    emotion_timeline: list[dict] = Field(description="list of emotion entries with timestamp and detected emotion")
    engagement_metrics: dict = Field(description="eye_contact_frequency and smile_frequency counts")


class VoiceAnalysisResponse(BaseModel):
    transcription: str = Field(description="full transcribed text from the audio")
    speech_rate_wpm: str = Field(description="words per minute as a string")
    pitch_variation: str = Field(description="pitch variation level: low, medium, or high")
    volume_consistency: str = Field(description="volume consistency level: consistent, moderate, or inconsistent")


class ContentAnalysisResponse(BaseModel):
    grammar_corrections: list[str] = Field(description="list of grammar correction suggestions")
    filler_words: dict = Field(description="dict mapping filler word to its occurrence count")
    suggestions: list[str] = Field(description="list of content improvement suggestions")


class FeedbackResponse(BaseModel):
    scores: dict = Field(description="scores dict with keys: content_organization, delivery_vocal_quality, body_language_eye_contact, audience_engagement, language_clarity each 1-5")
    total_score: int = Field(description="sum of all five scores, between 5 and 25")
    interpretation: str = Field(description="one of: Needs significant improvement, Developing skills, Competent speaker, Proficient speaker, Outstanding speaker")
    feedback_summary: str = Field(description="concise feedback addressing the speaker directly on strengths and areas for improvement")


class CoordinatorResponse(BaseModel):
    facial_expression_response: FacialExpressionResponse
    voice_analysis_response: VoiceAnalysisResponse
    content_analysis_response: ContentAnalysisResponse
    feedback_response: FeedbackResponse
    strengths: list[str] = Field(description="list of the speaker's key strengths")
    weaknesses: list[str] = Field(description="list of the speaker's key weaknesses")
    suggestions: list[str] = Field(description="list of actionable improvement suggestions for the speaker")