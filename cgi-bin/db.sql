CREATE TABLE tblSignups (
        id              serial not null primary key,
        name            text,
        email           text,
        phone           text,
        class           text,
        created         timestamptz,
        do_not_email    boolean not null default false
);

CREATE TABLE tblPhases (
        id          serial not null primary key,
        phase       text not null
);
INSERT INTO tblPhases(phase) VALUES ('leadership');

CREATE TABLE xrefSignupsPhases (
        signup_id   integer references tblSignups(id),
        phase_id    integer references tblPhases(id),
        created     timestamptz not null,
        primary key (signup_id, phase_id)
);
