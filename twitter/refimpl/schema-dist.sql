CREATE TABLE users (
    "id" serial,
    "username" varchar(64) unique,
    "password" varchar(64),
    CONSTRAINT "users_pkey" PRIMARY KEY ("username") NOT DEFERRABLE INITIALLY IMMEDIATE
)
distribute by replication;
CREATE INDEX "users_id_idx" ON users USING btree(id);

CREATE TABLE following (
    "user" int4 NOT NULL,
    "follows" int4 NOT NULL,
    CONSTRAINT "following_pk" PRIMARY KEY ("user", "follows") NOT DEFERRABLE INITIALLY IMMEDIATE
)
distribute by replication;
CREATE INDEX "following_follows_idx" ON "public".following USING btree(follows);

CREATE TABLE tweets (
    "body" text NOT NULL,
    "created" timestamp(6) NOT NULL DEFAULT now(),
    "user" int4 NOT NULL,
    "id" serial,
    CONSTRAINT "tweets_pkey" PRIMARY KEY ("id", "user") NOT DEFERRABLE INITIALLY IMMEDIATE
)
distribute by hash("user");
CREATE INDEX "tweet_by_user_idx" ON tweets USING btree("user");
CREATE INDEX "tweets_created_idx" ON tweets USING btree(created DESC);