class Post():
    """
    A class used to represent a Post

    title: str
    publication_date: str
    image_url: str
    content: str
    approved: bit
    user_id: int
        the id of the user who created the Post
    category_id: int 
        the type of category for the Post
    """

    def __init__(self, id, title, publication_date, image_url, content, approved, user_id, category_id):
        self.id = id
        self.title = title
        self.publication_date = publication_date
        self.image_url = image_url
        self.content = content
        self.approved = approved
        self.user_id = user_id
        self.category_id = category_id

        self.user = None
        self.category = None
