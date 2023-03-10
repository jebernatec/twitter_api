# Python
import json
from uuid import UUID, uuid4
from datetime import date, datetime
from typing import Optional, List

# Pydantic
from pydantic import BaseModel, EmailStr, Field

# FastAPI
from fastapi import FastAPI
from fastapi import status, Body

app = FastAPI()

# Models

class UserBase(BaseModel):
    #user_id: UUID = Field(default_factory= lambda: uuid.uuid4().hex)
    user_id: UUID = Field(default_factory= uuid4)
    email: EmailStr = Field(...)

class UserLogin(UserBase):
    password: str = Field(
        ...,
        min_length = 8,
        max_length = 25
    )

class User(UserBase):

    first_name: str = Field(
        ...,
        min_length = 1,
        max_length = 50
        )
    last_name: str = Field(
        ...,
        min_length = 1,
        max_length = 50
        )
    birth_date: Optional[date] = Field(default = None)

class UserRegister(User, UserLogin):
    pass

class Tweet(BaseModel):
    tweet_id: UUID = Field(default_factory= uuid4)
    content: str = Field(
        ...,
        max_length = 256,
        min_length = 1
        )
    created_at: datetime = Field(default = datetime.now())
    update_at: Optional[datetime] = Field(default = None)
    by: User = Field(...)


# Path Operations

## Users

### Register a user
@app.post(
    path = "/signup",
    response_model = User,
    status_code = status.HTTP_201_CREATED,
    summary = "Register a User",
    tags = ["Users"]
)
def signup(user: UserRegister = Body(...)):
    """
    Signup

    This path operation register a user in the app

    parameters:
        - Request body parameter
            - User: UserRegister
    
    Returns a json with the basic information:
        - user_id: UUID
        - email: EmailStr
        - first_name: str
        - last_name: str
        - birth_date: date
    """
    with open("users.json", "r+", encoding = "utf-8") as file:
         #results = json.loads(file.read())
         results = json.load(file)
         user_dict = user.dict()
         user_dict["user_id"] = str(uuid4())
         user_dict["birth_date"] = str(user_dict["birth_date"])
         results.append(user_dict)
         file.seek(0)
         file.write(json.dumps(results))
         
         return user

### Login a user
@app.post(
    path = "/login",
    response_model = User,
    status_code = status.HTTP_200_OK,
    summary = "Login a user",
    tags = ["Users"]
)
def login():
    pass

### Show all users
@app.get(
    path = "/users",
    response_model = List[User],
    status_code = status.HTTP_200_OK,
    summary = "Show all users",
    tags = ["Users"]
)
def users():
    """
    This path operation shows all users in the app

    Parameters:
        -
    Returns a json list with all users in the app, with the following keys
        - user_id: UUID
        - email: EmailStr
        - first_name: str
        - last_name: str
        - birth_date: date
    """

    with open("users.json", "r", encoding="utf-8") as file:
        results = json.load(file)
        return results

### Show a single user
@app.get(
    path = "/users/{user_id}",
    response_model = User,
    status_code = status.HTTP_200_OK,
    summary = "Show a user",
    tags = ["Users"]
)
def show_user():
    pass

### Delete a user
@app.delete(
    path = "/users/{user_id}/delete",
    response_model = User,
    status_code = status.HTTP_200_OK,
    summary = "Delete a user",
    tags = ["Users"]
)
def delete_user():
    pass

### Update a user
@app.put(
    path = "/users/{user_id}/update",
    response_model = User,
    status_code = status.HTTP_200_OK,
    summary = "Update a user",
    tags = ["Users"]
)
def update_user():
    pass


## Tweets

### Show all tweets
@app.get(
    path = "/",
    #response_model = List[Tweet],
    status_code = status.HTTP_200_OK,
    summary = "Show all tweets",
    tags = ["Tweets"]
    )
def home():
    """
    This path operation shows all tweets in the app

    Parameters:
        -
    Returns a json list with all tweets in the app, with the following keys:
        tweet_id: UUID;
        content: str;
        created_at: datetime; 
        update_at: Optional[datetime];
        by: User
    """

    with open("tweets.json", "r", encoding="utf-8") as file:
        results = json.load(file)
        return results
    

### Post a tweet
@app.post(
    path = "/post",
    response_model = Tweet,
    status_code = status.HTTP_201_CREATED,
    summary = "Post a tweet",
    tags = ["Tweets"]
)
def post(tweet: Tweet = Body(...)):
    """
    Post a Tweet 

    This path operation post a tweet

    parameters:
        - Request body parameter
            - tweet: Tweet
    
    Returns a json with the basic tweet information:
        tweet_id: UUID
        content: str
        created_at: datetime 
        update_at: Optional[datetime]
        by: User 
    """
    with open("tweets.json", "r+", encoding = "utf-8") as file:
         #results = json.loads(file.read())
         results = json.load(file)
         tweet_dict = tweet.dict()
         tweet_dict["tweet_id"] = str(uuid4())
         tweet_dict["created_at"] = str(tweet_dict["created_at"])
         if tweet_dict["update_at"]:
            tweet_dict["update_at"] = str(tweet_dict["update_at"])

         tweet_dict["by"]["user_id"] = str(uuid4())
         tweet_dict["by"]["birth_date"] = str(tweet_dict["by"]["birth_date"])
         results.append(tweet_dict)
         file.seek(0)
         file.write(json.dumps(results))
         
         return tweet

### Show a tweet
@app.get(
    path = "/post/{tweet_id}",
    response_model = Tweet,
    status_code = status.HTTP_200_OK,
    summary = "Show a tweet",
    tags = ["Tweets"]
)
def show_tweet():
    pass

### Delete a tweet
@app.delete(
    path = "/post/{tweet_id}/delete",
    response_model = Tweet,
    status_code = status.HTTP_200_OK,
    summary = "Delete a tweet",
    tags = ["Tweets"]
)
def delete_tweet():
    pass

### Update a tweet
@app.put(
    path = "/post/{tweet_id}/update",
    response_model = Tweet,
    status_code = status.HTTP_200_OK,
    summary = "Update a tweet",
    tags = ["Tweets"]
)
def Update_tweet():
    pass