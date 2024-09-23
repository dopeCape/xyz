import mongoengine as me

# Connect to MongoDB
me.connect(
    db="PayTm-Clone",
    username="swaraj",
    password="Swaraj2004",
    host="mongodb+srv://cluster0.txvw2vk.mongodb.net/PayTm-Clone"
)

# Define the User document schema


class User(me.Document):
    username = me.StringField(required=True)
    first_name = me.StringField()
    last_name = me.StringField()
    password = me.StringField()

# Define the Account document schema


class Account(me.Document):
    user = me.ReferenceField(User, required=True)
    balance = me.FloatField()

# Example of saving a User
# user = User(username="john_doe", first_name="John", last_name="Doe", password="securepassword123")
# user.save()

# Example of saving an Account linked to the User
# account = Account(user=user, balance=100.0)
# account.save()
