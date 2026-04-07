from fastapi import APIRouter

from app.models.schemas import ResearchRequest, ResearchResponse, TokenBudgetDebug
from app.services.answerer import AnswererService
from app.services.memory_manager import MemoryManager
from app.services.planner import PlannerService
from app.services.retriever import RetrieverService
from app.services.summarizer import SummarizerService
from app.services.token_budget import TokenBudgetManager

router = APIRouter()

planner_service = PlannerService()
retriever_service = RetrieverService()
summarizer_service = SummarizerService()
answerer_service = AnswererService()
memory_manager = MemoryManager()
token_budget_manager = TokenBudgetManager()


@router.post("/research")
async def run_research(payload: ResearchRequest) -> ResearchResponse:
    sub_questions = planner_service.plan(payload.query)
    retrieved_chunks = retriever_service.retrieve(payload.query, sub_questions)
    budgeted_chunks, debug = memory_manager.enforce_budget(
        retrieved_chunks,
        token_budget_manager=token_budget_manager,
        summarizer=summarizer_service,
    )
    summary = summarizer_service.summarize(budgeted_chunks)
    final_answer = answerer_service.answer(
        payload.query,
        summary,
        budgeted_chunks,
        constrained=debug["compressed"] or debug["dropped_chunks"] > 0,
    )

    return ResearchResponse(
        query=payload.query,
        session_id=payload.session_id,
        sub_questions=sub_questions,
        retrieved_chunks=budgeted_chunks,
        final_answer=final_answer,
        debug=TokenBudgetDebug(**debug),
    )
