CREATE TABLE IF NOT EXISTS messages (
        chatid TEXT,
        messageid int PRIMARY KEY,
        date DATE,
        messagetext TEXT,
        is_reply BOOL,
        reply_messageid int,
        is_sticker bool,
        sticker_id TEXT
);
