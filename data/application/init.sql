CREATE
DATABASE IF NOT EXISTS subscribers;
       CREATE
USE
subscribers;
CREATE TABLE subscribed_chats
(
    chat_id       INT NOT NULL,
    subscriber_id INT NOT NULL,
    PRIMARY KEY (chat_id, subscriber_id)
);
