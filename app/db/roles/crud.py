from sqlalchemy.orm import Session
from app.db.jobs.crud import get_job_roles
from app.db.use_cases.crud import get_use_case_mappings
from app.db.playbooks.crud import get_playbook_by_role


def delete_role_mapping(db: Session, role_id: int):
    type = "roles"
    job_roles = get_job_roles(db, type, role_id)
    if job_roles:
        for value in job_roles:
            db.delete(value)
            db.commit()
    use_case_resp = get_use_case_mappings(db, type, role_id)
    if use_case_resp:
        for value in use_case_resp:
            db.delete(value)
            db.commit()
    playbook_resp = get_playbook_by_role(db, role_id)
    if playbook_resp:
        for value in playbook_resp:
            db.delete(value)
            db.commit()
    return True
