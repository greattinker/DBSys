--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;
COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;
SET default_tablespace = '';
SET default_with_oids = false;

CREATE TABLE following (
    "user" integer NOT NULL,
    follows integer NOT NULL
);

CREATE TABLE tweets (
    body text NOT NULL,
    created timestamp without time zone DEFAULT now() NOT NULL,
    "user" integer NOT NULL,
    id integer NOT NULL
);
CREATE SEQUENCE tweets_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE tweets_id_seq OWNED BY tweets.id;

CREATE TABLE users (
    id integer NOT NULL,
    username character varying(64),
    password character varying(64)
);

CREATE SEQUENCE users_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE users_id_seq OWNED BY users.id;

ALTER TABLE ONLY tweets ALTER COLUMN id SET DEFAULT nextval('tweets_id_seq'::regclass);

ALTER TABLE ONLY users ALTER COLUMN id SET DEFAULT nextval('users_id_seq'::regclass);

ALTER TABLE ONLY following
    ADD CONSTRAINT following_pk PRIMARY KEY ("user", follows);

ALTER TABLE ONLY tweets
    ADD CONSTRAINT tweets_pkey PRIMARY KEY (id);

ALTER TABLE ONLY users
    ADD CONSTRAINT username_unique UNIQUE (username);

ALTER TABLE ONLY users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);

CREATE INDEX following_follows_idx ON following USING btree (follows);

CREATE INDEX tweet_by_user_idx ON tweets USING btree ("user");

CREATE INDEX tweets_created_idx ON tweets USING btree (created DESC);

ALTER TABLE ONLY following
    ADD CONSTRAINT following_follows_fkey FOREIGN KEY (follows) REFERENCES users(id) ON DELETE CASCADE;

ALTER TABLE ONLY following
    ADD CONSTRAINT following_user_fkey FOREIGN KEY ("user") REFERENCES users(id) ON DELETE CASCADE;

ALTER TABLE ONLY tweets
    ADD CONSTRAINT tweet_to_user_fk FOREIGN KEY ("user") REFERENCES users(id);
