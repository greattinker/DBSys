--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

--
-- Name: tweet_ids(character varying); Type: FUNCTION; Schema: public; Owner: hduser
--

CREATE FUNCTION tweet_ids(character varying, OUT id integer) RETURNS SETOF integer
    LANGUAGE sql ROWS 40
    AS $_$

select t.id		      
from 
	users as u
	join following as f on u.id=f."user"
	join users as followers on f.follows=followers.id
	join tweets as t on t."user"=followers.id
where 
	u.username = $1
order by 
	t.created desc 
    $_$;


ALTER FUNCTION public.tweet_ids(character varying, OUT id integer) OWNER TO hduser;

--
-- Name: tweet_ids(character varying, integer, integer); Type: FUNCTION; Schema: public; Owner: hduser
--

CREATE FUNCTION tweet_ids(character varying, lim integer, off integer, OUT id integer) RETURNS SETOF integer
    LANGUAGE sql ROWS 40
    AS $_$

select t.id		      
from 
	users as u
	join following as f on u.id=f."user"
	join users as followers on f.follows=followers.id
	join tweets as t on t."user"=followers.id
where 
	u.username = $1
order by 
	t.created desc 
limit $2 offset $3
    $_$;


ALTER FUNCTION public.tweet_ids(character varying, lim integer, off integer, OUT id integer) OWNER TO hduser;

--
-- Name: tweets(character varying, integer, integer); Type: FUNCTION; Schema: public; Owner: hduser
--

CREATE FUNCTION tweets(character varying, lim integer, off integer, OUT created_at timestamp without time zone, OUT username character varying, OUT body text) RETURNS SETOF record
    LANGUAGE sql ROWS 40
    AS $_$

select t.created, followers.username, t.body
		      
from 
	users as u
	join following as f on u.id=f."user"
	join users as followers on f.follows=followers.id
	join tweets as t on t."user"=followers.id
where 
	u.username = $1
order by 
	t.created desc 
limit $2 offset $3
    $_$;


ALTER FUNCTION public.tweets(character varying, lim integer, off integer, OUT created_at timestamp without time zone, OUT username character varying, OUT body text) OWNER TO hduser;

--
-- Name: tweets_dn(character varying, integer, integer); Type: FUNCTION; Schema: public; Owner: hduser
--

CREATE FUNCTION tweets_dn(character varying, lim integer, off integer, OUT created_at timestamp without time zone, OUT username character varying, OUT body text) RETURNS SETOF record
    LANGUAGE sql ROWS 40
    AS $_$select t.created, followers.username, t.body
                    from tweets as t,
                    users as followers,
                    (select
                        stream[array_upper(stream, 1)-($2+$3-1):array_upper(stream, 1)-$3] as stream_tail
                        from users where username=$1) as s
                    where t.id = any(stream_tail)
                    and followers.id=t."user"
                    order by t.created desc$_$;


ALTER FUNCTION public.tweets_dn(character varying, lim integer, off integer, OUT created_at timestamp without time zone, OUT username character varying, OUT body text) OWNER TO hduser;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: following; Type: TABLE; Schema: public; Owner: hduser; Tablespace: 
--

CREATE TABLE following (
    "user" integer NOT NULL,
    follows integer NOT NULL
);


ALTER TABLE public.following OWNER TO hduser;

--
-- Name: tweets; Type: TABLE; Schema: public; Owner: hduser; Tablespace: 
--

CREATE TABLE tweets (
    body text NOT NULL,
    created timestamp without time zone DEFAULT now() NOT NULL,
    "user" integer NOT NULL,
    id integer NOT NULL
);


ALTER TABLE public.tweets OWNER TO hduser;

--
-- Name: tweets_id_seq; Type: SEQUENCE; Schema: public; Owner: hduser
--

CREATE SEQUENCE tweets_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.tweets_id_seq OWNER TO hduser;

--
-- Name: tweets_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: hduser
--

ALTER SEQUENCE tweets_id_seq OWNED BY tweets.id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: hduser; Tablespace: 
--

CREATE TABLE users (
    id integer NOT NULL,
    username character varying(64),
    password character varying(64),
    stream integer[]
);


ALTER TABLE public.users OWNER TO hduser;

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: hduser
--

CREATE SEQUENCE users_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_id_seq OWNER TO hduser;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: hduser
--

ALTER SEQUENCE users_id_seq OWNED BY users.id;


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: hduser
--

ALTER TABLE ONLY tweets ALTER COLUMN id SET DEFAULT nextval('tweets_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: hduser
--

ALTER TABLE ONLY users ALTER COLUMN id SET DEFAULT nextval('users_id_seq'::regclass);


--
-- Name: following_pk; Type: CONSTRAINT; Schema: public; Owner: hduser; Tablespace: 
--

ALTER TABLE ONLY following
    ADD CONSTRAINT following_pk PRIMARY KEY ("user", follows);


--
-- Name: tweets_pkey; Type: CONSTRAINT; Schema: public; Owner: hduser; Tablespace: 
--

ALTER TABLE ONLY tweets
    ADD CONSTRAINT tweets_pkey PRIMARY KEY (id);


--
-- Name: username_unique; Type: CONSTRAINT; Schema: public; Owner: hduser; Tablespace: 
--

ALTER TABLE ONLY users
    ADD CONSTRAINT username_unique UNIQUE (username);


--
-- Name: users_pkey; Type: CONSTRAINT; Schema: public; Owner: hduser; Tablespace: 
--

ALTER TABLE ONLY users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: following_follows_idx; Type: INDEX; Schema: public; Owner: hduser; Tablespace: 
--

CREATE INDEX following_follows_idx ON following USING btree (follows);


--
-- Name: tweet_main_idx; Type: INDEX; Schema: public; Owner: hduser; Tablespace: 
--

CREATE INDEX tweet_main_idx ON tweets USING btree ("user", created DESC NULLS LAST);


--
-- Name: tweets_created_idx; Type: INDEX; Schema: public; Owner: hduser; Tablespace: 
--

CREATE INDEX tweets_created_idx ON tweets USING btree (created DESC);


--
-- Name: following_follows_fkey; Type: FK CONSTRAINT; Schema: public; Owner: hduser
--

ALTER TABLE ONLY following
    ADD CONSTRAINT following_follows_fkey FOREIGN KEY (follows) REFERENCES users(id) ON DELETE CASCADE;


--
-- Name: following_user_fkey; Type: FK CONSTRAINT; Schema: public; Owner: hduser
--

ALTER TABLE ONLY following
    ADD CONSTRAINT following_user_fkey FOREIGN KEY ("user") REFERENCES users(id) ON DELETE CASCADE;


--
-- Name: tweet_to_user_fk; Type: FK CONSTRAINT; Schema: public; Owner: hduser
--

ALTER TABLE ONLY tweets
    ADD CONSTRAINT tweet_to_user_fk FOREIGN KEY ("user") REFERENCES users(id);


--
-- Name: public; Type: ACL; Schema: -; Owner: hduser
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM hduser;
GRANT ALL ON SCHEMA public TO hduser;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

