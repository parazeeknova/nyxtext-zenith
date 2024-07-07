<h3 align="center">
	<img src="assets/Zenith-logo.png" width="350" alt="Logo"/><br/>
    Contributing to Nyxtext Zenith
    <img src="assets/misc/transparent.png" height="30" width="0px"/>
</h3>

### Ways to Contribute : 

There are several ways you can contribute to Nyxtext Zenith, including but not limited to the following:

1. **Code Contributions:** Fix bugs, implement new features, or improve existing functionality by submitting pull requests.
   
2. **Documentation:** Help improve the project's documentation by fixing errors, adding missing information, or clarifying existing content.

3. **Bug Reporting:** Report bugs, issues, or unexpected behavior you encounter while using NyxNote. Please provide detailed steps to reproduce the issue.

4. **Feature Requests:** Suggest new features, enhancements, or improvements you'd like to see in Nyxtext Zenith. Describe the feature and its potential benefits.

### Code Guidelines : 

When contributing code to Nyxtext Zenith, please adhere to the following guidelines:

- Write clear and concise code with meaningful variable names and comments where necessary.
- Test your changes thoroughly to ensure they do not introduce regressions or break existing functionality.

To get started, make a fork of Nyxtext Zenith with the button in the top right corner of this page.
Then install Python and [git](https://git-scm.com/), and run these commands:

```bash
    git clone https://github.com/parazeeknova/nyxtext-zenith.git
    cd nyxtext
    python3 -m venv env
    source env/bin/activate
    pip install -r requirements.txt
    python -m zenith
```

This should run Nyxtext Zenith. If you change some of Nyxtext Zenith's code in the `zenith` directory and you run `python -m zenith` again, your changes should be visible right away.

Windows-specific notes:
- You need to use `py` instead of `python3` when creating the venv, and `env\Scripts\activate` instead of `source env/bin/activate` to activate it.
- If creating the venv fails with an error message like `Error: [Errno 13] Permission denied: ...\\python.exe`, try creating the venv into a different folder.  It is created into whatever folder you are currently `cd`'d to (i.e. the folder that shows up on the command prompt before the `>`).
