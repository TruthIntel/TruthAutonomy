# TruthAutonomy

<!-- ![TruthAutonomy Logo](https://via.placeholder.com/600x200?text=TruthAutonomy) -->

TruthAutonomy is a Python library that simplifies interaction with Truth Social's API. Whether you're posting content, uploading media, or automating your workflow, TruthAutonomy empowers developers with an easy-to-use and feature-rich solution. 🚀

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

### 1. Initialize the Client

```python
from truthautonomy import TruthSocial

# Replace with your Bearer token
auth_bearer = "YOUR_BEARER_TOKEN"
ts = TruthSocial(auth_bearer=auth_bearer)
```

### 2. Create a Post

```python
response = ts.send_post(
    content="Hello, TruthSocial! This is my first post. 🚀",
    visibility="public"
)
print(response.url)  # View your post's URL
```

### 3. Upload Media

```python
media_response = response = ts.send_post(
    content="Hello, TruthSocial! This is my first post. 🚀",
    media_files=["path/to/image.jpg"]
    visibility="public"
)
print(media_response.url)  # Get the uploaded media's URL
```

---

## 📖 Documentation

### Initialization

```python
TrustSocial(auth_bearer: str)
```
- **auth_bearer** *(str)*: Your Truth Social Bearer token (required).

### Methods

#### `send_post()`

Create a post on Truth Social.

```python
ts.send_post(
    content: str,                # Post content
    media_files: List[str] = [], # Optional list of media file paths or media IDs
    visibility: str = "public"   # Post visibility: "public", "private", etc.
)
```

#### `upload_media()`

Upload a media file to Truth Social.

```python
media_response = ts.upload_media(file_path: str)
```

- **file_path** *(str)*: Path to the media file.

---

## 🛠️ Development

Clone the repository and set up the environment:

```bash
git clone https://github.com/TruthIntel/truthautonomy.git
cd truthautonomy
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Run the tests:

```bash
python -m unittest test.py
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

