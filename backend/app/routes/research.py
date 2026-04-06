from fastapi import APIRouter

from app.models.schemas import ResearchRequest, ResearchResponse, TokenBudgetDebug
from app.services.answerer import AnswererService
from app.services.planner import PlannerService
from app.services.retriever import RetrieverService
from app.services.summarizer import SummarizerService
from app.services.token_budget import TokenBudgetManager

router = APIRouter()

planner_service = PlannerService()
retriever_service = RetrieverService()
summarizer_service = SummarizerService()
answerer_service = AnswererService()
token_budget_manager = TokenBudgetManager()


@router.post("/research")
async def run_research(payload: ResearchRequest) -> ResearchResponse:
    sub_questions = planner_service.plan(payload.query)
    retrieved_chunks = retriever_service.retrieve(sub_questions)
    summary = summarizer_service.summarize(retrieved_chunks)
    final_answer = answerer_service.answer(payload.query, summary)
    debug = token_budget_manager.get_debug_snapshot()

    return ResearchResponse(
        query=payload.query,
        session_id=payload.session_id,
        sub_questions=sub_questions,
        retrieved_chunks=retrieved_chunks,
        final_answer=final_answer,
        debug=TokenBudgetDebug(**debug),
    )
