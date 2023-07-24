from mfrc522 import SimpleMFRC522

class NonBlockingBasicMFRC522(SimpleMFRC522):
    def __init__(self):
        super().__init__()
        self.MFRC522 = self.READER

    def read_no_block(self):
        """
        Attempt to read data from the RFID tag.

        Returns:
            tuple: A tuple containing the tag ID (as an integer) and the data read (as a string),
                or (None, None) if the operation fails.
        """
        # Send request to RFID tag
        (status, TagType) = self.MFRC522.Request(self.MFRC522.PICC_REQIDL)
        if status != self.MFRC522.MI_OK:
            return None, None

        # Anticollision, return UID if success
        (status, uid) = self.MFRC522.Anticoll()
        if status != self.MFRC522.MI_OK:
            return None, None

        # Convert UID to integer and store as the tag ID
        id = self._uid_to_num(uid)

        # Select the RFID tag using the UID
        self.MFRC522.SelectTag(uid)

        # Authenticate with the tag using the provided key
        status = self.MFRC522.Authenticate(self.MFRC522.PICC_AUTHENT1A, 8, self.KEY, uid)

        # Initialize variables for storing data and text read from the tag
        data = []
        text_read = ''

        if status == self.MFRC522.MI_OK:
            # Read data blocks specified by block_addr
            for block_num in range(8):
                block = self.MFRC522.Read(block_num)
                if block:
                    data += block

            # Convert data to string
            if data:
                text_read = ''.join(chr(i) for i in data)

        # Stop cryptographic communication with the tag
        self.MFRC522.StopCrypto1()

        # Return the tag ID and the read data
        return id, text_read
