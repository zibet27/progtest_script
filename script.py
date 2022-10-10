# HOW TO USE
# Unix system is preferable
# Install sample data in the Progtest website
# You can see the "Download" button under the condition of the problem
# After installation move this "sample.tgz" to your project directory
# Then run "python3 script.py" in your project directory
# Or "python3 script.py project-name" if you have the script in another folder.
# PS: Change the "project-name" to destination to your project directory


import os
import sys
import subprocess

path_to_dir = sys.argv[1] if len(sys.argv) == 2 else ""

cwd = os.path.join(os.getcwd(), path_to_dir)
tests_folder = os.path.join(cwd, "ENG")

if not os.path.exists(tests_folder):
    if not os.path.exists(os.path.join(cwd, "sample.tar")):
        subprocess.run(["gunzip", "sample.tgz"])
    subprocess.run(["tar", "xf", "sample.tar"])

subprocess.run(["g++", os.path.join(path_to_dir, "main.c"), "-Wall", "-Wextra"])

failed_count = 0
success = '\033[96m'
warning = "\033[93m"
end = '\033[0m'

for filename in os.listdir(tests_folder):
    if "_in.txt" in filename:
        data = os.path.join(tests_folder, filename)
        expected = os.path.join(tests_folder, filename.replace("in", "out"))
        subprocess.run("./a.out < " + data + " > output.txt", shell=True)
        try:
            res = subprocess.check_output("diff output.txt " + expected, shell=True)
        except subprocess.CalledProcessError as error:
            lines = error.output.decode("utf-8").split("\n")
            failed_count += 1
            lines.pop()
            print(warning + "Incorrect output running ./a.out with " + filename, end, "Difference:")
            for line in lines:
                print(line)

if failed_count == 0:
    print(success + "Everything is fine", end)

if os.path.exists("output.txt"):
    os.remove("output.txt")
if os.path.exists("a.out") and path_to_dir != "":
    os.remove("a.out")
