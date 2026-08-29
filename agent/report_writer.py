import json

from pydantic import BaseModel, Field

from llm import get_chat_model

class Finding(BaseModel):
    title: str
    detail: str

class Recommendation(BaseModel):
    priority: str
    action: str
    rationale: str

class Evidence(BaseModel):
    source: str
    summary: str

class AnalystReport(BaseModel):
    title: str
    subtitle: str
    executive_summary: str
    methodology: str
    findings: list[Finding]
    recommendations: list[Recommendation]
    limitations: str
    evidence: list[Evidence] = Field(default_factory=list)


def _json_object_from_content(content: object) -> str:
    """Return a JSON object from a model response, including fenced JSON."""
    if not isinstance(content, str):
        raise ValueError("The model returned non-text content for the report")

    text = content.strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[1] if "\n" in text else ""
        text = text.rsplit("```", 1)[0].strip()

    start, end = text.find("{"), text.rfind("}")
    if start == -1 or end == -1 or end <= start:
        raise ValueError("The model response did not contain a JSON object")

    candidate = text[start : end + 1]
    json.loads(candidate)  # Validate the JSON before Pydantic validates the schema.
    return candidate


def _report_prompt(analysis_text: str, evidence_text: str, data_profile: dict) -> str:
    schema = json.dumps(AnalystReport.model_json_schema(), indent=2)
    return f"""
You are the report-writing component of a professional analyst team.
Create a defensible report from the analysis notes below.
Use only numbers present in the notes/profile; do not invent metrics.
Clearly distinguish observation from interpretation. Include limitations.

Return ONLY a valid JSON object that conforms exactly to this schema. Do not use
Markdown, code fences, or prose before or after the JSON.
Keep the report concise: provide at most 3 findings and 3 recommendations;
keep each text field under 100 words.

JSON SCHEMA:
{schema}

DATA PROFILE:
{data_profile}

ANALYSIS NOTES:
{analysis_text}

RETRIEVED GUIDANCE / EVIDENCE:
{evidence_text}
"""


def write_report(analysis_text: str, evidence_text: str, data_profile: dict) -> AnalystReport:
    # Do not pass response_format to ChatOpenAI here. In some OpenRouter-compatible
    # responses, the OpenAI client attempts provider-side parsing and raises before
    # we can validate or repair an incomplete response ourselves.
    model = get_chat_model()
    prompt = _report_prompt(analysis_text, evidence_text, data_profile)

    for attempt in range(2):
        response = model.invoke(prompt)
        try:
            return AnalystReport.model_validate_json(_json_object_from_content(response.content))
        except (ValueError, json.JSONDecodeError) as exc:
            if attempt:
                raise RuntimeError(
                    "The LLM returned an invalid report format after a retry. "
                    "Try a model that supports JSON output."
                ) from exc
            prompt = f"""Your previous response was not valid JSON.
Return ONLY one JSON object matching the schema below, with no Markdown or explanation.
Provide at most 3 findings and 3 recommendations; keep each text field under 100 words.

JSON SCHEMA:
{json.dumps(AnalystReport.model_json_schema(), indent=2)}

PREVIOUS RESPONSE:
{response.content}
"""

    raise AssertionError("The report-generation retry loop should always return or raise")
