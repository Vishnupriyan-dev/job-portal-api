from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.controllers.user_controller import router as router_users
from app.controllers.company_controller import router as router_companies
from app.controllers.job_controller import router as router_jobs
from app.controllers.application_controller import router as router_applications
from app.controllers.skill_based_job_filter_controller import router as router_matching_jobs

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(router_users)
app.include_router(router_jobs)
app.include_router(router_companies)
app.include_router(router_applications)
app.include_router(router_matching_jobs)