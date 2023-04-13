from sqlalchemy.orm import Session
from sqlalchemy.orm.attributes import flag_modified
from app.db.use_cases.models import UseCase
from app.db.playbooks.models import Playbook
from app.db.jobs.models import Job
from app.db.roles.models import Role


__all__ = ("delete_all_role_mappings", "update_role_mappings")


def delete_all_role_mappings(db: Session, role_id: int, model=None):
    # Remove role reference from other models
    affected_models = [Job, UseCase, Playbook] if not model else [model]

    for model in affected_models:
        items = db.query(model).filter(model.role_ids.any(role_id)).all()
        for item in items:
            item.role_ids.remove(role_id)
            flag_modified(item, "role_ids")
            db.merge(item)
            db.flush()
            db.commit()


def update_role_mappings(db: Session, role_id, role: Role):
    if role.job_ids:
        delete_all_role_mappings(db, role_id, Job)
        jobs = db.query(Job).filter(Job.id.in_(role.job_ids)).all()
        for job in jobs:
            job.role_ids.append(role_id)
            flag_modified(job, "role_ids")
            db.merge(job)
            db.flush()
            db.commit()

    if role.use_case_ids:
        delete_all_role_mappings(db, role_id, UseCase)
        use_cases = (
            db.query(UseCase).filter(UseCase.id.in_(role.use_case_ids)).all()
        )
        for use_case in use_cases:
            use_case.role_ids.append(role_id)
            flag_modified(use_case, "role_ids")
            db.merge(use_case)
            db.flush()
            db.commit()

    if role.playbook_ids:
        delete_all_role_mappings(db, role_id, Playbook)
        playbooks = (
            db.query(Playbook).filter(Playbook.id.in_(role.playbook_ids)).all()
        )
        for playbook in playbooks:
            playbook.role_ids.append(role_id)
            flag_modified(playbook, "role_ids")
            db.merge(playbook)
            db.flush()
            db.commit()
