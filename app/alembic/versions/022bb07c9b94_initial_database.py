"""initial database

Revision ID: 022bb07c9b94
Revises: 
Create Date: 2020-03-23 14:53:53.101322

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "022bb07c9b94"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():

    op.execute(
        f"""CREATE TYPE "extension_modes" AS ENUM (
            'DESIGNER',
            'EXECUTOR'
        )"""
    )

    op.execute(
        f"""CREATE TYPE "table_views" AS ENUM (
        'JOB_ROLE_MATRIX',
        'SCREEN_JOB_MATRIX'
        )"""
    )

    op.execute(
        f"""CREATE TYPE "course_item_types" AS ENUM (
        'SECTION',
        'LESSON',
        'QUIZ'
        )"""
    )

    op.execute(
        f"""CREATE TYPE "question_types" AS ENUM (
        'TRUE_OR_FALSE',
        'MULTI_CHOICE',
        'SINGLE_CHOICE',
        'FILL_THE_BLANK'
        )"""
    )

    op.execute(
        f"""CREATE TYPE "user_item_types" AS ENUM (
        'COURSE',
        'LESSON',
        'QUIZ',
        'QUESTION'
        )"""
    )

    op.execute(
        f"""CREATE TYPE "user_item_status" AS ENUM (
        'ENROLLED',
        'INPROGRESS',
        'COMPLETED'
        )"""
    )

    op.execute(
        f"""CREATE TYPE "audit_trail_types" AS ENUM (
        'JOB',
        'USER',
        'ROLE',
        'APPLICATION_URL',
        'PLAYBOOK',
        'COURSE',
        'LESSON',
        'QUIZ',
        'QUESTION'
        )"""
    )

    op.execute(
        f"""CREATE TYPE "audit_trail_actions" AS ENUM (
        'CREATE',
        'UPDATE',
        'DELETE'
        )"""
    )

    op.execute(
        f"""CREATE TABLE "ext_sessions" (
        "id" SERIAL PRIMARY KEY,
        "user_id" int,
        "job_id" int,
        "ext_mode" extension_modes,
        "active_tab_id" varchar,
        "active_step" int DEFAULT 0,
        "created_on" timestamp default current_timestamp,
        "updated_on" timestamp
        )"""
    )

    op.execute(
        f"""CREATE TABLE "users" (
        "id" SERIAL PRIMARY KEY,
        "email" varchar,
        "first_name" varchar,
        "last_name" varchar,
        "address" text,
        "hashed_password" varchar,
        "role_id" int,
        "is_designer" bool DEFAULT false,
        "is_active" bool DEFAULT true,
        "is_superuser" bool DEFAULT false
        )"""
    )

    op.execute(
        f"""CREATE TABLE "roles" (
        "id" SERIAL PRIMARY KEY,
        "name" varchar
        )"""
    )

    op.execute(
        f"""CREATE TABLE "application_urls" (
        "id" SERIAL PRIMARY KEY,
        "name" varchar
        )"""
    )

    op.execute(
        f"""CREATE TABLE "jobs" (
        "id" SERIAL PRIMARY KEY,
        "name" varchar,
        "description" text,
        "application_url_id" int,
        "steps" json,
        "is_locked" bool
        )"""
    )

    op.execute(
        f"""CREATE TABLE "job_role_mappings" (
        "id" SERIAL PRIMARY KEY,
        "job_id" int,
        "role_id" int
        )"""
    )

    op.execute(
        f"""CREATE TABLE "playbooks" (
        "id" SERIAL PRIMARY KEY,
        "name" varchar,
        "description" text,
        "page_content" text
        )"""
    )

    op.execute(
        f"""CREATE TABLE "playbook_role_mappings" (
        "id" SERIAL PRIMARY KEY,
        "playbook_id" int,
        "role_id" int
        )"""
    )

    op.execute(
        f"""CREATE TABLE "user_table_views" (
        "id" SERIAL PRIMARY KEY,
        "user_id" int,
        "table" table_views,
        "config" text
        )"""
    )

    op.execute(
        f"""CREATE TABLE "courses" (
        "id" SERIAL PRIMARY KEY,
        "name" varchar,
        "description" varchar,
        "duration" int,
        "enroll_required" bool,
        "passing_percentage" int
        )"""
    )

    op.execute(
        f"""CREATE TABLE "lessons" (
        "id" SERIAL PRIMARY KEY,
        "name" varchar,
        "description" text,
        "duration" int,
        "page_content" text
        )"""
    )

    op.execute(
        f"""CREATE TABLE "course_items" (
        "id" SERIAL PRIMARY KEY,
        "course_id" int,
        "item_title" varchar,
        "item_type" course_item_types,
        "item_id" int,
        "item_order" int
        )"""
    )

    op.execute(
        f"""CREATE TABLE "quizzes" (
        "id" SERIAL PRIMARY KEY,
        "name" varchar,
        "description" text,
        "duration" int,
        "passing_percentage" int,
        "show_correct_review" bool
        )"""
    )

    op.execute(
        f"""CREATE TABLE "questions" (
        "id" SERIAL PRIMARY KEY,
        "name" varchar,
        "page_content" text,
        "type" question_types
        )"""
    )

    op.execute(
        f"""CREATE TABLE "quiz_questions_mapping" (
        "id" SERIAL PRIMARY KEY,
        "quiz_id" int,
        "question_id" int,
        "order" int
        )"""
    )

    op.execute(
        f"""CREATE TABLE "question_answers" (
        "id" SERIAL PRIMARY KEY,
        "question_id" int,
        "title" varchar,
        "value" varchar,
        "is_true" bool
        )"""
    )

    op.execute(
        f"""CREATE TABLE "user_items" (
        "id" SERIAL PRIMARY KEY,
        "user_id" int,
        "item_type" user_item_types,
        "item_id" int,
        "start_time" timestamp,
        "end_time" timestamp,
        "status" user_item_status,
        "due_date" date
        )"""
    )

    op.execute(
        f"""CREATE TABLE "user_question_answers" (
        "id" SERIAL PRIMARY KEY,
        "user_item_id" int,
        "answer" varchar
        )"""
    )

    op.execute(
        f"""CREATE TABLE "audit_trails" (
        "id" SERIAL PRIMARY KEY,
        "type" audit_trail_types,
        "action" audit_trail_actions,
        "item_id" int,
        "item_value" text,
        "user_id" int,
        "entry_datetime" timestamp default current_timestamp
        )"""
    )

    op.execute(f"""COMMENT ON COLUMN "roles"."name" IS 'DESIGNER, '""")

    op.execute(f"""COMMENT ON COLUMN "courses"."duration" IS 'in days'""")

    op.execute(
        f"""COMMENT ON COLUMN "courses"."passing_percentage" IS 'in %'"""
    )

    op.execute(f"""COMMENT ON COLUMN "lessons"."duration" IS 'in days'""")

    op.execute(
        f"""COMMENT ON COLUMN "course_items"."item_id" IS 'id of item_type, null for SECTION'"""
    )

    op.execute(f"""COMMENT ON COLUMN "quizzes"."duration" IS 'in min'""")

    op.execute(
        f"""COMMENT ON COLUMN "quizzes"."passing_percentage" IS 'in %'"""
    )

    op.execute(
        f"""COMMENT ON COLUMN "user_items"."item_id" IS 'id of item_type'"""
    )

    op.execute(
        f"""COMMENT ON COLUMN "audit_trails"."item_id" IS 'id of type'"""
    )

    op.execute(
        f"""ALTER TABLE "ext_sessions" ADD FOREIGN KEY ("user_id") REFERENCES "users" ("id")"""
    )

    op.execute(
        f"""ALTER TABLE "ext_sessions" ADD FOREIGN KEY ("job_id") REFERENCES "jobs" ("id")"""
    )

    op.execute(
        f"""ALTER TABLE "users" ADD FOREIGN KEY ("role_id") REFERENCES "roles" ("id")"""
    )

    op.execute(
        f"""ALTER TABLE "jobs" ADD FOREIGN KEY ("application_url_id") REFERENCES "application_urls" ("id")"""
    )

    op.execute(
        f"""ALTER TABLE "job_role_mappings" ADD FOREIGN KEY ("job_id") REFERENCES "jobs" ("id")"""
    )

    op.execute(
        f"""ALTER TABLE "job_role_mappings" ADD FOREIGN KEY ("role_id") REFERENCES "roles" ("id")"""
    )

    op.execute(
        f"""ALTER TABLE "playbook_role_mappings" ADD FOREIGN KEY ("playbook_id") REFERENCES "playbooks" ("id")"""
    )

    op.execute(
        f"""ALTER TABLE "playbook_role_mappings" ADD FOREIGN KEY ("role_id") REFERENCES "roles" ("id")"""
    )

    op.execute(
        f"""ALTER TABLE "user_table_views" ADD FOREIGN KEY ("user_id") REFERENCES "users" ("id")"""
    )

    op.execute(
        f"""ALTER TABLE "course_items" ADD FOREIGN KEY ("course_id") REFERENCES "courses" ("id")"""
    )

    op.execute(
        f"""ALTER TABLE "quiz_questions_mapping" ADD FOREIGN KEY ("quiz_id") REFERENCES "quizzes" ("id")"""
    )

    op.execute(
        f"""ALTER TABLE "quiz_questions_mapping" ADD FOREIGN KEY ("question_id") REFERENCES "questions" ("id")"""
    )

    op.execute(
        f"""ALTER TABLE "question_answers" ADD FOREIGN KEY ("question_id") REFERENCES "questions" ("id")"""
    )

    op.execute(
        f"""ALTER TABLE "user_items" ADD FOREIGN KEY ("user_id") REFERENCES "users" ("id")"""
    )

    op.execute(
        f"""ALTER TABLE "user_question_answers" ADD FOREIGN KEY ("user_item_id") REFERENCES "user_items" ("id")"""
    )

    op.execute(
        f"""ALTER TABLE "audit_trails" ADD FOREIGN KEY ("user_id") REFERENCES "users" ("id")"""
    )


def downgrade():
    pass
