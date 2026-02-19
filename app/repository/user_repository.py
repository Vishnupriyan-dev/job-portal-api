from sqlalchemy.orm import Session
from sqlalchemy import text
from app.exceptions.exception import UserNotFoundError


def active_user(db:Session,user_id):
    query=text(
        """SELECT 
                status
           FROM users
           where user_id= :user_id"""
    )

    return db.execute(
        query,
        {"user_id":user_id}
    ).mappings()


def fetch_skill_id_by_name(db:Session,skill_name:str):
    query=text("SELECT skill_id FROM skills WHERE skill_name=:skill_name")
    return db.execute(
        query,
        {"skill_name":skill_name.strip().lower()}
    ).scalar_one_or_none()


def fetch_user_by_id(db:Session,user_id:int):
    query=text("""SELECT user_id,role,status FROM Users where user_id= :user_id """)
    return db.execute(
        query,
        {"user_id": user_id}
    ).mappings().first()


def create_user(
    db: Session,
    name: str,
    number: str,
    email: str,
    role: str,
    password: str
):
    query = text("""
        INSERT INTO users (user_name, mob_no, email, role, password)
        VALUES (:name, :number, :email, :role, :password)
    """)

    result = db.execute(
        query,
        {
            "name": name,
            "number": number,
            "email": email,
            "role": role,
            "password": password
        }
    )

    return result.lastrowid

 
def update_user(
    db: Session,
    user_id:int,
    name=None,
    number=None,
    email=None,
    password=None
):
    fields = {
        "user_name": name,
        "mob_no": number,
        "email": email,
        "password": password
    }

    field_values = {k: v for k, v in fields.items() if v is not None}

    if not field_values:
        raise ValueError("No fields to update")

    set_clause = ", ".join(f"{col} = :{col}" for col in field_values.keys())

    query = text(f"""
        UPDATE users
        SET {set_clause}
        WHERE user_id = :user_id
    """)

    field_values["user_id"] = user_id

    result = db.execute(query, field_values)

    if result.rowcount == 0:
        return 0
    return result.rowcount

def delete_user(db: Session, user_id: int):
    query = text("""
        UPDATE users
        SET status = 'DELETED'
        WHERE user_id = :user_id
    """)

    result = db.execute(query, {"user_id": user_id})
    return result.rowcount
def applied_jobs(db: Session, user_id: int):
    query = text("""
        SELECT
            j.job_title,
            a.app_status,
            a.app_date,
            c.comp_name
        FROM users u
        INNER JOIN applications a ON u.user_id = a.user_id
        INNER JOIN jobs j ON a.job_id = j.job_id
        INNER JOIN companies c ON j.comp_id = c.comp_id
        WHERE u.user_id = :user_id
    """)
    return db.execute(
        query,
        {"user_id": user_id}
    ).mappings().all()

def fetch_user_with_same_email(db:Session,email:str,user_id:int):
     query=text(""" SELECT * FROM users 
              WHERE email = :email 
              AND user_id != :user_id
              """)
     return db.execute(
         query,
         {"email":email,"user_id":user_id}
     ).mappings().first()
     
     

def fetch_user_by_email(db: Session, email: str):
    query = text("""
        SELECT user_id, email, password, role
        FROM users
        WHERE email = :email
    """)

    return db.execute(
        query,
        {"email": email}
    ).mappings().first()

def add_skills(
    db: Session,
    user_id: int,
    skill_id: int,
    user_mini_exp: int,
    user_maxi_exp: int
):
    query = text("""
        INSERT INTO user_skill (
            user_id, skill_id, user_mini_exp, user_maxi_exp
        )
        VALUES (
            :user_id, :skill_id, :user_mini_exp, :user_maxi_exp
        )
    """)

    result = db.execute(
        query,
        {
            "user_id": user_id,
            "skill_id": skill_id,
            "user_mini_exp": user_mini_exp,
            "user_maxi_exp": user_maxi_exp
        }
    )

    return result.lastrowid
def fetch_user_skill(db: Session, user_id: int):
    query = text("""
        SELECT
            u.user_name,
            s.skills,
            us.user_mini_exp,
            us.user_maxi_exp
        FROM users u
        INNER JOIN user_skill us ON u.user_id = us.user_id
        INNER JOIN skills s ON s.skill_id = us.skill_id
        WHERE u.user_id = :user_id
    """)

    return db.execute(
        query,
        {"user_id": user_id}
    ).mappings().all()
def get_application_count(db: Session, user_id: int):
    query = text("""
        SELECT COUNT(*) AS total_applications
        FROM applications
        WHERE user_id = :user_id
    """)

    return db.execute(
        query,
        {"user_id": user_id}
    ).mappings().first()
def search_jobs(
    db: Session,
    job_title=None,
    comp_title=None,
    location=None,
    industry=None
):
    query = """
        SELECT
            j.job_id,
            j.job_title,
            j.job_type,
            c.comp_name,
            l.location,
            c.industry_type
        FROM jobs j
        INNER JOIN companies c ON j.comp_id = c.comp_id
        INNER JOIN locations l ON c.comp_id = l.comp_id
        WHERE 1 = 1
    """

    params = {}

    if job_title and job_title.strip():
        query += " AND j.job_title LIKE :job_title"
        params["job_title"] = f"%{job_title}%"

    if comp_title and comp_title.strip():
        query += " AND c.comp_name LIKE :comp_title"
        params["comp_title"] = f"%{comp_title}%"

    if location and location.strip():
        query += " AND l.location LIKE :location"
        params["location"] = f"%{location}%"

    if industry and industry.strip():
        query += " AND c.industry_type LIKE :industry"
        params["industry"] = f"%{industry}%"

    return db.execute(
        text(query),
        params
    ).mappings().all()

def update_user_role(
    db: Session,
    user_id: int,
    new_role: str,
    comp_id:int,
    role_granted_by: int
):
    query=text("""
        UPDATE users
        SET role = :role,
            role_granted_by = :admin_id,
            comp_id=:comp_id
        WHERE user_id = :user_id
        """)
    result = db.execute(query,
        {
            "role": new_role,
            "admin_id": role_granted_by,
            "user_id": user_id,
            "comp_id":comp_id
        }
    )

    if result.rowcount == 0:
        raise UserNotFoundError("User not found")
    


def get_recent_applications(db: Session, user_id: int, days: int):
        query = text("""
        SELECT j.job_title, a.app_date, a.app_status
        FROM applications a
        INNER JOIN jobs j ON a.job_id = j.job_id
        WHERE a.user_id = :user_id
          AND a.app_date BETWEEN
              CURDATE() - INTERVAL :days DAY
              AND CURDATE()
    """)
        return db.execute(
              query,
             {"user_id": user_id, "days": days}
      ).mappings().all()


def get_job_application_stats(db: Session, job_id: int, user_id:int):
    query = text("""
        SELECT
            j.status,
            j.job_title,
            COUNT(DISTINCT a.user_id=:user_id) AS applicant_count
        FROM jobs j
        LEFT JOIN applications a ON j.job_id = a.job_id
        WHERE j.job_id = :job_id
        GROUP BY j.job_id, j.job_title, j.status
    """)
    return db.execute(query, {"job_id": job_id,"user_id":user_id}).mappings().first()



def fetch_all_skills(db:Session):
    query=text(
        """ select *
            from skills"""
    )
    return db.execute(
        query
    ).mappings().all()