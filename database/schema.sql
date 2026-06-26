BEGIN;

------------------------------------------------------------
-- Movies
------------------------------------------------------------

CREATE TABLE IF NOT EXISTS movies (

    id BIGSERIAL PRIMARY KEY,

    external_id BIGINT NOT NULL UNIQUE,

    slug TEXT NOT NULL,

    url TEXT NOT NULL UNIQUE,

    title TEXT NOT NULL,

    description TEXT,

    cover TEXT,

    imdb REAL,

    year INTEGER,

    language TEXT,

    original_language TEXT,

    quality TEXT,

    format TEXT,

    runtime TEXT,

    filesize TEXT,

    genres TEXT[] DEFAULT '{}',

    cast TEXT[] DEFAULT '{}',

    writers TEXT[] DEFAULT '{}',

    directors TEXT[] DEFAULT '{}',

    screenshots TEXT[] DEFAULT '{}',

    tags TEXT[] DEFAULT '{}',

    download_links JSONB DEFAULT '[]',

    content_hash TEXT,

    links_hash TEXT,

    upload_date TIMESTAMP,

    created_at TIMESTAMP DEFAULT NOW(),

    updated_at TIMESTAMP DEFAULT NOW(),

    last_scraped TIMESTAMP,

    last_link_check TIMESTAMP

);

------------------------------------------------------------
-- Crawl Queue
------------------------------------------------------------

CREATE TABLE IF NOT EXISTS crawl_queue (

    id BIGSERIAL PRIMARY KEY,

    external_id BIGINT NOT NULL UNIQUE,

    url TEXT NOT NULL UNIQUE,

    status VARCHAR(20) NOT NULL DEFAULT 'pending',

    priority INTEGER NOT NULL DEFAULT 0,

    attempts INTEGER NOT NULL DEFAULT 0,

    error TEXT,

    created_at TIMESTAMP DEFAULT NOW(),

    updated_at TIMESTAMP DEFAULT NOW(),

    processed_at TIMESTAMP

);

------------------------------------------------------------
-- Crawler State
------------------------------------------------------------

CREATE TABLE IF NOT EXISTS crawler_state (

    worker TEXT PRIMARY KEY,

    current_page INTEGER NOT NULL DEFAULT 1,

    last_external_id BIGINT,

    updated_at TIMESTAMP DEFAULT NOW()

);

------------------------------------------------------------
-- Crawl History
------------------------------------------------------------

CREATE TABLE IF NOT EXISTS crawl_history (

    id BIGSERIAL PRIMARY KEY,

    worker TEXT,

    page INTEGER,

    urls_found INTEGER,

    success BOOLEAN,

    message TEXT,

    created_at TIMESTAMP DEFAULT NOW()

);

------------------------------------------------------------
-- Indexes
------------------------------------------------------------

CREATE INDEX IF NOT EXISTS idx_movies_external
ON movies(external_id);

CREATE INDEX IF NOT EXISTS idx_movies_updated
ON movies(updated_at);

CREATE INDEX IF NOT EXISTS idx_movies_scraped
ON movies(last_scraped);

CREATE INDEX IF NOT EXISTS idx_queue_status
ON crawl_queue(status);

CREATE INDEX IF NOT EXISTS idx_queue_priority
ON crawl_queue(priority DESC);

CREATE INDEX IF NOT EXISTS idx_queue_created
ON crawl_queue(created_at);

COMMIT;
