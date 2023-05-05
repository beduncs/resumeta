CREATE TABLE IF NOT EXISTS jobs (
    job_id integer PRIMARY KEY,
    title text NOT NULL,
    begin_date text NOT NULL,
    end_date text NOT NULL,
    job_workplace integer,
    FOREIGN KEY (job_workplace) REFERENCES workplace(workplace_id)
);

CREATE TABLE IF NOT EXISTS activities (
    activity_id integer PRIMARY KEY,
    detail text NOT NULL
);

CREATE TABLE IF NOT EXISTS workplaces (
    workplace_id integer PRIMARY KEY,
    company_name text NOT NULL
);

CREATE TABLE IF NOT EXISTS job_activities (
   job_activity_id integer PRIMARY KEY,
   job_link_id integer NOT NULL,
   activity_link_id integer NOT NULL,
   FOREIGN KEY (job_link_id) REFERENCES job(job_id),
   FOREIGN KEY (activity_link_id) REFERENCES activity(activity_id)
);