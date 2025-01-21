# TruthAutonomy

<!-- ![TruthAutonomy Logo](https://via.placeholder.com/600x200?text=TruthAutonomy) -->

TruthAutonomy is a Python library designed to streamline interactions with Truth Social. It enables seamless posting, media uploads, and workflow automation, providing AI agents and developers with a powerful and intuitive tool for efficient social media management. 🚀

---

## 🌟 Features

- **Seamless Post Creation**: Effortlessly create posts with customizable visibility and additional metadata.
- **Media Uploading**: Upload images, videos, and other media types with ease.
- **Robust Error Handling**: Handle API errors gracefully with built-in exceptions.
- **Lightweight & Fast**: For bypassing challenges and ensuring smooth communication.

---

## 🔧 Installation

Install TruthAutonomy via `pip`:

```bash
pip install git+https://github.com/TruthIntel/TruthAutonomy
```

---

## 🚀 Quick Start

Here’s how to get started:

### Initialize the Client

```python
from truthautonomy import TruthSocial

# Replace with your Bearer token
auth_bearer = "YOUR_BEARER_TOKEN"
client = TruthSocial(auth_bearer=auth_bearer)
```

### Create a Post

```python
response = client.send_post(
    content="Hello, TruthSocial! This is my first post. 🚀",
    visibility="public"
)
print(response.url)  # View your post's URL
```

### Upload Media

```python
media_response = client.send_post(
    content="Hello, TruthSocial! This is my first post. 🚀",
    media_files=["path/to/image.jpg"]
    visibility="public"
)
print(media_response.url)  # Get the uploaded media's URL
```
---

### **Search**

```python
# Search for posts containing the keyword 'news'
results = client.search(query="news", search_type="statuses", limit=10)

for result in results.get("statuses", []):
    print(result["content"])
```

---

### **Pull Statuses**

```python
from datetime import datetime

# Pull recent statuses from a user
statuses = client.pull_statuses(
    username="truthuser",
    replies=False,
    verbose=True,
    created_after=datetime(2024, 1, 1),  # Fetch posts created after this date
)

for status in statuses:
    print(status["content"])
```

---

### **Pull Comments**

```python
# Pull comments for a given post
comments = client.pull_comments(post_id="123456789", include_all=True, top_num=50)

for comment in comments:
    print(comment["content"])
```

---

#### Fetch Users Who Liked a Post

```python
# Example Post URL
post_url = "https://truthsocial.com/@user/post/12345"

# Fetch top 10 users who liked the post
for user in client.user_likes(post_url, include_all=False, top_num=10):
    print(user)
```

---

#### Fetch Followers of a User

```python
# Fetch followers of a user by handle
for follower in client.user_followers(user_handle="@user", maximum=50):
    print(follower)
```

---

#### Fetch Users a User is Following

```python
# Fetch following list of a user
for following in client.user_following(user_handle="@user", maximum=50):
    print(following)
```

---

#### Post a New Status

```python
# Post content with optional media
content = "Hello, TruthSocial!"
media_files = ["path/to/image1.jpg", "path/to/image2.png"]

response = client.send_post(content, media_files=media_files, visibility="public")
print(response)
```

---

#### Upload Media

```python
# Upload a single media file
media_file = "path/to/media.jpg"
media_response = client.upload_media(media_file)
print(f"Uploaded Media ID: {media_response.id}")
```

---

#### Lookup a User's Information

```python
# Get user information by handle
user_info = client.lookup(user_handle="@user")
print(user_info)
```

---

#### Fetch Trending Posts

```python
# Fetch top 10 trending posts
trending_posts = client.trending(limit=10)
print(trending_posts)
```

---

#### Fetch Trending Tags

```python
# Fetch trending tags
tags = client.tags()
print(tags)
```

---

#### Fetch Suggested Users

```python
# Fetch suggested users
suggested_users = client.suggested(maximum=20)
print(suggested_users)
```

---

#### Fetch Trending Group Tags

```python
# Fetch trending group tags
group_tags = client.group_tags()
print(group_tags)
```

---

#### Fetch Group Posts

```python
# Fetch posts from a specific group
group_id = "12345"
group_posts = client.group_posts(group_id, limit=10)
print(group_posts)
```

---

#### Simulate Random Interactions

```python
# Perform random user interactions
client.random_interactions()
```

---

#### Generate Random Trending Tags

```python
# Generate random trending tags
trending_tags = client.random_trending_tags()
print(trending_tags)
```

---

#### Generate Random Suggestions

```python
# Generate random user and group suggestions
suggestions = client.random_suggestions()
print(suggestions)
```

---

## 🤝 Contributing

We welcome contributions from the community! Feel free to:

- Open issues for bugs or feature requests.
- Fork the repository and submit pull requests.

Before contributing, please read our [CONTRIBUTING.md](CONTRIBUTING.md).

---

## 📄 License

TruthAutonomy is licensed under the [MIT License](LICENSE). You are free to use, modify, and distribute this software.

---

## 💡 Inspiration

TruthAutonomy was built with the vision of providing developers with the tools to engage with Truth Social effortlessly. We aim to support innovation and creativity within the community.

---

## 🙌 Support

If you encounter any issues or have questions, feel free to open an issue on GitHub or reach out to us directly.

Happy coding! 🌟

