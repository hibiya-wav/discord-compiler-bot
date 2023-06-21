# Discord Compiler Bot

This GitHub repository contains the source code of a Discord bot that allows you to send source code snippets to the bot via chat and receive compiled output in response. The bot supports four programming languages: Python, C++, Java, and Bash. It incorporates syntax checking to avoid unnecessary API credit consumption on invalid code.

## How to use

### 1. Install [Discord](https://discord.com/developers/docs/intro)

Make sure you have Discord installed on your device. If you don't have it yet, you can download and install it from the official Discord website.

### 2. Code Away!

The general syntax to use with requesting an action from the bot is to start with `!compile` and place both the programming language name and source code in between the `````` ``` ``````

Example:

    !compile
    ```<programming-language>
    <insert-code>
    ```

* When using Markdown, ensure that there are no spaces between the triple backticks `````` ``` `````` and `<programming-language>`. This is necessary to ensure correct code processing and highlighting in Discord and the bot.

Here's a simple example for a request to send that the bot can read and then process/compile:

    !compile
    ```python
    print("Hi There!")
    ```

If you wish for your compilation to return in your DM's, use `?!compile` instead of `!compile`.

## Hosting
If you want to host this bot on your own local machine or server, follow these steps:

1. Copy the repository to your desired location.
2. Fill out the fields in `env.example` and save the file as `.env`.
   - You will need a Discord API Key and a JDOODLE API Key, which you can obtain for free.
3. Install any missing requirements listed in `requirements.txt`, as well as the latest Java, GCC, Bash versions.
4. Run `main.py` to start the bot.

## Updates
You are free to copy, learn from, make your own version, or even contribute updates to this repository through pull requests. If you have any questions or need assistance with this repository or its code, feel free to contact me by email.

