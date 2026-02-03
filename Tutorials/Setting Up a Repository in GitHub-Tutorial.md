# Setting Up a Repository in GitHub

This tutorial walks through creating a GitHub repository, cloning it locally, and converting tutorials into Markdown so they render cleanly on GitHub.

## Create a Repository

Repository URL:
<https://github.com/BennettLandman/ES3890Spring2026>

## Tools Used

- VS Code: <https://code.visualstudio.com>
- GitHub

## Clone the Repository

```bash
git clone https://github.com/BennettLandman/ES3890Spring2026.git
```

## Organize Tutorials

Create a folder for tutorials or how-to guides. For example, include prior tutorials such as the VibeVoice setup guide.

```bash
mkdir tutorials
```

## Configure Git (One Time Setup)

```bash
git config --global user.name "Bennett Landman"
git config --global user.email "bennett.landman@vanderbilt.edu"
```

## Add Files and Commit

Remember:
- **Commit** is local only
- **Commit & Push** sends changes to GitHub

```bash
git add .
git commit -m "Add tutorial"
git push
```

## Converting Word to Markdown

Binary Word files are not easily viewable on GitHub. Convert them to Markdown using an LLM or another conversion tool.

1. Convert to Markdown
2. Paste into a new `.md` file in VS Code
3. Save
4. Commit and push

## Result

Once pushed, the tutorial is cleanly rendered and viewable directly on GitHub.

Poof. 🎉
