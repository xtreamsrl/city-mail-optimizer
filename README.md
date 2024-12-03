# City Mail Optimizer

## How To Run
If you want to install and run the project, follow the steps below:
1. Copy the GitHub URL and clone the repository using `git`:
    ```bash
    git clone <repository-url>
    ```
2. Go to the location where you cloned the repository:
    ```bash
    cd <repository-directory>
    ```
3. Install the dependencies in a Python environment. We suggest using [uv](https://docs.astral.sh/uv/):
    ```bash
    uv init
    ```
4. Now you are ready to run the main script; with `uv`, the command is:
    ```bash
    uv run city-mail-optimizer "<city-name>, <city-province>" --addresses-file-path "<addresses-file-path>"
    ```
   where `<city-name>` is the name of the city you want to optimize the mail delivery for, `<city-province>` is the 
   province of the city, and `<addresses-file-path>` is the path to the file containing the addresses to be optimized.
   Note that, the `<addresses-file-path>` should be a file where every line is an address in the format 
   `"<address>, <city>, <province>"`.
   

## How to Contribute
If you want to contribute to the project, keep in mind the following developer guidelines:
1. Always add dependencies using `uv`:
    ```bash
    uv add <package>
    ```
2. Install `pre-commit` and then use it to enable automatic code quality checks:
    ```bash
    pip install pre-commit
    pre-commit install
    ```
3. Always create a new branch for your changes:
    ```bash
    git checkout -b <branch-name>
    ```
4. Branch names shoud follow the [conventional commits](https://www.conventionalcommits.org/en/v1.0.0/) pattern, for example:
    ```bash
    git checkout -b feat/<feature-name>
    git checkout -b fix/<fix-name>
    git checkout -b docs/<docs-name>
    git checkout -b style/<style-name>
    git checkout -b refactor/<refactor-name>
    git checkout -b test/<test-name>
    ```
5. After you finish your changes, push the branch to the repository and create a pull request:
    ```bash
    git push origin <branch-name>
    ```
6. On GitHub, request a code review from a maintainer and wait for the approval.
7. After the approval, merge the branch into main with the "merge and squash" option and delete the branch both locally and remotely:
    ```bash
    git checkout main && git merge <branch-name> --squash
    git commit -m "merge commit message following conventional commits" && git push origin main
    git branch -d <branch-name> && git push origin --delete <branch-name>
    ```
