# Requirements.txt for Machine Learning Applications

**Note:** This README assumes that you are running your code in a virtual environment. If you are not using a virtual environment, you should create one before following the instructions in this README.

## What is a `requirements.txt` file?

A `requirements.txt` file is a text file that lists all of the Python packages that are required to run a particular Machine Learning application. This file is often used to share code with others, or to install the necessary packages on a new machine.

## What is pip-chill?

pip-chill is a command-line utility that lists all of the Python packages that are required to run a particular Python project, but only includes the packages that are not dependencies of other packages. This makes it a more lightweight alternative to pip freeze, which lists all of the packages that are currently installed in your environment.

## Difference between pip freeze and pip-chill

Let's say you have installed the following packages in your environment:

* `appdirs`
* `black`
* `click`

If you run the `pip freeze` command, you will see the following output:

```
(foo) $ pip freeze
appdirs==1.4.4
black==20.8b1
click==7.1.2
```

As you can see, the `pip freeze` command includes all of the packages that are installed in your environment, including dependencies.

If you run the `pip-chill` command, you will see the following output:

```
(foo) $ pip-chill
black==20.8b1
```

As you can see, the `pip-chill` command only includes the packages that are required to run the project.

 **pip-chill -v**

The `pip-chill -v` command will print more verbose output, including the names of the dependencies of the packages in the form of comments.


```
(foo) $ pip-chill -v --no-version
black
# appdirs # Installed as dependency for black
# click # Installed as dependency for black
```

## How to install pip-chill

To install pip-chill, you can run the following command in your virtual environment:

```
pip install pip-chill
```

## How to create a `requirements.txt` file

There are two ways to create a `requirements.txt` file:

* **Using pip-chill:**

    The easiest way to create a `requirements.txt` file is to run the following command in your virtual environment:

    ```
    pip-chill > requirements.txt
    ```

    This command will create a `requirements.txt` file that lists all of the Python packages that are required to run the project.

* **Manually:**

    If you want to create a `requirements.txt` file manually, you can list all of the Python packages that are required by your code. For example, if your code requires the `numpy` and `pandas` packages, you would add the following lines to your `requirements.txt` file:

    ```
    numpy
    pandas
    ```


## Using a `requirements.txt` file

To use a `requirements.txt` file, you can install the packages manually by running the following command:

```
pip install -r requirements.txt
```


## Best practices for creating a `requirements.txt` file

When creating a `requirements.txt` file, it is important to consider the following:

* **Use the latest versions of the packages:**

    The latest versions of the packages are likely to be the most stable and feature-rich. However, it is important to test your code with the latest versions of the packages before you deploy it to production.

* **Specify the exact versions of the packages:**

    If you are using a specific version of a package, you should specify the exact version in your `requirements.txt` file. This will ensure that your code will only work with that specific version of the package.

* **Comment out any packages that are not required:**

    If you are not using a particular package, you should comment it out in your `requirements.txt` file. This will make your `requirements.txt` file easier to read and maintain.



## Automate Updating and Installing `requirements.txt`

Instead of manually updating and installing `requirements.txt`, you can create two batch files: `update_requirements.bat` and `install_requirements.bat`.

### `update_requirements.bat`

```
@echo off

rem Check if the virtual environment is activated
if not exist "%VIRTUAL_ENV%" (
  echo "Virtual environment is not activated. Activating..."
  call path\to\venv\Scripts\activate
)

rem Run the pip-chill command
pip-chill > path\to\project\requirements.txt
pip-chill -v > path\to\project\requirements1.txt
```

This batch file first checks if the virtual environment is activated. If it is not activated, the batch file activates the virtual environment. Then, the batch file runs the `pip-chill` command to generate a new `requirements.txt` file in your project directory. The `pip-chill` command will also generate a verbose version of the `requirements.txt` file, which is saved as `requirements1.txt`.

### `install_requirements.bat`

```
@echo off

rem Check if the virtual environment is activated
if not exist "%VIRTUAL_ENV%" (
  echo "Virtual environment is not activated. Activating..."
  call path\to\venv\Scripts\activate
)

rem Install the packages from the requirements file
pip install -r path\to\project\requirements.txt
```

This batch file first checks if the virtual environment is activated. If it is not activated, the batch file activates the virtual environment. Then, the batch file installs the packages from the `requirements.txt` file in your project directory.

To run the batch files, you can double-click them or open a command prompt and navigate to the directory where the batch files are stored. Then, you can run the batch files by typing the following commands:

```
update_requirements.bat
install_requirements.bat
```

It is recommended **not** to save the batch files in your project directory because the batch files are hard coded to your personal virtual environment.


