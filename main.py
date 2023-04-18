from sender import Sender


def main():
    server_config: str = './in/configs.json'
    message_text: str = './in/message.txt'
    receivers_file: str = './in/emails.txt'
    sender: Sender = Sender(server_config, message_text)
    sender.sendMessage(receivers_file)


if __name__ == "__main__":
    main()
