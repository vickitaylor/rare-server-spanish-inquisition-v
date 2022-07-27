class User():

    """
    A class used to represent a User
    """

    def __init__(self, id, first_name, last_name, username, email, password, bio, created_on, active):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.email = email
        self.password = password
        self.bio = bio
        self.created_on = created_on
        self.active = active
