from sqlalchemy.orm import Session
from sqlalchemy.orm.attributes import flag_modified
from app.db.use_cases.models import UseCase
from app.db.playbooks.models import Playbook
from app.db.jobs.models import Job


def delete_role_mapping(db: Session, role_id: int):
    # Remove role reference from other models
    affected_models = [Job, UseCase, Playbook]

    for model in affected_models:
        items = db.query(model).filter(model.role_ids.any(role_id)).all()
        for item in items:
            item.role_ids.remove(role_id)
            flag_modified(item, "role_ids")
            db.merge(item)
            db.flush()
            db.commit()
