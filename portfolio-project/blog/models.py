from django.db import models

# Create A blog model here.
class Blog(models.Model):
    # title, pub_date, body, image
    title = models.CharField(max_length=25)
    pub_date = models.DateTimeField()
    body = models.TextField(max_length=500)
    image = models.ImageField(upload_to="images/")

    def summary(self):
        return self.body[:100]

    def pub_date_pretty(self):
        return self.pub_date.strftime('%b %e %Y')

    def __str__(self):
        return self.title


# Add the blog app to the settings
# create a migration
# migrate

# Add to the admin
