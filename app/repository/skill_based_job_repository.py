from sqlalchemy.orm import Session
from sqlalchemy import text

def get_recommended_jobs(db: Session, user_id: int):
     query=text("""
        WITH user_profile AS (
            SELECT u.user_id, u.user_name,
                   us.user_mini_exp,
                   us.user_maxi_exp, us.skill_id
            FROM users u
            INNER JOIN user_skill us ON u.user_id = us.user_id
            WHERE u.user_id = :user_id
        ),
        job_profile AS (
            SELECT j.job_id, j.job_title,
                   js.mini_req_exp, js.max_req_exp,
                   js.skill_id,
                   c.comp_name AS company_name,
                   l.location
            FROM jobs j
            INNER JOIN companies c ON j.comp_id = c.comp_id
            INNER JOIN locations l ON l.comp_id = c.comp_id
            INNER JOIN job_skills js ON j.job_id = js.job_id
        ),
        matched_skills AS (
            SELECT up.user_id, up.user_name,
                   MIN(up.user_mini_exp) AS mini_exp,
                   MAX(up.user_maxi_exp) AS max_exp,
                   jp.company_name, jp.location,
                   jp.job_title, jp.job_id,
                   COUNT(DISTINCT jp.skill_id) AS skill_count,
                   MIN(jp.mini_req_exp) AS mini_expj,
                   MAX(jp.max_req_exp) AS maxi_expj
            FROM user_profile up
            INNER JOIN job_profile jp ON up.skill_id = jp.skill_id
            GROUP BY up.user_id, up.user_name,
                     jp.job_id, jp.job_title,
                     jp.location, jp.company_name
        ),
        total_skills AS (
            SELECT job_id,
                   COUNT(DISTINCT skill_id) AS all_skills_per_job
            FROM job_skills
            GROUP BY job_id
        )
        SELECT
            ms.job_title,
            CASE
                WHEN (ms.skill_count * 100 / ts.all_skills_per_job) >= 25 THEN 30
                ELSE 0
            END +
            CASE
                WHEN (ms.mini_exp <= ms.maxi_expj AND ms.max_exp >= ms.mini_expj) THEN 20
                ELSE 0
            END AS total_score
        FROM matched_skills ms
        INNER JOIN total_skills ts ON ms.job_id = ts.job_id
        WHERE (ms.skill_count * 100 / ts.all_skills_per_job) >= 10
          AND (ms.max_exp >= ms.mini_expj AND ms.mini_expj <= ms.maxi_expj)
        ORDER BY total_score DESC
    """)

     return db.execute(
        query,
        {"user_id": user_id}
     ).mappings().all()
