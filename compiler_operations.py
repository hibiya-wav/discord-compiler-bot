import subprocess
import traceback
import requests
import os
import json
from dotenv import load_dotenv

load_dotenv()
CLIENT_ID = os.getenv("JDOODLE_CLIENT_ID")
CLIENT_SECRET = os.getenv("JDOODLE_CLIENT_SECRET")


def API_CALL(input_code, language, version_flag):
    api_url = "https://api.jdoodle.com/v1/execute"
    new_request = requests.post(api_url,
                                json={
                                    "clientId": f"{CLIENT_ID}",
                                    "clientSecret": f"{CLIENT_SECRET}",
                                    "script": f"{input_code}",
                                    "language": f"{language}",
                                    "versionIndex": f"{version_flag}"
                                }
                                )

    # 'output' is the key for the value which is what compiles which is what we want.
    compile_return = json.loads(new_request.content)
    return '**Output:** ' + f'({language})' + '\n```' + compile_return['output'] + '\n```'


def python_checker(input_code, language, version_flag):
    tempfile = open("tempFile.py", "w")
    tempfile.write(input_code)
    tempfile.close()

    try:
        completed_process = subprocess.run(["bash_scripts/python_test.sh"], capture_output=True, text=True)
        output = completed_process.stdout
        error_output = completed_process.stderr
        output_message = completed_process.stderr.split()[7:]
        output_message = " ".join(output_message)

        if error_output:
            error_message = f"(Error occurred)\n```{output_message}```"
            os.remove("tempFile.py")
            return '**Output:** ' + error_message
        else:
            os.remove("tempFile.py")
            return API_CALL(input_code, language, version_flag)
    except subprocess.CalledProcessError as e:
        error_output = f"Error occurred (return code {e.returncode}):\n"
        error_output += "```python\n" + traceback.format_exc() + "```"
        os.remove("tempFile.py")
        return '**Output:** ' + error_output


def cpp_checker(input_code, language, version_flag):
    tempfile = open("tempFile.cpp", "w")
    tempfile.write(input_code)
    tempfile.close()

    try:
        completed_process = subprocess.run(["bash_scripts/cpp_test.sh"], capture_output=True, text=True)
        output = completed_process.stdout
        error_output = completed_process.stderr
        output_message = completed_process.stderr.split()[7:]
        output_message = " ".join(output_message)

        if error_output:
            error_message = f"(Error occurred)\n```{output_message}```"
            os.remove("tempFile.cpp")
            return '**Output:** ' + error_message
        else:
            os.remove("tempFile.cpp")
            return API_CALL(input_code, language, version_flag)
    except subprocess.CalledProcessError as e:
        error_output = f"Error occurred (return code {e.returncode}):\n"
        error_output += "```python\n" + traceback.format_exc() + "```"
        os.remove("tempFile.cpp")
        return '**Output:** ' + error_output


def delete_java_files():
    os.remove("Main.java")
    if os.path.exists("Main.class"):
        os.remove("Main.class")


def java_checker(input_code, language, version_flag):
    tempfile = open("Main.java", "w")
    tempfile.write(input_code)
    tempfile.close()

    try:
        completed_process = subprocess.run(["bash_scripts/java_test.sh"], capture_output=True, text=True)
        output = completed_process.stdout
        error_output = completed_process.stderr
        output_message = completed_process.stderr.split()[7:]
        output_message = " ".join(output_message)

        if error_output:
            error_message = f"(Error occurred)\n```{output_message}```"
            delete_java_files()
            return '**Output:** ' + error_message
        else:
            delete_java_files()
            return API_CALL(input_code, language, version_flag)
    except subprocess.CalledProcessError as e:
        error_output = f"Error occurred (return code {e.returncode}):\n"
        error_output += "```python\n" + traceback.format_exc() + "```"
        delete_java_files()
        return '**Output:** ' + error_output


def bash_checker(input_code, language, version_flag):
    tempfile = open("tempFile.sh", "w")
    tempfile.write(input_code)
    tempfile.close()

    try:
        completed_process = subprocess.run(["bash_scripts/bash_test.sh"], capture_output=True, text=True)
        output = completed_process.stdout

        if len(output) != 0:  # output only takes in information if the input source code is incorrect in bash. returns nothing if process is OK/0
            error_message = f"(Error occurred)\n```{output}```"
            os.remove("tempFile.sh")
            return '**Output:** ' + error_message
        else:
            os.remove("tempFile.sh")
            return API_CALL(input_code, language, version_flag)
    except subprocess.CalledProcessError as e:
        error_output = f"Error occurred (return code {e.returncode}):\n"
        error_output += "```python\n" + traceback.format_exc() + "```"
        os.remove("tempFile.sh")
        return '**Output:** ' + error_output


def formatter(process_code):
    input_code = process_code.split("\n")[2:-1]
    input_code = '\n'.join(input_code)
    return input_code


def compileInfo(language: str, input_code: str):
    version_flag = "none"
    return_flag = 0
    if language.lower() == "python":
        input_code = formatter(input_code)
        language = "python3"
        version_flag = "4"
        return python_checker(input_code, language, version_flag)
    elif language.lower() == "c++":
        input_code = formatter(input_code)
        language = "cpp17"
        version_flag = "1"
        return cpp_checker(input_code, language, version_flag)
    elif language.lower() == "java":
        input_code = formatter(input_code)
        language = "java"
        version_flag = "4"
        return java_checker(input_code, language, version_flag)

    elif language.lower() == "bash":
        input_code = formatter(input_code)
        language = "bash"
        version_flag = "4"
        return bash_checker(input_code, language, version_flag)
    else:
        return '**Output:**\n```Unsupported language.\nIf you wish to add any additional support for any pre-existing ' \
               'or your own language, check out: https://github.com/hibiya-wav/discord-compiler-bot\n```'
