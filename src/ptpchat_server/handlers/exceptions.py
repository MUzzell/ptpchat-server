
class InvalidMessage(Exception):
    """Encapsulates handling any invalid messages received by the server

    """
    def __init__(self, culprit):
        """
        Args:
            culprit (string): The offending piece of data from the message
        """
        self.culprit

    def __srt__(self):
        return "Invalid message received, invalid {0} attribute".format(culprit)


class TtlExceeded(Exception):
    """Raised when the ttl of the message is 0 or 1 if not ment for us
    """
    def __init__(self, sender_id, msg_id):
        self.sender_id = sender_id
        self.msg_id = msg_id

    def __str__(self):
        return "TTL exceeded for message ({0}) from sender ({1})".format(
            msg_id, sender_id)