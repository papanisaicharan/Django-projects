from django.db import models

# Create A blog model here.
class Blog(models.Model):
    # title, pub_date, body, image
    title = models.CharField(max_length=25)
    pub_date = models.DateTimeField()
    body = models.TextField(max_length=300)
    image = models.ImageField(upload_to="images/")



# Add the blog app to the settings
# create a migration
# migrate

# Add to the admin
