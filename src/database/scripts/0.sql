SET statement_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = off;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET escape_string_warning = off;
SET search_path = public, pg_catalog;
SET default_tablespace = '';
SET default_with_oids = false;

-- Role: kestava
DROP ROLE kestava;
CREATE ROLE kestava WITH LOGIN ENCRYPTED PASSWORD 'kestava123';

-- Table: items

CREATE TABLE items
(
  item_id serial NOT NULL,
  title character varying(200) NOT NULL,
  additional_description text,
  quantity numeric(10,2) NOT NULL,
  loc geography(Point,4326) NOT NULL,
  CONSTRAINT items_pk PRIMARY KEY (item_id)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE items OWNER TO jacob;
GRANT ALL ON TABLE items TO jacob;
GRANT SELECT, UPDATE, INSERT, DELETE ON TABLE items TO kestava;

-- Index: items_gix

CREATE INDEX items_gix
  ON items
  USING gist
  (loc);

GRANT USAGE ON TABLE items_item_id_seq TO kestava;

-- Table: accounts

CREATE TABLE accounts
(
  account_id serial NOT NULL,
  email character varying NOT NULL,
  CONSTRAINT user_accounts_pk PRIMARY KEY (account_id)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE accounts OWNER TO jacob;
GRANT ALL ON TABLE accounts TO jacob;
GRANT SELECT, UPDATE, INSERT, DELETE ON TABLE accounts TO kestava;

GRANT USAGE ON TABLE accounts_account_id_seq TO kestava;

-- Table: openid_accounts

CREATE TABLE openid_accounts
(
  openid_identifier character varying NOT NULL,
  account_id integer NOT NULL,
  CONSTRAINT openid_accounts_pk PRIMARY KEY (openid_identifier),
  CONSTRAINT openid_accounts_fk1 FOREIGN KEY (account_id)
      REFERENCES accounts (account_id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
)
WITH (
  OIDS=FALSE
);
ALTER TABLE openid_accounts OWNER TO jacob;
GRANT ALL ON TABLE openid_accounts TO jacob;
GRANT SELECT, UPDATE, INSERT, DELETE ON TABLE openid_accounts TO kestava;